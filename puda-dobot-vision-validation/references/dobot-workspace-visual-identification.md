# IMRE/MOF Dobot Workspace Visual-Identification Reference

## Reference Scope

| Field | Value |
|---|---|
| Site/environment | IMRE/MOF; confirm from the current PUDA project/configuration |
| Machine ID | `dobot-m1pro` |
| Camera ID | `imre-mof-ipcam` |
| Reference camera status | azimuth 749, elevation 573, absolute zoom 10 (`74.9°`, `57.3°`, `1×`) |
| Reference resolution | 2560 × 1440 |
| Clean reference capture | `assets/dobot-ipcamera-workspace-reference.jpg` |
| Annotated reference | `assets/dobot-ipcamera-workspace-reference-annotated.jpg` |
| Host capture time | `2026-07-22T06:31:00Z` (derived from file capture time) |
| Workspace model version | 2026-07-22 initial IMRE/MOF profile |
| Calibration status | visual profile only; no metric homography or camera-to-robot calibration |

This reference is valid only for the stated site, machine, camera, pose, and resolution. A fresh image must visibly match the pose before the polygons can be used as presentation guidance. The image is never current-run occupancy evidence.

## Reference Integrity

| Asset | SHA-256 | Permitted use |
|---|---|---|
| `assets/dobot-ipcamera-workspace-reference.jpg` | `0cae1dcfe13a7e9f6f369a91105de84788eb883dfda64d3882a2463c29120587` | same-pose morphology, framing, and clean-pixel comparison only |
| `assets/dobot-ipcamera-workspace-reference-annotated.jpg` | `fc0ce5f9fd78e825147595520f854127e75375ecb4b0c0ea75d4ce82790e0d6a` | annotation/presentation example only |

The camera's embedded overlay displays an incorrect 1970 date/time. Use host UTC, file metadata, and SHA-256 for provenance; never use the overlay timestamp.

## Authoritative Sources

| Object/region | Source | What it establishes |
|---|---|---|
| Dobot commands | live `puda machine commands dobot-m1pro` | current command names and parameters |
| Dobot named positions | current environment-scoped `imre-machines` Dobot reference and deployed driver configuration | robot-coordinate definitions for tube rack, BioShake, centrifuges, and CAP |
| Cap MTP | current environment-scoped `imre-machines` QBot/capper reference | `A1`–`D6` cap positions |
| Live machine state | `puda machine state dobot-m1pro` plus controller/edge evidence | current software state and freshness; not physical clearance |
| Camera pose | current camera status endpoint or approved PTZ CLI | azimuth, elevation, and zoom at capture |

Image polygons are not an authoritative coordinate source. Never derive a robot target from the annotated asset.

## What the Reference Frame Shows

The clean reference frame visibly contains:

- the Dobot M1Pro body and arm in the center, creating substantial self-occlusion;
- a left-side 4 × 6 transfer-tube rack with multiple visible tubes/caps;
- the BioShake region in the lower-left quadrant with a holder/plate visibly present;
- two circular centrifuge/rotor regions along the lower-center edge;
- the CAP/QBot region at right with tube/cap holders and a white machine enclosure;
- the upper-left handling/deck area and surrounding cell frame;
- a broad overhead view of the cell, but not a guaranteed view of the full 3D swept volume.

The lower and upper frame edges clip parts of the physical enclosure. The Dobot arm hides portions of the central transfer corridor and CAP/QBot approach. Therefore the reference itself would not pass a run-specific clearance gate without fresh target-specific evidence.

## Workspace Boundary Model

### Outer visible boundary

The white outline in the annotated asset is a presentation boundary for the visible cell/workspace. It follows enclosure/deck cues near the frame perimeter. It is not a calibrated safety fence, collision envelope, or robot reach limit.

### Pose-specific annotation regions

The following image coordinates apply only to the 2560 × 1440 reference pose. They exist to regenerate the example overlay through `scripts/annotate_reference.py`.

| Region | Reference polygon (pixels) | Reference-frame state | Limitation |
|---|---|---|---|
| `TUBE-RACK` | `(806,748) (1014,735) (1024,1030) (802,1045)` | occupied | exact well orientation and tube identity require a clean crop |
| `BIOSHAKE` | `(525,790) (795,775) (820,1260) (510,1265)` | occupied | polygon is a broad fixture region, not a plate-coordinate calibration |
| `CENTRIFUGE-1` | `(1000,955) (1300,950) (1315,1380) (984,1380)` | occupied | partly clipped near lower frame; stopped/interlocked state is non-visual |
| `CENTRIFUGE-2` | `(1300,940) (1655,920) (1664,1380) (1315,1380)` | occupied | partly clipped near lower frame; stopped/interlocked state is non-visual |
| `CAP-QBOT` | `(1580,500) (2075,500) (2110,1155) (1555,1155)` | not fully visible | Dobot body/arm hides part of the approach and exchange area |
| `DOBOT BODY` | `(1090,0) (1840,0) (1840,370) (1525,960) (1160,960) (1075,280)` | fixed/occluding | follows visible body broadly; not a kinematic envelope |
| `TRANSFER-CORRIDOR` | `(820,265) (1685,230) (1905,1190) (760,1215)` | partly hidden | conceptual visible corridor only; not a planned trajectory |

Do not apply these polygons if the camera pose, zoom, resolution, crop, or enclosure geometry changes. Recalibrate visually and retain the clean evidence.

## Region Identification

### Tube rack (`A1`–`D6`)

Positive cues:

- rectangular dark holder;
- four-by-six position pattern;
- small cylindrical tubes/caps at approximately uniform pitch;
- located left of the Dobot body in the reference pose.

Confusable alternatives include other multi-position racks and neighbouring tip/plate holders. Establish orientation from the current position definition and visible fixture cues before resolving a named well. Colour alone is insufficient.

### BioShake (`A1`–`D6`)

Positive cues:

- dark instrument body in the lower-left workspace;
- holder/plate area above the instrument;
- `BioShake` marking may be visible near the lower edge in the reference frame.

Vision can establish visible occupancy and obstruction, not clamp state, temperature, shaking state, or safe-access interlocks. Query live state separately.

### Centrifuge 1 and Centrifuge 2 (`1`–`6`)

Positive cues:

- two adjacent circular rotor/holder regions along the lower-center workspace;
- six positions arranged at roughly 60-degree intervals around each rotor;
- distinct left/right fixture locations in the reference pose.

The image cannot prove a rotor is stationary, unlocked, homed, balanced, or safe for robot access. Require current machine state/interlock evidence. If the requested slot or lid/access area is clipped, report `not visible`.

### CAP/QBot exchange and cap MTP (`A1`–`D6`)

Positive cues:

- right-side white machine enclosure;
- adjacent dark holders with regular cap/tube positions;
- orange/grey/blue caps visible in the reference frame.

The Dobot body hides part of this region at the reference pose. Do not treat visible rack occupancy as proof the CAP exchange point or gripper approach is clear. Exact cap-well identity requires current orientation evidence.

### Dobot body, gripper, and transfer corridor

The white Dobot body is fixed machine geometry but its arm and end effector can change pose. The body can hide fixtures, the gripper approach, and objects in the corridor. An orange corridor polygon in the example communicates the area that needs inspection; it is not a trajectory, safe-height model, or collision envelope.

If the requested target or final approach is behind the arm, gate as `not visible`. Do not move the robot solely to improve the view unless the user separately approves that motion under normal robot-safety procedures.

## Addressable Position Identification

| Parent fixture | Valid positions | Orientation requirement | Visual limitation |
|---|---|---|---|
| Tube rack | `A1`–`D6` | match the deployed rack definition and visible fixture orientation | caps/tubes can occlude neighbouring wells |
| BioShake | `A1`–`D6` | match the deployed holder definition | fixture may be partly clipped/covered; equipment state is non-visual |
| Centrifuge 1 | `1`–`6` | match current slot-1 cue and rotor orientation | lower edge and arm can obscure slots |
| Centrifuge 2 | `1`–`6` | match current slot-1 cue and rotor orientation | lower edge and arm can obscure slots |
| Cap MTP | `A1`–`D6` | match current QBot/cap MTP definition | exact region may be hidden by Dobot body |
| CAP exchange | named `CAP` position | target and vertical gripper approach must be visible | partial self-occlusion in the reference pose |

For any named position, preserve a complete clean crop of the parent fixture, establish orientation from an authoritative cue, and inspect the requested position directly. Do not overlay a full grid.

## Known Optical and Scene Limitations

- **Incorrect camera overlay time:** ignore it; use host UTC.
- **Dobot self-occlusion:** the white body/arm hides central and right-side areas.
- **Wide-angle perspective:** apparent pixel distances are not robot distances.
- **Reflections and highlights:** white robot surfaces and enclosure panels can wash out edges.
- **Frame clipping:** the lower fixture edges and parts of the enclosure are near or beyond the image border.
- **Similar rack patterns:** tube, cap, tip, and plate holders can be confused without shape/orientation evidence.
- **No depth proof:** an overhead frame cannot establish 3D clearance throughout a vertical-lateral-vertical motion path.

Artifacts and hidden regions must not be silently treated as empty or safe.

## Reference Verification Checklist

- [ ] Site, machine, camera ID, PTZ pose, resolution, and capture time are explicit.
- [ ] Clean and annotated hashes match the files.
- [ ] Reference frame is used only for same-pose morphology and annotation guidance.
- [ ] Current occupancy is never copied from the reference.
- [ ] Position identity comes from the current machine/fixture definition.
- [ ] Pixel polygons are never used as robot coordinates or collision geometry.
- [ ] Self-occluded and clipped regions are marked `not visible` or `obstructed`.
- [ ] BioShake and centrifuge safety states are verified through live non-visual evidence.
- [ ] Camera endpoint and credentials remain runtime-only and uncommitted.
