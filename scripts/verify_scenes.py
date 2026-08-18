#!/usr/bin/env python3
import os
from pathlib import Path

from pxr import Usd


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = Path(
    os.environ.get("ISAACSIM_ASSET_ROOT", str(ROOT / "assets"))
).expanduser().resolve()

SCENES = {
    "Room_Mesh": (
        ASSET_ROOT / "Room_Mesh/Room_With_Lightwheel.usda",
        "/Lightwheel_Imported",
    ),
    "Room_3DGS": (
        ASSET_ROOT / "Room_3DGS/Room_3DGS_With_Lightwheel.usda",
        "/World/Lightwheel_Imported",
    ),
}


def verify(name, stage_path, imported_path):
    if not stage_path.is_file():
        raise FileNotFoundError(stage_path)
    stage = Usd.Stage.Open(str(stage_path), Usd.Stage.LoadAll)
    if not stage:
        raise RuntimeError(f"failed to open {stage_path}")
    errors = stage.GetCompositionErrors()
    if errors:
        raise RuntimeError(f"{name} composition errors: {errors}")
    imported = stage.GetPrimAtPath(imported_path)
    if not imported:
        raise RuntimeError(f"{name} imported asset root is missing: {imported_path}")
    assets = [child.GetName() for child in imported.GetChildren()]
    if len(assets) != 5:
        raise RuntimeError(f"{name} expected five assets, found {assets}")
    print(
        f"SCENE_VERIFY PASS name={name} stage={stage_path} "
        f"assets={assets} composition_errors=0"
    )


for scene_name, (stage_path, imported_path) in SCENES.items():
    verify(scene_name, stage_path, imported_path)
