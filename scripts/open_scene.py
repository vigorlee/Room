#!/usr/bin/env python3
import argparse
import time
from pathlib import Path

import isaacsim
from isaacsim import SimulationApp


ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "assets/Room_Mesh/Room_With_Lightwheel.usda"
EXPERIENCE = (
    Path(isaacsim.__file__).resolve().parent
    / "apps/isaacsim.exp.base.python.kit"
)
CAMERAS = {
    "overview": "/RoomOverviewCamera",
    "detail": "/AssetDetailCamera",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Open Room_Mesh with five Lightwheel sample assets."
    )
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--screenshot", type=Path)
    parser.add_argument("--camera", choices=CAMERAS, default="overview")
    parser.add_argument("--exit-after", type=float, default=0.0)
    args = parser.parse_args()
    if args.exit_after < 0:
        parser.error("--exit-after must be non-negative")
    return args


args = parse_args()
if not STAGE.is_file():
    raise SystemExit(
        "Combined room stage is missing. Run scripts/prepare_room_mesh.py first."
    )

app = SimulationApp(
    {
        "headless": args.headless,
        "hide_ui": args.headless,
        "open_usd": str(STAGE),
        "renderer": "RaytracedLighting",
        "sync_loads": True,
        "multi_gpu": False,
        "width": 1280,
        "height": 720,
        "window_width": 1440,
        "window_height": 900,
    },
    experience=str(EXPERIENCE),
)

import omni.kit.viewport.utility  # noqa: E402
import omni.usd  # noqa: E402


def update_for(seconds):
    deadline = time.monotonic() + seconds
    while app.is_running() and time.monotonic() < deadline:
        app.update()


def wait_for_load(context, timeout=300.0):
    deadline = time.monotonic() + timeout
    while app.is_running() and time.monotonic() < deadline:
        app.update()
        _, _, remaining = context.get_stage_loading_status()
        if remaining == 0:
            update_for(8.0)
            return
    raise TimeoutError("Room_Mesh stage loading timed out")


def capture(path, timeout=120.0):
    viewport = omni.kit.viewport.utility.get_active_viewport()
    if not viewport:
        raise RuntimeError("no active viewport")
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    omni.kit.viewport.utility.capture_viewport_to_file(
        viewport, file_path=str(path)
    )
    deadline = time.monotonic() + timeout
    while app.is_running() and time.monotonic() < deadline:
        app.update()
        if path.exists() and path.stat().st_size > 0:
            update_for(1.0)
            return path
    raise TimeoutError(f"viewport capture timed out: {path}")


context = omni.usd.get_context()
wait_for_load(context)
stage = context.get_stage()
if not stage:
    raise RuntimeError("Room_Mesh stage did not open")
errors = stage.GetCompositionErrors()
if errors:
    raise RuntimeError(f"Room_Mesh composition errors: {errors}")

viewport = omni.kit.viewport.utility.get_active_viewport()
if not viewport:
    raise RuntimeError("no active viewport")
viewport.set_active_camera(CAMERAS[args.camera])
context.get_selection().set_selected_prim_paths([], True)
update_for(12.0)

imported = stage.GetPrimAtPath("/Lightwheel_Imported")
assets = [child.GetName() for child in imported.GetChildren()]
if len(assets) != 5:
    raise RuntimeError(f"expected five Lightwheel assets, found {assets}")
print(
    f"ROOM_OPEN stage={context.get_stage_url()} camera={args.camera} "
    f"assets={assets} composition_errors={len(errors)}",
    flush=True,
)

if args.screenshot:
    output = capture(args.screenshot)
    print(f"ROOM_SCREENSHOT file={output}", flush=True)

if args.exit_after:
    update_for(args.exit_after)
else:
    while app.is_running():
        app.update()
app.close(wait_for_replicator=False)
