# Isaac Sim Room Scenes

This repository provides a non-destructive NVIDIA Isaac Sim 6.0.0.1
runtime for two room scenes and five independent Sim-Ready object assets:
`BaggedFood020`, `BottledDrink034`, `Pot079`, `Toaster099`, and `Cart018`.

The repository contains the runnable composition and viewer code, README files,
verification code, and Room_Mesh evidence screenshots. The large source data
is intentionally kept outside GitHub and is supplied through
`ISAACSIM_ASSET_ROOT`.

For `Room_Mesh`, the four small assets are placed on the kitchen dining table
and the cart is placed on the floor to its left. The composition layer only
deactivates the table's original `CoffeeMachine094` to prevent overlap. The
source scene is not modified.

For `Room_3DGS`, the five assets are overlaid on the NuRec room visual. The
original furniture is baked into the Gaussian data and is not independently
draggable. The composition layer disables one optional missing payload from the
source stage so the final combined stage opens with zero composition errors.

## Repository visibility

The supplied `Room_Mesh.zip` contains no license or source notice. This
repository and its data-bearing Release are therefore private. Do not make the
Release public until redistribution permission for Room_Mesh is documented.
The five independent object assets are CC BY-NC 4.0 and are restricted to
non-commercial use.

The source data is not committed to this repository. On the current working
machine it is located at:

```text
/home/unitree/isaacsim/assets/Room_Mesh
/home/unitree/isaacsim/assets/Room_3DGS
/home/unitree/isaacsim/assets
```

`Room_Mesh` can also be downloaded from the private v1.0.0 Release using
`scripts/download_assets.sh`. `Room_3DGS` is not included in that Release and
must be supplied separately through `ISAACSIM_ASSET_ROOT`.

## Requirements

- Ubuntu 22.04 x86_64
- Vulkan-capable NVIDIA GPU with at least 16 GiB VRAM recommended
- Python 3.12 with `venv`
- GitHub CLI, unzip, and zstd (`sudo apt install gh unzip zstd`)
- At least 40 GiB free disk space

## Reproduce

Authenticate with a GitHub account that can access this private repository:

```bash
gh auth login
gh repo clone vigorlee/Room
cd Room
./scripts/download_assets.sh
./scripts/install_isaacsim.sh
export OMNI_KIT_ACCEPT_EULA=YES  # only after reviewing NVIDIA's EULA
./start_room_mesh.sh
```

To use an existing Isaac Sim 6.0.0.1 installation:

```bash
export OMNI_KIT_ACCEPT_EULA=YES
ISAACSIM_PYTHON=/path/to/isaacsim/python ./start_room_mesh.sh
```

## Use the existing local data directory

The current machine already has both scene data sets under
`/home/unitree/isaacsim/assets`. Set the data and Isaac Sim Python paths before
running either scene:

```bash
export ISAACSIM_ASSET_ROOT=/home/unitree/isaacsim/assets
export ISAACSIM_PYTHON=/home/unitree/isaacsim/env/bin/python
export OMNI_KIT_ACCEPT_EULA=YES  # after reviewing NVIDIA's EULA
```

The launchers generate the combined USDA layer in the external data directory
when it does not already exist, so the original source scenes remain unchanged.

### Room_Mesh

```bash
./start_room_mesh.sh
./start_room_mesh.sh --camera detail
./start_room_mesh.sh --headless --camera overview \
  --screenshot room-mesh-overview.png --exit-after 1
```

### Room_3DGS

```bash
./start_room_3dgs.sh
./start_room_3dgs.sh --camera detail
./start_room_3dgs.sh --headless --camera overview \
  --screenshot room-3dgs-overview.png --settle-seconds 30
```

If `ISAACSIM_ASSET_ROOT` is not set, both launchers use the repository-local
`assets/` directory. This is useful after downloading the Room_Mesh release,
but the Room_3DGS files still need to be supplied separately.

## Validate and capture

```bash
python3 scripts/verify_package.py

export OMNI_KIT_ACCEPT_EULA=YES
./start_room_mesh.sh --headless --camera overview \
  --screenshot room-overview.png --exit-after 1
./start_room_mesh.sh --headless --camera detail \
  --screenshot room-detail.png --exit-after 1
```

The existing Room_Mesh package validation passed: all source ZIP CRC checks, zero USD composition errors
in both source and combined stages, all five new asset references resolved, and
two non-black 1280 x 720 RTX renders with working materials and lighting. All
five assets retain valid rigid bodies and colliders; Cart018's eight joints and
Toaster099's four joints have no broken body targets.

To check the two final combined stages and their five imported asset nodes using
the external data directory:

```bash
ISAACSIM_ASSET_ROOT=/home/unitree/isaacsim/assets \
  "$ISAACSIM_PYTHON" scripts/verify_scenes.py
```

The expected result is `SCENE_VERIFY PASS` for both `Room_Mesh` and
`Room_3DGS`, with `composition_errors=0`.

## Runtime files

| File | Purpose |
|---|---|
| `start_room_mesh.sh` | Launch `Room_Mesh`; supports external data root |
| `scripts/prepare_scene.py` | Build the non-destructive Room_Mesh composition |
| `scripts/open_scene.py` | Open, validate, and capture Room_Mesh |
| `start_room_3dgs.sh` | Launch `Room_3DGS`; supports external data root |
| `scripts/prepare_room_3dgs.py` | Build the non-destructive NuRec composition |
| `scripts/open_room_3dgs.py` | Open, validate NuRec, and capture Room_3DGS |
| `scripts/verify_scenes.py` | Structural check for both final stages |

## Current validation summary

| Item | Room_Mesh | Room_3DGS |
|---|---|---|
| Final combined stage | Generated USDA layer | Generated USDA layer |
| Imported assets | 5/5 | 5/5 |
| Final composition errors | 0 | 0 |
| Render output | 1280×720 overview/detail | 1280×720 overview/detail |
| Imported asset transforms | Translate/rotate/scale | Translate/rotate |
| Room furniture independently draggable | Yes, USD hierarchy | No, baked into NuRec visual |
| Best use | Physics and interaction | Realistic display and vision |

Known limitation: `Room_3DGS/Scene.usd` by itself references an optional local
payload named `MilkDrink014_clean_particle_asset` that is not present. The
Room_3DGS composition layer disables this payload; the final combined stage is
the supported entry point and has zero composition errors.

## Release data

The original Room_Mesh ZIP is 2,454,033,960 bytes and extracts to about 4.4 GiB.
It is split into 1,572,864,000-byte and 881,169,960-byte Release assets to stay
below GitHub's 2 GiB per-file limit. The downloader reassembles and verifies the
original archive SHA-256:

```text
0be5acc7fe75d1982decd9c4f934c79e32b8c183cfc3928bd1d5b82819e1babc
```

The generated main stage is written under the selected data directory:

```text
assets/Room_Mesh/<generated-combined-stage>.usda
```

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for provenance and license
boundaries.
