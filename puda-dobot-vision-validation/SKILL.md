---
name: puda-dobot-vision-validation
description: Use before IMRE/MOF Dobot M1Pro pick, place, home, or transfer workflows when visible workspace setup and clearance must be checked. Capture a fresh passive IP-camera frame, verify the source, destination, gripper approach, transfer corridor, and neighbouring fixtures, and keep execution blocked when anything is mismatched, occluded, or uncertain.
version: 1.0.0
author: PUDAP
license: MIT
metadata:
  hermes:
    tags: [puda, dobot, vision-validation, ip-camera, physical-ai, imre]
    related_skills: [puda-robot-operations, lab-imaging-operations, imre-machines]
---

# PUDA Dobot Vision Validation

## Goal

Prevent `dobot-m1pro` motion in the IMRE/MOF cell when the visible physical setup does not support the requested transfer. Before a physical command, capture a fresh passive frame from the IMRE-MOF IP camera, inspect the clean pixels, annotate the Dobot-relevant regions, compare expected and observed state, and keep the execution gate closed when the source, destination, approach, corridor, or neighbouring equipment cannot be verified.

This is a **physical safety gate**, not motion authorization. It does not replace protocol validation, live PUDA state, measured robot pose, controller alarms, homing, collision limits, fixture calibration, equipment interlocks, or operator approval.

## When to Use

Use this skill before Dobot operations whose safety depends on visible setup, especially:

- `pick_from`, `place_to`, `safe_move`, or `home`
- tube transfers involving the 4 × 6 tube rack (`A1`–`D6`)
- BioShake positions (`A1`–`D6`)
- Centrifuge 1 or Centrifuge 2 positions (`1`–`6`)
- the CAP/QBot exchange region
- recovery after an interrupted or uncertain side-effecting action
- a validation-only request where no robot motion should occur

Do not use vision as proof that a coordinate is calibrated, a gripper contains a tube, a controller is alarm-free, or a centrifuge/BioShake is safe to access. Verify those separately.

## Critical Gate

Before any physical Dobot motion:

1. Identify the current site/project. Run `puda env current` when supported; on CLI versions without `env`, run `puda config list` and record the environment/site identity from the configured project context.
2. Confirm the exact machine ID is `dobot-m1pro` and query live state. A stale `idle` record is not readiness.
3. Extract the requested source, destination, addressable position, and required-clear path from the current request/protocol.
4. Capture a **fresh passive image** with [`scripts/capture_image.sh`](scripts/capture_image.sh). Do not move the camera or robot merely to obtain evidence unless separately approved.
5. Record the camera status/pose when available. The deployed reference pose is described in [`references/dobot-workspace-visual-identification.md`](references/dobot-workspace-visual-identification.md).
6. Inspect the clean image before drawing overlays.
7. Mark every visible Dobot-relevant region and classify source, destination, approach, corridor, neighbouring fixtures, and occlusions.
8. Compare expected and observed state.
9. Keep the gate closed unless every required visual condition is `OK` and all non-visual prerequisites independently pass.
10. Vision approval still does not authorize motion. Execute only after the user or approved workflow separately authorizes the robot command.

If a physical action was interrupted or timed out, do not replay it from the image alone. Treat its effect as unknown, reconstruct state from fresh image plus live machine evidence, and ask before executing a safe suffix.

## Deployed Machine and Camera Profile

| Field | Value |
|---|---|
| Site/environment | IMRE/MOF; confirm from current PUDA project/configuration |
| Machine ID | `dobot-m1pro` |
| Machine family | 4-axis Dobot M1Pro arm with tube gripper |
| Image source | Passive IMRE-MOF IP-camera stream configured at runtime with `DOBOT_VISION_RTSP_URL` |
| Camera ID | `imre-mof-ipcam` |
| Reference pose | PTZ status azimuth `74.9°`, elevation `57.3°`, zoom `1×` (camera units 749/573/10) |
| Calibration | No metric camera-to-robot calibration is established by this skill |
| Workspace model | Tube rack, BioShake, two centrifuges, CAP/QBot exchange region, Dobot base, and visible transfer corridor |
| Coordinate model | Robot coordinates and named positions are authoritative; image pixels are not robot coordinates |
| Safety gate | Any mismatch, uncertain identity, obstruction, clipped target, hidden gripper approach, or unverified corridor blocks motion |

Profile identity is `(IMRE/MOF, dobot-m1pro, imre-mof-ipcam, camera_pose)`. Region polygons and reference appearance are valid only when the fresh frame visibly matches the reference pose. Never transfer pixel coordinates, credentials, occupancy, or calibration to another camera or site.

## Dobot-Relevant Workspace Regions

| Region | Machine-native positions | Required visual checks |
|---|---|---|
| `TUBE-RACK` | `A1`–`D6` | full rack orientation, requested tube position, neighbouring clearance, no displaced tube |
| `BIOSHAKE` | `A1`–`D6` | target holder visible, BioShake not visibly obstructed, access path clear; live idle/interlock checked separately |
| `CENTRIFUGE-1` | slots `1`–`6` | rotor/holder and requested slot visible; lid/access and live stopped state checked separately |
| `CENTRIFUGE-2` | slots `1`–`6` | rotor/holder and requested slot visible; lid/access and live stopped state checked separately |
| `CAP-QBOT` | CAP exchange plus cap MTP `A1`–`D6` | exchange point visible, capper deck clear for robot access, no unexpected item in approach |
| `DOBOT-BASE` | fixed robot base | base and adjacent cables/fixtures visibly normal; never treat base occupancy as an obstruction |
| `TRANSFER-CORRIDOR` | safe-height arm travel between regions | no visible foreign object, raised lid, cable, fixture, or human intrusion; hidden portions remain unverified |
| `GRIPPER-APPROACH` | final vertical approach to source/destination | end effector and target approach visible enough to establish clearance |

The camera frame can be self-occluded by the arm. If the arm hides the target, gripper, CAP point, or travel corridor, classify it `not visible`; do not infer clearance from an earlier frame.

## Addressable Position Checks

For a requested position such as tube-rack `B2` or Centrifuge 2 slot `3`:

1. Validate the name against the current Dobot position definition.
2. Establish fixture orientation from physical geometry and a current authoritative reference.
3. Crop the complete parent fixture from the fresh image.
4. Keep a clean unannotated crop.
5. Inspect the requested position and its immediate neighbours.
6. Do not draw a full coordinate grid over tubes, centrifuge slots, BioShake positions, or cap wells.
7. Report one of:
   - `present` — required tube/object is clearly visible at the requested position;
   - `absent` — position is clearly visible and empty;
   - `needs confirmation` — position is localized but exact state/identity is uncertain;
   - `not visible` — framing, occlusion, reflection, or resolution prevents checking it.

Completion criterion: the named position is valid, fixture orientation is established, and the position has an evidence-based status. `needs confirmation` and `not visible` keep the gate closed.

## Vision Validation Workflow

### 1. Extract expected state

Record at minimum:

| Region/position | Expected object/state | Role | Required? |
|---|---|---|---|
| source | tube/object present and accessible | pick | yes |
| destination | empty or correctly prepared | place | yes |
| transfer corridor | clear | motion path | yes |
| neighbouring equipment | safe access state | interlock context | yes |

Also record the expected gripper state and all non-visual prerequisites.

Completion criterion: every physical precondition has a named expected observation or is explicitly classified as non-visual.

### 2. Capture fresh passive evidence

Configure a credential-free local MediaMTX/RTSP endpoint at runtime and run:

```bash
export DOBOT_VISION_RTSP_URL='rtsp://<configured-local-stream>/<path>'
./puda-dobot-vision-validation/scripts/capture_image.sh \
  /tmp/dobot-vision-$(date -u +%Y%m%dT%H%M%SZ).jpg
```

Record:

- UTC capture time from the host, not the camera overlay
- clean image path, size, dimensions, and SHA-256
- camera ID and measured PTZ pose/status when available
- whether capture was passive

The IMRE-MOF camera's on-image date/time overlay may be incorrect and must not be used as provenance.

Completion criterion: a fresh, valid, non-empty image exists with host UTC provenance and hash.

### 3. Inspect clean pixels conservatively

Before annotation, report:

- whether the entire requested source and destination fixtures are visible
- whether the requested position can be resolved
- whether the gripper approach is visible
- whether the visible transfer corridor is clear
- all unexpected occupied, displaced, raised, or obstructing objects
- all clipped, hidden, reflective, or ambiguous regions

Consult [`references/dobot-workspace-visual-identification.md`](references/dobot-workspace-visual-identification.md). Historical images support morphology and pose matching only; they never prove current occupancy.

Completion criterion: every required and unexpected region is classified without expectation-biased guessing.

### 4. Annotate and verify

Create an annotated copy while preserving the clean original. Draw:

- the visible cell/workspace boundary;
- one perspective-aligned polygon per relevant fixture/region;
- source and destination labels;
- `EMPTY`, `OCCUPIED`, `OBSTRUCTED`, or `NOT VISIBLE` state labels;
- a legend.

Use physical fixture boundaries, not the footprint of the occupying tube/object. Do not encode robot coordinates from image pixels. Independently inspect the annotated copy and reject overlays that clip targets, overlap unrelated fixtures, or obscure evidence.

The committed reference is [`assets/dobot-ipcamera-workspace-reference-annotated.jpg`](assets/dobot-ipcamera-workspace-reference-annotated.jpg). It is a pose/morphology example, not current-run evidence.

### 5. Compare expected and observed

| Region/position | Expected | Observed | Confidence | Status |
|---|---|---|---|---|
| source | required tube/object present | current visual observation | high/medium/low | `OK` / `needs confirmation` / `MISMATCH` / `not visible` |
| destination | prepared and accessible | current visual observation | high/medium/low | status |
| corridor | clear | current visual observation | high/medium/low | status |

Every required region gets exactly one status:

- `OK`: current pixels support the expected state with adequate confidence.
- `needs confirmation`: visible but exact state or identity is uncertain.
- `MISMATCH`: current state conflicts with the requested setup.
- `not visible`: framing or occlusion prevents verification.
- `obstructed`: an item or machine geometry blocks required inspection/access.

### 6. Gate execution

Continue only when:

- all required visual checks are `OK`;
- source and destination are both visible and consistent;
- gripper approach and visible corridor are clear;
- live machine states and equipment interlocks independently pass;
- robot pose/controller state is current;
- the user or approved workflow separately authorizes execution.

Any `needs confirmation`, `MISMATCH`, `not visible`, or `obstructed` result keeps the gate closed. A setup change requires a new image and a new independent validation.

## Output Format

Report:

1. **Profile and evidence** — site, machine, camera pose, host UTC, clean/annotated paths and hashes.
2. **Visibility summary** — source, destination, gripper approach, transfer corridor, and clipped/occluded regions.
3. **Expected-vs-observed table** — one status per required region/position.
4. **Non-visual prerequisites** — current machine state, measured pose, controller alarms, BioShake/centrifuge state, interlocks, and authorization.
5. **Gate decision** — `PASS`, `BLOCKED`, or `NEEDS CONFIRMATION`.
6. **Execution statement** — explicitly state whether any command or motion occurred.

## Current-Run Evidence Policy

Each validation is independent. Use only the current request/protocol, a fresh image, current machine/fixture definitions, and same-profile references for morphology. Never copy occupancy, tube presence, gripper state, clearance, or orientation from an earlier run.

The committed clean reference was captured passively on `2026-07-22T06:31:00Z` at camera status 749/573/10. It shows the cell from the reference pose but does not establish any later state. Its SHA-256 and limitations are recorded in the visual-identification reference.

## Common Pitfalls

- Using the camera's incorrect date/time overlay as capture time.
- Treating a broad overhead view as proof that the arm's full 3D swept volume is clear.
- Inferring a hidden source/destination behind the Dobot arm.
- Calling a tube position from rack occupancy without resolving the requested well.
- Treating visible centrifuge rotors as proof they are stopped or interlocked.
- Treating a visible BioShake as proof it is idle or unclamped.
- Using image pixels as robot coordinates or calibration.
- Reusing reference-image occupancy as current evidence.
- Automatically replaying an uncertain interrupted pick/place action.
- Moving the camera or robot merely to improve validation without separate approval.
- Executing because vision passed without separate motion authorization.

## Verification Checklist

- [ ] Current PUDA project/site identity recorded.
- [ ] Exact machine ID `dobot-m1pro` selected.
- [ ] Expected source, destination, position, gripper state, and corridor extracted.
- [ ] Fresh passive IP-camera image captured and hashed.
- [ ] Host UTC used; camera overlay time ignored.
- [ ] Camera pose/status recorded and compared with the reference pose.
- [ ] Clean image retained before annotation.
- [ ] Source and destination fixtures fully visible.
- [ ] Requested position directly inspected without a full grid overlay.
- [ ] Gripper approach and visible transfer corridor checked.
- [ ] Occlusions and unseen portions explicitly reported.
- [ ] Annotated image independently checked against clean pixels.
- [ ] Live robot pose/state and equipment interlocks verified separately.
- [ ] Gate closed for uncertainty, mismatch, obstruction, or invisibility.
- [ ] Final report states whether any command or motion occurred.
