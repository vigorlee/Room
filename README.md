# Room_Mesh with Five Lightwheel Assets

This repository provides a non-destructive NVIDIA Isaac Sim 6.0.0.1
composition of `Room_Mesh/Scene.usd` and five Lightwheel Sim-Ready assets:
`BaggedFood020`, `BottledDrink034`, `Pot079`, `Toaster099`, and `Cart018`.

The four small assets are placed on the kitchen dining table and the cart is
placed on the floor to its left. The composition layer only deactivates the
table's original `CoffeeMachine094` to prevent overlap. The source scene is not
modified.

## Repository visibility

The supplied `Room_Mesh.zip` contains no license or source notice. This
repository and its data-bearing Release are therefore private. Do not make the
Release public until redistribution permission for Room_Mesh is documented.
The five Lightwheel assets are CC BY-NC 4.0 and are restricted to
non-commercial use.

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
gh repo clone vigorlee/lightwheel-room-mesh-isaacsim-repro
cd lightwheel-room-mesh-isaacsim-repro
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

## Validate and capture

```bash
python3 scripts/verify_package.py

export OMNI_KIT_ACCEPT_EULA=YES
./start_room_mesh.sh --headless --camera overview \
  --screenshot room-overview.png --exit-after 1
./start_room_mesh.sh --headless --camera detail \
  --screenshot room-detail.png --exit-after 1
```

Local validation passed: all source ZIP CRC checks, zero USD composition errors
in both source and combined stages, all five new asset references resolved, and
two non-black 1280 x 720 RTX renders with working materials and lighting. All
five assets retain valid rigid bodies and colliders; Cart018's eight joints and
Toaster099's four joints have no broken body targets.

## Release data

The original Room_Mesh ZIP is 2,454,033,960 bytes and extracts to about 4.4 GiB.
It is split into 1,572,864,000-byte and 881,169,960-byte Release assets to stay
below GitHub's 2 GiB per-file limit. The downloader reassembles and verifies the
original archive SHA-256:

```text
0be5acc7fe75d1982decd9c4f934c79e32b8c183cfc3928bd1d5b82819e1babc
```

The generated main stage is:

```text
assets/Room_Mesh/Room_With_Lightwheel.usda
```

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for provenance and license
boundaries.
