#!/usr/bin/env python3
import os
from pathlib import Path

from pxr import Gf, Usd, UsdGeom


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = Path(
    os.environ.get("ISAACSIM_ASSET_ROOT", str(ROOT / "assets"))
).expanduser().resolve()
ROOM_ROOT = ASSET_ROOT / "Room_3DGS"
SOURCE_STAGE = ROOM_ROOT / "Scene.usd"
COMBINED_STAGE = ROOM_ROOT / "Room_3DGS_With_Lightwheel.usda"
LIGHTWHEEL_ROOT = ASSET_ROOT / "Lightwheel_Samples"

# The four small assets rest on the scanned coffee-table surface at Z=0.426 m.
# Cart018 rests on the floor behind and to the left of the table.
PLACEMENTS = {
    "BaggedFood020": (Gf.Vec3d(-0.25, 0.08, 0.451), 12.0),
    "BottledDrink034": (Gf.Vec3d(0.06, 0.08, 0.525), -8.0),
    "Pot079": (Gf.Vec3d(-0.20, 0.45, 0.469), 0.0),
    "Toaster099": (Gf.Vec3d(0.13, 0.45, 0.508), 0.0),
    "Cart018": (Gf.Vec3d(-0.92, 1.00, 0.726), 8.0),
}


def look_at(eye, target):
    view = Gf.Matrix4d().SetLookAt(eye, target, Gf.Vec3d(0.0, 0.0, 1.0))
    return view.GetInverse()


def define_camera(stage, path, eye, target, focal_length):
    camera = UsdGeom.Camera.Define(stage, path)
    camera.CreateFocalLengthAttr(focal_length)
    camera.CreateClippingRangeAttr(Gf.Vec2f(0.03, 1000.0))
    camera.AddTransformOp().Set(look_at(eye, target))


def build_combined_stage():
    if not SOURCE_STAGE.is_file():
        raise FileNotFoundError(SOURCE_STAGE)
    if COMBINED_STAGE.exists():
        COMBINED_STAGE.unlink()

    stage = Usd.Stage.CreateNew(str(COMBINED_STAGE))
    stage.GetRootLayer().subLayerPaths = ["./Scene.usd"]
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)

    world = stage.GetPrimAtPath("/World")
    if not world:
        raise RuntimeError("Room_3DGS default prim /World is missing")
    stage.SetDefaultPrim(world)

    # The source contains an optional payload that is not present locally.
    missing = stage.OverridePrim("/World/MilkDrink014_clean_particle_asset")
    missing.SetActive(False)
    missing.GetPayloads().SetPayloads([])

    imported = UsdGeom.Xform.Define(stage, "/World/Lightwheel_Imported")
    for name, (position, yaw) in PLACEMENTS.items():
        asset = LIGHTWHEEL_ROOT / name / f"{name}.usd"
        if not asset.is_file():
            raise FileNotFoundError(asset)
        prim = stage.DefinePrim(
            f"/World/Lightwheel_Imported/lightwheel_{name}", "Xform"
        )
        prim.GetReferences().AddReference(
            f"../Lightwheel_Samples/{name}/{name}.usd"
        )
        xform = UsdGeom.Xformable(prim)
        xform.AddTranslateOp().Set(position)
        xform.AddRotateZOp().Set(yaw)

    define_camera(
        stage,
        "/World/LightwheelOverviewCamera",
        Gf.Vec3d(0.7713, -2.6871, 1.0583),
        Gf.Vec3d(0.05, 0.20, 0.48),
        18.0,
    )
    define_camera(
        stage,
        "/World/LightwheelDetailCamera",
        Gf.Vec3d(0.58, -1.58, 0.92),
        Gf.Vec3d(-0.05, 0.24, 0.47),
        27.0,
    )

    stage.GetRootLayer().documentation = (
        "Non-destructive composition of the Room_3DGS NuRec scene and five "
        "independently transformable Lightwheel sample assets."
    )
    stage.GetRootLayer().Save()

    check = Usd.Stage.Open(str(COMBINED_STAGE), Usd.Stage.LoadAll)
    if not check:
        raise RuntimeError(f"cannot open combined stage: {COMBINED_STAGE}")
    errors = check.GetCompositionErrors()
    if errors:
        raise RuntimeError(f"combined stage has composition errors: {errors}")
    children = list(
        check.GetPrimAtPath("/World/Lightwheel_Imported").GetChildren()
    )
    if len(children) != len(PLACEMENTS):
        raise RuntimeError(
            f"expected {len(PLACEMENTS)} imported assets, found {len(children)}"
        )


def main():
    build_combined_stage()
    print(f"ROOM_3DGS_COMBINED stage={COMBINED_STAGE} assets={len(PLACEMENTS)}")
    for name, (position, yaw) in PLACEMENTS.items():
        print(
            f"ROOM_3DGS_PLACEMENT name={name} position={tuple(position)} "
            f"yaw={yaw:.1f}"
        )


if __name__ == "__main__":
    main()
