# Machine Workspace Visual-Identification Reference Template

Replace this file with target-machine references before deploying the copied skill. Do not use this unfilled template as evidence for physical execution.

## Reference Scope

| Field | Value |
|---|---|
| Environment | `<ENVIRONMENT>` |
| Machine ID | `<MACHINE_ID>` |
| Camera ID/pose | `<CAMERA_ID_AND_POSE>` |
| Workspace model version | `<VERSION/DATE>` |
| Maintainer | `<OWNER>` |

A reference is valid only for the stated environment, machine, camera, pose, and workspace version.

## Authoritative Sources

| Object/region | Source | Version/date | What it establishes |
|---|---|---|---|
| `<MACHINE DECK>` | `<OFFICIAL DRAWING/DOC>` | `<VERSION>` | `<BOUNDARIES/ORIENTATION>` |
| `<FIXTURE/LABWARE/TOOL>` | `<LIBRARY/DRIVER/DOC>` | `<VERSION>` | `<IDENTITY/GEOMETRY>` |

Prefer official machine drawings, driver definitions, fixture CAD, manufacturer libraries, visible labels, and current project records. Record user confirmation only when official evidence cannot establish the visible category.

## Workspace Boundary Model

### Outer boundary

- Physical cues: `<CORNERS/RAILS/FRAME MARKERS>`
- Expected image shape: `<DESCRIPTION>`
- Calibration/homography: `<ID/PATH OR UNAVAILABLE>`

### Shared region nodes and edges

| Node/edge | Physical cue | Adjacent regions | Calibration source |
|---|---|---|---|
| `<NODE/EDGE>` | `<CUE>` | `<REGIONS>` | `<SOURCE>` |

Adjacent regions must reuse the same nodes/edges. Never calibrate each box independently from the occupying object's footprint.

## Object Identification

For each object category, document cues that are stable for the selected camera pose.

| Category | Positive cues | Confusable alternatives | Disambiguation | Gate if uncertain |
|---|---|---|---|---|
| `<CATEGORY>` | `<GEOMETRY/LABEL/OPENING/PATTERN>` | `<ALTERNATIVES>` | `<AUTHORITATIVE CUE>` | `needs confirmation` |

Classify observed morphology before comparing with the expected setup. Colour alone is insufficient for exact identity.

## User-Confirmed Same-Angle References

| Asset | SHA-256 | Capture/profile | Confirmed category | Permitted use |
|---|---|---|---|---|
| `<assets/file>` | `<HASH>` | `<TIME + PROFILE>` | `<CATEGORY>` | morphology comparison only |

Historical references never prove current occupancy, placement, orientation, or alignment.

## Addressable Positions

| Parent object | Position definition | Orientation marker | Valid range | Visual limitation |
|---|---|---|---|---|
| `<FIXTURE/RACK>` | `<OFFICIAL DEFINITION>` | `<A1/ORIGIN/CUE>` | `<RANGE>` | `<RESOLUTION/OCCLUSION>` |

Do not draw a full coordinate grid over the image. Use a clean complete crop, establish orientation, and inspect the requested position directly.

## Known Optical Artifacts

- `<REFLECTION / TRANSPARENT LID / CABLE / SHADOW>`: `<HOW TO RECOGNIZE AND REPORT>`

Artifacts must not be silently treated as occupancy or emptiness.

## Reference Verification Checklist

- [ ] Environment, machine, camera, and pose are explicit.
- [ ] Every exact identity claim has an authoritative source or scoped user confirmation.
- [ ] Workspace boundaries use physical deck cues, not object footprints.
- [ ] Shared nodes/edges are documented for adjacent regions.
- [ ] Confusable alternatives and conservative fallback statuses are listed.
- [ ] Historical images are limited to morphology comparison.
- [ ] No credentials or secret connection strings are present.
- [ ] No current occupancy is encoded as a standing convention.
