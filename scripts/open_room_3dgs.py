#!/usr/bin/env python3
import argparse
import os
import time
from pathlib import Path

import isaacsim
from isaacsim import SimulationApp


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = Path(
    os.environ.get("ISAACSIM_ASSET_ROOT", str(ROOT / "assets"))
).expanduser().resolve()
STAGE = ASSET_ROOT / "Room_3DGS/Room_3DGS_With_Lightwheel.usda"
EXPERIENCE = (
    Path(isaacsim.__file__).resolve().parent
    / "apps/isaacsim.exp.base.python.kit"
)
NUREC_PRIM = "/World/Room001_Fix/gauss/gauss"
CAMERAS = {
    "overview": "/World/LightwheelOverviewCamera",
    "detail": "/World/LightwheelDetailCamera",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Open the Room_3DGS NuRec scene in Isaac Sim."
    )
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--screenshot", type=Path)
    parser.add_argument("--camera", choices=CAMERAS, default="overview")
    parser.add_argument("--exit-after", type=float, default=0.0)
    parser.add_argument("--settle-seconds", type=float, default=25.0)
    args = parser.parse_args()
    if args.exit_after < 0 or args.settle_seconds < 0:
        parser.error("timing arguments must be non-negative")
    return args


args = parse_args()
if not STAGE.is_file():
    raise SystemExit(f"Room_3DGS stage is missing: {STAGE}")

app = SimulationApp(
    {
        "headless": args.headless,
        "hide_ui": args.headless,
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
            return
    raise TimeoutError("Room_3DGS stage loading timed out")


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
if not context.open_stage(str(STAGE)):
    raise RuntimeError(f"failed to open Room_3DGS stage: {STAGE}")
wait_for_load(context)
stage = context.get_stage()
if not stage:
    raise RuntimeError("Room_3DGS stage did not open")

nurec = stage.GetPrimAtPath(NUREC_PRIM)
if not nurec or not nurec.GetAttribute("omni:nurec:isNuRecVolume").Get():
    raise RuntimeError(f"NuRec volume is missing: {NUREC_PRIM}")
field = stage.GetPrimAtPath(NUREC_PRIM + "/density_field")
nurec_file = field.GetAttribute("filePath").Get() if field else None
if not nurec_file:
    raise RuntimeError("NuRec field data path is missing")

viewport = omni.kit.viewport.utility.get_active_viewport()
if not viewport:
    raise RuntimeError("no active viewport")
viewport.set_active_camera(CAMERAS[args.camera])
context.get_selection().set_selected_prim_paths([], True)
update_for(args.settle_seconds)

errors = stage.GetCompositionErrors()
imported = stage.GetPrimAtPath("/World/Lightwheel_Imported")
assets = [child.GetName() for child in imported.GetChildren()]
if len(assets) != 5:
    raise RuntimeError(f"expected five Lightwheel assets, found {assets}")
print(
    f"ROOM_3DGS_OPEN stage={context.get_stage_url()} "
    f"camera={viewport.get_active_camera()} nurec={nurec_file} "
    f"assets={assets} composition_errors={len(errors)}",
    flush=True,
)
for error in errors:
    print(f"ROOM_3DGS_COMPOSITION_WARNING {error}", flush=True)

if args.screenshot:
    output = capture(args.screenshot)
    print(f"ROOM_3DGS_SCREENSHOT file={output}", flush=True)

if args.exit_after:
    update_for(args.exit_after)
elif not (args.headless and args.screenshot):
    while app.is_running():
        app.update()
app.close(wait_for_replicator=False)
