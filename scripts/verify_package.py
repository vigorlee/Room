#!/usr/bin/env python3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "assets/Room_Mesh/Scene.usd",
    "assets/Room_Mesh/HDRI002.hdr",
    "assets/Room_Mesh/Assets/Floor001/Floor001.usd",
    "assets/Room_Mesh/Assets/Table121/Table121.usd",
    "assets/Lightwheel_Samples/BaggedFood020/BaggedFood020.usd",
    "assets/Lightwheel_Samples/BottledDrink034/BottledDrink034.usd",
    "assets/Lightwheel_Samples/Cart018/Cart018.usd",
    "assets/Lightwheel_Samples/Pot079/Pot079.usd",
    "assets/Lightwheel_Samples/Toaster099/Toaster099.usd",
    "assets/Lightwheel_Samples/LICENSE.txt",
    "assets/ASSET_PROVENANCE.txt",
    "screenshots/room-with-lightwheel-overview.png",
    "screenshots/room-with-lightwheel-detail.png",
)


missing = [relative for relative in REQUIRED if not (ROOT / relative).is_file()]
if missing:
    for relative in missing:
        print(f"MISSING {relative}")
    raise SystemExit(1)

room_files = sum(1 for path in (ROOT / "assets/Room_Mesh").rglob("*") if path.is_file())
if room_files < 389:
    raise SystemExit(f"Room_Mesh is incomplete: expected at least 389 files, found {room_files}")

print(f"PACKAGE_VERIFY PASS required_files={len(REQUIRED)} room_files={room_files}")
