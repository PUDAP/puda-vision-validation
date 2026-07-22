# puda-vision-validation

Reusable PUDA vision-validation skills for BEARS, IMRE, NTU, and future PUDA environments.

## Skills

| Skill | Purpose |
|---|---|
| `puda-opentrons-vision-validation` | Opentrons OT-2 adapter for deck semantics, labware identification, pipette mounts, trash, and requested tip/well positions. Camera calibration and current-scene evidence remain scoped to the active site. |
| `puda-dobot-vision-validation` | IMRE/MOF Dobot M1Pro adapter. Uses a fresh passive IP-camera frame to check tube-rack, BioShake, centrifuge, CAP/QBot, gripper-approach, and transfer-corridor conditions before separately authorized robot motion. Includes clean and annotated same-pose reference assets plus capture/annotation scripts. |
| `template` (`puda-machine-vision-validation-template`) | Copy-and-customize skill package for another user, environment, camera, or machine. Mirrors the Opentrons skill structure with a `SKILL.md`, annotated example under `assets/`, and machine-identification guidance under `references/`. |

The template supports creation of environment- and machine-specific skills without transferring camera geometry, calibration, credentials, workspace polygons, or previous visual confirmations between sites.

## Template skill package

Copy the [`template/`](template/) directory to create a vision-validation skill for another user, environment, or machine. Rename the copied directory and frontmatter `name`, replace every `<PLACEHOLDER>`, and install current machine/camera references before using it as a physical gate.

The package follows the `puda-opentrons-vision-validation` layout:

```text
template/
├── SKILL.md
├── assets/
│   └── machine-deck-region-annotation-example.svg
└── references/
    └── machine-workspace-visual-identification.md
```

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
