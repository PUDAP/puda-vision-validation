---
name: puda-machine-vision-validation
description: Use before physical PUDA workflows at BEARS, IMRE, NTU, or another configured environment when execution depends on visually verifiable machine setup, workspace occupancy, fixtures, labware, targets, tools, cables, or addressable positions. Select the active environment and machine profile, capture fresh evidence, and block uncertain or mismatched motion.
---

# PUDA Machine Vision Validation

## Goal

Provide one environment- and machine-neutral visual safety gate for PUDA-connected machines at **BEARS, IMRE, NTU, and future PUDA environments**. Validate the current physical scene before motion or execution without assuming that two sites—or two machines with the same `machine_id`—share a camera, calibration, workspace, deck, fixtures, or coordinates.

This skill validates visible physical state. It does not replace protocol validation, machine telemetry, calibration, interlocks, homing requirements, or operator approval.

## When to Use

Use this skill when a PUDA workflow depends on any visually checkable condition, including:

- deck, stage, tray, pan, holder, fixture, cell, vessel, tool, gripper, or target placement
- required-empty or keep-out regions
- addressable wells, tips, channels, samples, bins, or grid positions
- camera-guided alignment, pickup, placement, or inspection
- user requests for vision validation without execution

Use the environment-specific machine skill selected from the active PUDA environment. Known routes are `bears-machines`, `imre-machines`, and `ntu-machines`. Do not force vision validation onto a machine that has no suitable current image source or whose critical state cannot be established visually.

## No-Execution Boundary

For a validation-only request:

- allowed: read the planned protocol, inspect machine definitions, capture a passive fresh frame, crop/rectify/annotate copies, compare with authoritative references, hash evidence, and report the gate result
- prohibited: home, jog, scan, move, grip, pick, dispense, tare, start a run, reset faults, energize outputs, or change machine state unless the user separately authorizes that action

A camera command can itself move hardware or alter machine state. Prefer an already-configured passive stream or snapshot endpoint. If capture requires motion (for example, moving an arm to a scan pose), ask for approval before moving.

## Machine Profile Contract

Before inspection, build or load a profile containing:

| Field | Requirement |
|---|---|
| `environment` | Active PUDA environment/site from `puda env current`, such as `bears`, `imre`, or `ntu` |
| `machine_id` | Exact PUDA machine identifier in that environment; profile identity is `(environment, machine_id)` |
| `image_source` | Environment-scoped passive stream/snapshot or approved capture command; never reuse another site's endpoint |
| `camera_pose` | Named/fixed pose and calibration validity, when applicable |
| `workspace_model` | Full machine/deck boundary plus every visible addressable slot, zone, tray, fixture, stage, pan, channel, or free-space region that must receive an annotation box |
| `expected_objects` | Required object, identity/category, role, and expected region |
| `required_states` | Open/closed, occupied/empty, attached/detached, aligned, connected, etc. |
| `coordinate_model` | Optional named positions and their authoritative definition |
| `reference_sources` | Official library, driver docs, machine drawings, labels, or current project record |
| `safety_gate` | Which uncertain/mismatched observations block execution |

If any field needed for the requested check is missing and cannot be retrieved, report that limitation instead of borrowing an Opentrons convention.

## Environment and Machine Selection

1. Run `puda env current`; do not infer the site from hostname, working directory, chat title, or earlier sessions.
2. Load the matching environment skill:

   | Environment | Machine skill |
   |---|---|
   | `bears` | `bears-machines` |
   | `imre` | `imre-machines` |
   | `ntu` | `ntu-machines` |

3. If the environment skill is unavailable, stop and request installation with `puda skills install pudap/<environment>-skills`.
4. Select the exact `machine_id` from the current environment skill and confirm it with live discovery/command schema when needed.
5. Build/load a profile keyed by **environment + machine ID + camera ID/pose**. Never reuse camera geometry, pixel-to-robot calibration, workspace regions, or identity confirmations from another site.

### Environment Integration

- **BEARS:** use `bears-machines` and `bears-workflows`. Opentrons-specific deck validation may additionally load `puda-opentrons-vision-validation`, but its camera calibration and expected scene remain BEARS-instance-specific.
- **IMRE:** use `imre-machines` for machines such as PipQuBotV3, centrifuge, Dobot M1Pro, and BioShake. Validate machine-native trays, rotor/tube positions, gripper regions, clamp state, and keep-out zones only when current references and a safe camera are available.
- **NTU:** use `ntu-machines` for machines such as First, PipQuBotV3, Biologic, centrifuge, Dobot M1Pro, BioShake, balance, and Opentrons. An Opentrons adapter can supply deck semantics, but BEARS camera coordinates or slot polygons must never be reused at NTU.
- **Future environments:** load `<environment>-machines`; if absent, build a profile from current official driver/docs and the contract above.

### Machine-Family Rules

#### Liquid handlers

Validate site-specific deck/tray regions, labware, tip/tool state, required-empty areas, and requested addressable positions. Do not assume an OT-2 12-slot deck or A1 orientation unless the selected machine definition establishes it.

#### Robot arms and grippers

Record the active camera, camera pose, calibration, target description, tool/gripper state, pickup/placement regions, and keep-out zones. A fresh image from an unknown or changed pose cannot prove robot coordinates. Vision-only validation must not initiate scanning, arm motion, or gripper motion.

#### Centrifuges and shakers

Vision may validate visible tube/plate occupancy, balance pattern, lid/clamp state, and surrounding clearance when a safe camera exists. It cannot prove rotor balance, latch interlock, RPM, temperature, or stopped state; verify those through the machine driver/telemetry.

#### Balances

Vision may confirm that a vessel is centered on the pan and the surrounding area appears clear. It cannot prove tare state, calibrated mass, serial connectivity, or data freshness.

#### Electrochemical equipment

Validate visible cell/fixture/cable placement only when the current environment provides a camera and explicit connection map. An image cannot prove channel configuration, electrical continuity, voltage limits, or test readiness.

#### Other or new machines

Use machine-native region names and current environment references. If no safe fresh image can be captured, return `not visible` and keep the execution gate closed.

## Evidence Policy

Every validation is independent and must use:

1. the current user request or current protocol as the expected scene,
2. a fresh image captured for this validation, and
3. current machine-specific authoritative references.

Do not carry object identity, occupancy, orientation, or alignment confirmations from an earlier capture into a new validation. Earlier corrections may improve the inspection method but do not prove the current scene.

Record:

- active PUDA environment/site from `puda env current`
- capture time and provenance
- environment-scoped machine ID and camera/pose identifier
- image path, non-zero size, and SHA-256
- whether capture was passive or required an approved command
- any cropping, perspective correction, or enhancement applied to copies

Never expose camera credentials or secret connection strings in reports or committed files.

## Required Machine-Deck Box Annotation

Follow the full-deck presentation discipline in `puda-opentrons-vision-validation`, generalized to the selected machine's own workspace model. For every validation where deck/workspace boundaries can be resolved, return an annotated copy of the fresh image with a closed visible box around **every machine deck region in view**—not only the regions named by the protocol.

Here, “rectangle box” means a four-edge region outline. Use an axis-aligned rectangle only when the camera view and physical geometry support it. For a tilted camera, draw a perspective-aligned quadrilateral so the box follows the real deck boundaries instead of cutting across neighbouring regions.

Annotation rules:

1. Draw the full visible machine/deck outer boundary first.
2. Identify shared physical boundary intersections for all slots, zones, trays, stages, pans, channels, fixtures, or other addressable deck regions.
3. Build one shared lattice or boundary graph. Adjacent region boxes must reuse the same corner nodes and edges; do not estimate each box independently.
4. Draw one complete closed box for every visible deck region, covering the whole physical region from boundary to boundary without entering a neighbour.
5. Anchor boxes to the machine/deck structure, not to the footprint of the object currently occupying the region.
6. Label every box with the machine-native region name or identifier and its observed state.
7. Use **green** for `EMPTY`, **red** for `OCCUPIED`, **orange** for `OBSTRUCTED`, and **grey** for `NOT VISIBLE` when a region's expected location is known but cannot be inspected.
8. Include an on-image legend using the same colours. Keep the underlying scene visible with transparent fills or outline-only boxes.
9. Preserve the original unannotated evidence image separately from the annotated copy.
10. Independently inspect the final overlay. Reject and redraw it if a box clips its own region, crosses into a neighbour, follows an object's edge instead of the deck, omits a visible region, or obscures evidence needed for identity/occupancy checks.

For irregular workspaces, use a named polygon with the minimum vertices needed to follow the physical boundary rather than forcing an inaccurate four-corner box. If a boundary is occluded or cannot be calibrated, draw the known portion conservatively, label the region `NOT VISIBLE` or `OBSTRUCTED`, and keep the execution gate closed.

Completion criterion: the annotated image contains the machine/deck outer boundary, one correctly aligned and labelled box for every visible workspace region, a legend, and no missing, overlapping, or neighbour-crossing regions; the clean original remains available as evidence.

## Addressable Positions and Occupancy

When the user names a position:

1. Validate the coordinate against the exact machine/labware/fixture definition.
2. Establish physical orientation from a visible marker or authoritative cue.
3. Crop the full object, including edge rows/columns needed to count from the origin.
4. If needed, perspective-rectify the crop internally.
5. Do **not** draw a row/column grid over tips, wells, samples, or targets.
6. Count from the established origin and compare the requested position with its immediate neighbours in a clean crop.
7. Optionally add one small circle/arrow while retaining an unannotated crop.
8. Assign an explicit status: `present`, `absent`, `needs confirmation`, or `not visible`.

Do not infer one position's occupancy from general rack/tray fullness unless every position is individually visible and the conclusion is orientation-independent.

## Validation Workflow

### 1. Build the expected scene

List every machine, region, object, state, coordinate, and required-empty/keep-out area that affects the planned action.

Completion criterion: every physical precondition used by the workflow has a named expected observation or is explicitly classified as non-visual telemetry.

### 2. Capture fresh evidence

Use the selected machine profile's passive image source. If no passive path exists, determine whether the capture command can move or alter hardware and obtain approval when required.

Completion criterion: a fresh non-empty image exists with provenance, time, and hash.

### 3. Inspect conservatively

For each expected region/object/state, report visibility, occupancy/state, observed category or identity, confidence, and supporting visual cue. Compare exact identity with official references when geometry affects safe operation.

Create the required machine-deck box annotation after classifying the clean image. Do not let labels or overlays substitute for inspection of the original pixels.

Completion criterion: all expected regions plus unexpected occupied/obstructed/keep-out regions are covered, and every visible machine deck/workspace region has a verified closed annotation box.

### 4. Compare expected versus observed

Use:

| Status | Meaning |
|---|---|
| `OK` | Expected state is visible and supported with adequate confidence |
| `needs confirmation` | Region/state is visible but exact identity or condition is uncertain |
| `MISMATCH` | Visible state conflicts with expected state |
| `not visible` | Framing, pose, occlusion, or resolution prevents verification |
| `obstructed` | Another item prevents inspection or occupies a required clear region |

### 5. Gate execution

- Continue only when every required visual condition is `OK` and every non-visual safety prerequisite is separately satisfied.
- `needs confirmation`, `MISMATCH`, `not visible`, and `obstructed` keep the gate closed unless the user explicitly accepts the stated risk.
- A user correction applies only to the current image. If physical setup changes, capture again.
- Vision approval does not authorize robot execution; retain any separate protocol approval requirement.

## Output Format

Report:

1. **Environment, machine, and evidence** — active PUDA environment, machine ID, camera/pose, capture time, path/hash.
2. **Annotated machine/deck image** — attach the verified overlay with the outer boundary, one box per visible deck/workspace region, labels, states, and legend; retain the clean evidence image separately.
3. **Expected-vs-observed table** — region, expected, observed, confidence, status.
4. **Region summary** — concise occupied, empty, obstructed, and not-visible region lists, including unexpected observations.
5. **Coordinate checks** — requested position and occupancy/state, without a grid overlay.
6. **Non-visual prerequisites** — telemetry/calibration/interlocks that remain unverified.
7. **Gate decision** — pass, blocked, or needs confirmation.
8. **Execution statement** — explicitly state whether any machine command or motion occurred.

## Common Pitfalls

- Applying BEARS camera geometry, workspace polygons, identity confirmations, or credentials at IMRE/NTU (or vice versa).
- Applying OT-2 slots, A1 orientation, or labware rules to another machine.
- Moving an arm to improve the camera view during a validation-only request.
- Treating a camera image as proof of calibration, tare, electrical continuity, or telemetry freshness.
- Drawing boxes only around protocol-used regions instead of every visible machine deck/workspace region.
- Using axis-aligned rectangles on a tilted view, causing boxes to cross neighbouring regions; use perspective-aligned quadrilaterals.
- Drawing region boxes from object footprints instead of physical workspace outlines.
- Drawing a full coordinate grid over positions rather than inspecting a clean crop.
- Reusing old confirmations as evidence for a fresh scene.
- Reporting an exact object identity from colour alone.
- Passing a gate when the camera pose or workspace calibration is unknown.

## Verification Checklist

- [ ] Active PUDA environment read with `puda env current`.
- [ ] Matching environment machine skill loaded (`bears`, `imre`, `ntu`, or another configured environment).
- [ ] Exact environment-scoped machine profile selected.
- [ ] Expected physical scene extracted from the current request/protocol.
- [ ] Visual versus non-visual prerequisites separated.
- [ ] Passive capture used, or motion/state-changing capture separately approved.
- [ ] Fresh image path, time, size, hash, camera, and pose recorded.
- [ ] Full visible machine/deck outer boundary drawn on the annotated copy.
- [ ] Every visible deck/workspace region has one complete closed rectangle or perspective-aligned box.
- [ ] Physical regions aligned using shared perspective-aware boundaries and exact shared edges/corners.
- [ ] Every box covers its complete physical region without clipping it or entering a neighbour.
- [ ] Every box is labelled with the machine-native region identifier and observed state.
- [ ] Annotation uses green `EMPTY`, red `OCCUPIED`, orange `OBSTRUCTED`, and grey `NOT VISIBLE`, with an on-image legend.
- [ ] Annotated image independently rechecked; no visible region is omitted and no box follows an object's footprint.
- [ ] Clean unannotated evidence retained.
- [ ] No coordinate grid drawn over objects or positions.
- [ ] Every requested position validated against its exact definition and assigned a status.
- [ ] Expected and unexpected regions inspected.
- [ ] Current official machine references used.
- [ ] Gate closed for every uncertain, mismatched, obstructed, or invisible required condition.
- [ ] Final report states whether any command or motion occurred.
