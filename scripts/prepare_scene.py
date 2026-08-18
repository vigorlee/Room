#!/usr/bin/env python3
import os
from pathlib import Path

from pxr import Gf, Usd, UsdGeom, UsdPhysics


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = Path(
    os.environ.get("ISAACSIM_ASSET_ROOT", str(ROOT / "assets"))
).expanduser().resolve()
ROOM_ROOT = ASSET_ROOT / "Room_Mesh"
SOURCE_STAGE = ROOM_ROOT / "Scene.usd"
COMBINED_STAGE = ROOM_ROOT / "Room_With_Lightwheel.usda"
LIGHTWHEEL_ROOT = ASSET_ROOT / "Lightwheel_Samples"

PLACEMENTS = {
    "BaggedFood020": (Gf.Vec3d(-1.00, -2.40, 0.790), 12.0, 1.0),
    "BottledDrink034": (Gf.Vec3d(-0.76, -2.31, 0.870), -8.0, 1.0),
    "Pot079": (Gf.Vec3d(-0.48, -2.23, 0.815), 90.0, 1.0),
    "Toaster099": (Gf.Vec3d(-0.17, -2.23, 0.855), 0.0, 1.0),
    "Cart018": (Gf.Vec3d(-1.88, -2.95, 0.735), 12.0, 1.0),
}


def look_at(eye, target):
    view = Gf.Matrix4d().SetLookAt(eye, target, Gf.Vec3d(0.0, 0.0, 1.0))
    return view.GetInverse()


def define_camera(stage, path, eye, target, focal_length):
    camera = UsdGeom.Camera.Define(stage, path)
    camera.CreateFocalLengthAttr(focal_length)
    camera.CreateClippingRangeAttr(Gf.Vec2f(0.05, 1000.0))
    camera.AddTransformOp().Set(look_at(eye, target))


def build_combined_stage():
    if not SOURCE_STAGE.is_file():
        raise FileNotFoundError(SOURCE_STAGE)
    if COMBINED_STAGE.exists():
        COMBINED_STAGE.unlink()

    source = Usd.Stage.Open(str(SOURCE_STAGE), Usd.Stage.LoadAll)
    if not source:
        raise RuntimeError(f"cannot open Room_Mesh stage: {SOURCE_STAGE}")
    errors = source.GetCompositionErrors()
    if errors:
        raise RuntimeError(f"Room_Mesh source has composition errors: {errors}")

    stage = Usd.Stage.CreateNew(str(COMBINED_STAGE))
    stage.GetRootLayer().subLayerPaths = ["./Scene.usd"]
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)

    root = stage.GetPrimAtPath("/root")
    if not root.IsValid():
        raise RuntimeError("Room_Mesh default prim /root is missing")
    stage.SetDefaultPrim(root)

    # Clear the existing dining table so the four small assets remain visible.
    stage.OverridePrim("/root/CoffeeMachine094").SetActive(False)

    imported = UsdGeom.Xform.Define(stage, "/Lightwheel_Imported")
    for name, (position, yaw, scale) in PLACEMENTS.items():
        asset = LIGHTWHEEL_ROOT / name / f"{name}.usd"
        if not asset.is_file():
            raise FileNotFoundError(asset)
        prim = stage.DefinePrim(f"/Lightwheel_Imported/lightwheel_{name}", "Xform")
        prim.GetReferences().AddReference(
            f"../Lightwheel_Samples/{name}/{name}.usd"
        )
        xform = UsdGeom.Xformable(prim)
        xform.AddTranslateOp().Set(position)
        xform.AddRotateZOp().Set(yaw)
        xform.AddScaleOp().Set(Gf.Vec3d(scale, scale, scale))

    bag = stage.GetPrimAtPath(
        "/Lightwheel_Imported/lightwheel_BaggedFood020"
    )
    UsdPhysics.RigidBodyAPI.Apply(bag)
    UsdPhysics.MassAPI.Apply(bag).CreateMassAttr(0.2)
    bag_mesh = stage.GetPrimAtPath(
        "/Lightwheel_Imported/lightwheel_BaggedFood020/"
        "BaggedFood020/Visuals/BaggedFood020"
    )
    if not bag_mesh.IsA(UsdGeom.Mesh):
        raise RuntimeError("BaggedFood020 visual mesh is missing")
    UsdPhysics.CollisionAPI.Apply(bag_mesh)
    UsdPhysics.MeshCollisionAPI.Apply(bag_mesh).CreateApproximationAttr(
        "convexHull"
    )

    define_camera(
        stage,
        "/RoomOverviewCamera",
        Gf.Vec3d(0.95, -3.32, 1.60),
        Gf.Vec3d(-0.58, -2.42, 0.76),
        19.0,
    )
    define_camera(
        stage,
        "/AssetDetailCamera",
        Gf.Vec3d(0.42, -3.16, 1.32),
        Gf.Vec3d(-0.58, -2.34, 0.79),
        27.0,
    )

    stage.GetRootLayer().documentation = (
        "Non-destructive composition of Room_Mesh and five Lightwheel sample "
        "assets. The source Room_Mesh Scene.usd is preserved unchanged."
    )
    stage.GetRootLayer().Save()

    check = Usd.Stage.Open(str(COMBINED_STAGE), Usd.Stage.LoadAll)
    errors = check.GetCompositionErrors()
    if errors:
        raise RuntimeError(f"combined room stage has composition errors: {errors}")
    children = [child.GetName() for child in imported.GetPrim().GetChildren()]
    if len(children) != len(PLACEMENTS):
        raise RuntimeError(f"expected five imported assets, found {children}")


def main():
    build_combined_stage()
    print(f"ROOM_COMBINED stage={COMBINED_STAGE} assets={len(PLACEMENTS)}")
    for name, (position, yaw, scale) in PLACEMENTS.items():
        print(
            f"ROOM_PLACEMENT name={name} position={tuple(position)} "
            f"yaw={yaw:.1f} scale={scale:.2f}"
        )


if __name__ == "__main__":
    main()
