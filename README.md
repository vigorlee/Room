# Isaac Sim Room Scenes

This repository provides a non-destructive NVIDIA Isaac Sim 6.0.0.1
runtime for two room scenes and five independent Sim-Ready object assets:
`BaggedFood020`, `BottledDrink034`, `Pot079`, `Toaster099`, and `Cart018`.

The repository contains the runnable composition and viewer code, README files,
and verification code. The large source data
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

The code repository is public, but the supplied `Room_Mesh.zip` contains no
license or source notice. The source data is not included in the normal checkout;
do not redistribute it until its permission and provenance are documented.
The five independent object assets are CC BY-NC 4.0 and are restricted to
non-commercial use.

The source data is not committed to this repository. On the current working
machine it is located at:

```text
/home/unitree/isaacsim/assets/Room_Mesh
/home/unitree/isaacsim/assets/Room_3DGS
```

The parent directory `/home/unitree/isaacsim/assets` must also contain the five
referenced object USD assets. They are not committed to this repository.

## Requirements

- Ubuntu 22.04 x86_64
- Vulkan-capable NVIDIA GPU with at least 16 GiB VRAM recommended
- Git
- Python 3.12 with `venv`
- NVIDIA Isaac Sim 6.0.0.1, installed locally or through the included installer
- At least 40 GiB free disk space

## Installation and run

### 1. Clone the public code repository

```bash
git clone https://github.com/vigorlee/Room.git
cd Room
```

### 2. Confirm the local scene data

The verified data is already on the machine at these exact paths:

```text
/home/unitree/isaacsim/assets/Room_Mesh
/home/unitree/isaacsim/assets/Room_3DGS
```

Check both source stages before running:

```bash
test -f /home/unitree/isaacsim/assets/Room_Mesh/Scene.usd
test -f /home/unitree/isaacsim/assets/Room_3DGS/Scene.usd
```

The parent directory must also contain the five referenced object USD assets.
The source data is external to this repository and is not downloaded by
`git clone`.

### 3. Install or locate Isaac Sim and configure the data root

If Isaac Sim is already installed on this machine, use:

```bash
export ISAACSIM_ASSET_ROOT=/home/unitree/isaacsim/assets
export ISAACSIM_PYTHON=/home/unitree/isaacsim/env/bin/python
export OMNI_KIT_ACCEPT_EULA=YES  # after reviewing NVIDIA's EULA
```

If Isaac Sim is not installed, the repository includes an installer that creates
`.venv` and installs Isaac Sim 6.0.0.1 from NVIDIA's package index:

```bash
./scripts/install_isaacsim.sh
export ISAACSIM_PYTHON="$PWD/.venv/bin/python"
export ISAACSIM_ASSET_ROOT=/home/unitree/isaacsim/assets
export OMNI_KIT_ACCEPT_EULA=YES  # after reviewing NVIDIA's EULA
```

On another machine, replace `ISAACSIM_PYTHON` with that machine's Isaac Sim
Python executable. Keep `ISAACSIM_ASSET_ROOT` pointed at the parent directory
that contains both `Room_Mesh/` and `Room_3DGS/`.

Optional environment checks:

```bash
test -x "$ISAACSIM_PYTHON"
"$ISAACSIM_PYTHON" -c 'import isaacsim; print("Isaac Sim Python: OK")'
```

### 4. Verify both scenes

```bash
ISAACSIM_ASSET_ROOT=/home/unitree/isaacsim/assets \
  "$ISAACSIM_PYTHON" scripts/verify_scenes.py
```

Expected output contains two `SCENE_VERIFY PASS` lines and
`composition_errors=0` for both scenes.

### 5. Start a scene

Start the mesh scene:

```bash
./start_room_mesh.sh
```

Start the NuRec scene:

```bash
./start_room_3dgs.sh
```

Use `--camera detail` for the detail view. The launchers generate the combined
USDA layer under the selected external data directory and preserve the source
scenes. Do not run both Isaac Sim instances at the same time unless sufficient
GPU memory is available.

## Runtime files

| File | Purpose |
|---|---|
| `start_room_mesh.sh` | Launch `Room_Mesh`; supports external data root |
| `scripts/prepare_scene.py` | Build the non-destructive Room_Mesh composition |
| `scripts/open_scene.py` | Open and validate Room_Mesh |
| `start_room_3dgs.sh` | Launch `Room_3DGS`; supports external data root |
| `scripts/prepare_room_3dgs.py` | Build the non-destructive NuRec composition |
| `scripts/open_room_3dgs.py` | Open and validate Room_3DGS |
| `scripts/verify_scenes.py` | Structural check for both final stages |
| `scripts/install_isaacsim.sh` | Create a virtual environment and install Isaac Sim 6.0.0.1 |

## Current validation summary

| Item | Room_Mesh | Room_3DGS |
|---|---|---|
| Final combined stage | Generated USDA layer | Generated USDA layer |
| Imported assets | 5/5 | 5/5 |
| Final composition errors | 0 | 0 |
| Imported asset transforms | Translate/rotate/scale | Translate/rotate |
| Room furniture independently draggable | Yes, USD hierarchy | No, baked into NuRec visual |
| Best use | Physics and interaction | Realistic display and vision |

Known limitation: `Room_3DGS/Scene.usd` by itself references an optional local
payload named `MilkDrink014_clean_particle_asset` that is not present. The
Room_3DGS composition layer disables this payload; the final combined stage is
the supported entry point and has zero composition errors.

## External data layout

The GitHub repository contains code only. Before starting either scene, provide
the external data under this layout:

```text
/home/unitree/isaacsim/assets/
├── Room_Mesh/
│   └── Scene.usd
├── Room_3DGS/
│   └── Scene.usd
└── <five referenced object USD assets>
```

The launchers write their generated combined USDA layers inside the respective
external data directories. Keep the source data outside this public code
repository. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for provenance
and license boundaries.
