# PUDA Machine/Deck Vision-Validation Template

Use this template to create a site- and machine-scoped vision-validation record that follows the full-deck annotation discipline of `puda-opentrons-vision-validation` without importing OT-2 slot assumptions into other machines.

Replace every `<placeholder>` before use. Delete sections that genuinely do not apply, but do not omit a safety-relevant region or prerequisite.

## 1. Validation Scope

| Field | Value |
|---|---|
| Environment | `<output of puda env current>` |
| Machine ID | `<environment-scoped machine ID>` |
| Machine family | `<liquid handler / arm / centrifuge / balance / other>` |
| Validation purpose | `<planned workflow or validation-only request>` |
| Execution requested? | `<yes / no>` |
| Operator approval required? | `<yes / no; approval rule>` |

### No-execution boundary

- Passive image capture only: `<yes / no>`
- Capture can move or alter hardware: `<yes / no / unknown>`
- Separate capture-motion approval, if required: `<approval text and time / not granted>`
- Machine commands or motion performed during validation: `<none / list exact commands>`

## 2. Environment-Scoped Machine Profile

| Profile field | Value/source |
|---|---|
| Profile identity | `(<environment>, <machine-id>, <camera-id>, <camera-pose>)` |
| Environment machine skill | `<environment>-machines` |
| Image source | `<passive snapshot/stream or approved capture command; redact credentials>` |
| Camera ID | `<camera identifier>` |
| Camera pose | `<fixed pose name>` |
| Calibration/homography | `<identifier, version, date, or unavailable>` |
| Machine/deck outer boundary | `<authoritative source or calibration record>` |
| Workspace model | `<slots/zones/trays/stages/pans/channels/fixtures>` |
| Coordinate model | `<definition or not applicable>` |
| Identity references | `<official docs/library/project reference>` |
| Safety gate | `<conditions that block execution>` |

Do not reuse camera endpoints, geometry, calibration, box coordinates, identity confirmations, or occupancy from another environment, machine, camera, pose, or earlier validation.

## 3. Expected Physical Scene

List every workflow-relevant region plus every required-empty and keep-out region.

| Region | Expected object/state | Role | Required for execution? | Reference |
|---|---|---|---|---|
| `<region-id>` | `<expected item/state>` | `<source/destination/tool/clearance/etc.>` | `<yes/no>` | `<definition/document>` |
| `<region-id>` | `<EMPTY / expected item>` | `<keep-out/etc.>` | `<yes/no>` | `<definition/document>` |

### Requested addressable positions

| Parent region/object | Position | Valid definition | Orientation cue | Expected state |
|---|---|---|---|---|
| `<region/object>` | `<position>` | `<source>` | `<visible marker/source>` | `<present/absent/etc.>` |

## 4. Fresh Evidence

| Evidence field | Value |
|---|---|
| Capture UTC time | `<YYYY-MM-DDTHH:MM:SSZ>` |
| Capture provenance | `<passive endpoint or approved command>` |
| Clean image path | `<path>` |
| Clean image size | `<non-zero bytes>` |
| Clean image SHA-256 | `<sha256>` |
| Annotated image path | `<path>` |
| Annotated image SHA-256 | `<sha256>` |
| Crop/rectification/enhancement | `<none or exact operations on copies>` |

Never put camera passwords, tokens, or credential-bearing URLs in this record.

## 5. Machine/Deck Region Geometry

### Shared boundary nodes

Define one shared lattice or boundary graph from physical machine/deck boundaries. Adjacent regions must reuse the exact same nodes and edges.

| Node | Pixel coordinate `(x, y)` | Physical cue | Confidence |
|---|---:|---|---|
| `<N1>` | `<x, y>` | `<deck corner/intersection>` | `<high/medium/low>` |
| `<N2>` | `<x, y>` | `<deck corner/intersection>` | `<high/medium/low>` |

### Region boxes

Draw the full visible machine/deck outer boundary, then one closed box around **every visible deck/workspace region**, including regions not used by the protocol.

“Rectangle box” means a closed four-edge outline. Use an axis-aligned rectangle only for an orthogonal view; use a perspective-aligned quadrilateral for a tilted view. For genuinely irregular regions, use the minimum-vertex polygon that follows the physical boundary.

| Region | Box nodes/polygon | Label | Observed state | Colour | Overlay verified? |
|---|---|---|---|---|---|
| `<region-id>` | `<N1,N2,N3,N4>` | `<region-id>: EMPTY` | `EMPTY` | green | `<yes/no>` |
| `<region-id>` | `<N2,N5,N6,N3>` | `<region-id>: OCCUPIED` | `OCCUPIED` | red | `<yes/no>` |
| `<region-id>` | `<nodes>` | `<region-id>: OBSTRUCTED` | `OBSTRUCTED` | orange | `<yes/no>` |
| `<region-id>` | `<known/estimated nodes>` | `<region-id>: NOT VISIBLE` | `NOT VISIBLE` | grey | `<yes/no>` |

### Required overlay presentation

- Green outline/transparent fill: `EMPTY`
- Red outline/transparent fill: `OCCUPIED`
- Orange outline/transparent fill: `OBSTRUCTED`
- Grey outline/transparent fill: `NOT VISIBLE`
- Label every region with its machine-native identifier and state.
- Include an on-image legend.
- Keep the scene visible; do not cover evidence with opaque fills or oversized labels.
- Do not draw row/column grids over tips, wells, samples, or targets.
- Retain the clean image separately from the annotated copy.

## 6. Clean-Image Inspection

Classify the original pixels before relying on the overlay.

| Region | Visible? | Occupancy/state | Observed object/category | Supporting visual cue | Confidence |
|---|---|---|---|---|---|
| `<region-id>` | `<yes/no/partial>` | `<state>` | `<observed item>` | `<geometry/label/fixture cue>` | `<high/medium/low>` |

### Unexpected observations

| Region | Observation | Potential effect | Status |
|---|---|---|---|
| `<region-id>` | `<unexpected item/obstruction>` | `<collision/identity/visibility/etc.>` | `<MISMATCH/obstructed/needs confirmation>` |

## 7. Expected vs Observed

| Region | Expected | Observed | Confidence | Status |
|---|---|---|---|---|
| `<region-id>` | `<expected>` | `<observed>` | `<high/medium/low>` | `<OK/needs confirmation/MISMATCH/not visible/obstructed>` |

Status meanings:

- `OK`: expected state is visible and adequately supported.
- `needs confirmation`: visible, but identity or condition is uncertain.
- `MISMATCH`: visible state conflicts with the expected scene.
- `not visible`: framing, pose, occlusion, or resolution prevents verification.
- `obstructed`: an item prevents inspection or occupies a required clear region.

## 8. Addressable-Position Checks

Use a clean crop with orientation established from an authoritative cue. Do not add a full coordinate grid.

| Parent region/object | Requested position | Coordinate valid? | Orientation established? | Observed state | Status |
|---|---|---|---|---|---|
| `<region/object>` | `<position>` | `<yes/no>` | `<yes/no + cue>` | `<present/absent/etc.>` | `<OK/needs confirmation/not visible/MISMATCH>` |

Clean crop: `<path>`  
Optional small circle/arrow callout: `<path or none>`

## 9. Non-Visual Prerequisites

Vision does not prove protocol validity, homing, calibration, tare, electrical continuity, interlocks, telemetry freshness, temperature, RPM, or other machine state.

| Prerequisite | Verification source | Result |
|---|---|---|
| `<protocol/schema validation>` | `<command/result>` | `<pass/fail/unverified>` |
| `<machine telemetry/interlock>` | `<source>` | `<pass/fail/unverified>` |
| `<operator approval>` | `<record>` | `<granted/not granted/not required>` |

## 10. Region Summary

- Occupied: `<regions>`
- Empty: `<regions>`
- Obstructed: `<regions>`
- Not visible: `<regions>`
- Needs confirmation: `<regions>`
- Unexpected occupied/unsafe: `<regions>`

## 11. Gate Decision

**Decision:** `<PASS / BLOCKED / NEEDS CONFIRMATION>`

**Reason:** `<concise evidence-based explanation>`

Blocking conditions: `<none or exact list>`

Required correction/confirmation: `<none or exact action>`

If the user explicitly accepts a stated risk, record the exact risk, instruction, and timestamp here. A vision override does not replace separate authorization for physical execution.

## 12. Execution Statement

- Machine command or motion occurred during validation: `<no / yes: exact action>`
- Physical workflow executed: `<no / yes: run ID and result>`
- Final machine state: `<state/source/time or unverified>`

## Final Verification Checklist

- [ ] Active environment came from `puda env current`.
- [ ] Correct environment machine skill and exact machine profile were used.
- [ ] Fresh clean image has provenance, non-zero size, time, and SHA-256.
- [ ] Machine/deck outer boundary is drawn.
- [ ] Every visible deck/workspace region has a complete closed box or correct irregular polygon.
- [ ] Adjacent boxes share exact nodes/edges with no gaps or overlaps.
- [ ] No box clips its region, enters a neighbour, or follows an object's footprint.
- [ ] Every region box has a machine-native label and state colour.
- [ ] The annotated image includes the colour legend.
- [ ] Clean unannotated evidence is retained.
- [ ] Every expected and unexpected region was inspected from the clean image.
- [ ] Requested addressable positions were checked without a coordinate-grid overlay.
- [ ] Non-visual prerequisites were verified separately or marked unverified.
- [ ] Uncertain, mismatched, obstructed, or invisible required conditions keep the gate closed unless the exact risk is explicitly accepted.
- [ ] Gate decision and execution statement are explicit.
