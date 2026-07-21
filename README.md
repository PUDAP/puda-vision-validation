# puda-vision-validation

Reusable PUDA vision-validation skills for BEARS, IMRE, NTU, and future PUDA environments.

## Skills

| Skill | Purpose |
|---|---|
| `puda-machine-vision-validation` | Environment- and machine-neutral visual safety gate. Selects the active PUDA environment and machine profile, captures fresh evidence, validates machine-native regions/objects/states, and blocks uncertain or mismatched physical execution. |
| `puda-opentrons-vision-validation` | Opentrons OT-2 adapter for deck semantics, labware identification, pipette mounts, trash, and requested tip/well positions. Camera calibration and current-scene evidence remain scoped to the active site. |

The generic skill supports `bears`, `imre`, `ntu`, and future environments through their corresponding `<environment>-machines` skills. It does not transfer camera geometry, calibration, credentials, workspace polygons, or previous visual confirmations between sites.

## Install

Using PUDA:

```bash
puda skills install pudap/puda-vision-validation
```

Or using the skills CLI for Hermes Agent and Cursor:

```bash
npx skills add pudap/puda-vision-validation -g --agent hermes-agent cursor -y
```

## Safety principles

- Use the active environment from `puda env current`.
- Use a fresh image for every validation.
- Prefer passive capture; validation-only requests must not move hardware.
- Keep machine/camera profiles scoped by environment, machine ID, camera ID, and pose.
- Preserve clean unannotated evidence and do not draw coordinate grids over physical positions.
- Vision does not replace protocol validation, telemetry, calibration, interlocks, or operator approval.
