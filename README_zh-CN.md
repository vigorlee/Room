# Isaac Sim Room 两套场景运行说明

这是一个面向 NVIDIA Isaac Sim 6.0.0.1 的运行代码仓库，包含
`Room_Mesh` 和 `Room_3DGS` 两套房间场景的组合、加载、截图和验证脚本。
README、运行代码和 Room_Mesh 验证截图上传到 GitHub；数 GB 的原始数据不
上传，通过 `ISAACSIM_ASSET_ROOT` 从本地目录加载。

五个独立物体资产为：

- `BaggedFood020`
- `BottledDrink034`
- `Pot079`
- `Toaster099`
- `Cart018`

`Room_Mesh` 中四件小物品放在厨房餐桌上，推车放在餐桌左侧地面。为了避免
重叠，组合层只停用了原餐桌上的 `CoffeeMachine094`；源场景没有被修改。

`Room_3DGS` 中五件资产叠加到 NuRec 房间视觉层。原有沙发、电视、茶几等
已经烘焙进高斯数据，不能独立拖动；只有新增的 USD 资产可以独立选择和移动。

## 仓库可见性

`Room_Mesh.zip` 内没有许可证或来源说明，因此本仓库和包含原场景数据的
Release 保持为 private。确认 Room_Mesh 的公开再分发授权前，不应把 Release
改为 public。五个独立物体资产使用 CC BY-NC 4.0，仅限非商业用途。

## 数据在哪里

数据不在 GitHub 仓库中。当前机器上的实际数据位置是：

```text
/home/unitree/isaacsim/assets/Room_Mesh
/home/unitree/isaacsim/assets/Room_3DGS
/home/unitree/isaacsim/assets
```

规模和许可边界：

| 数据 | 规模 | 说明 |
|---|---:|---|
| `Room_Mesh` | 约 4.4 GiB，390 个文件 | 原始数据未公开授权，保持私有 |
| `Room_3DGS` | 约 642 MiB，20 个文件 | 包含 `Room001_Fix.usdz` 和 `111.nurec` |
| 独立物体资产 | 约 73 MiB，21 个文件 | CC BY-NC 4.0，仅限非商业使用 |

仓库代码默认从仓库内的 `assets/` 读取。使用当前机器的数据时设置：

```bash
export ISAACSIM_ASSET_ROOT=/home/unitree/isaacsim/assets
export ISAACSIM_PYTHON=/home/unitree/isaacsim/env/bin/python
export OMNI_KIT_ACCEPT_EULA=YES  # 阅读 NVIDIA EULA 后设置
```

如果在其他机器运行，只需把 `ISAACSIM_ASSET_ROOT` 指向包含
`Room_Mesh/`、`Room_3DGS/` 和独立物体资产目录。

## 环境要求

- Ubuntu 22.04 x86_64
- 支持 Vulkan 的 NVIDIA GPU，建议至少 16 GiB 显存
- Python 3.12 与 `venv`
- GitHub CLI、unzip 和 zstd：`sudo apt install gh unzip zstd`
- 至少 40 GiB 可用空间

## 一键复现

先用有权访问本私有仓库的 GitHub 账号登录：

```bash
gh auth login
gh repo clone vigorlee/Room
cd Room
./scripts/download_assets.sh
./scripts/install_isaacsim.sh
export OMNI_KIT_ACCEPT_EULA=YES  # 阅读并接受 NVIDIA EULA 后设置
./start_room_mesh.sh
```

已经安装 Isaac Sim 6.0.0.1 时可跳过安装：

```bash
export OMNI_KIT_ACCEPT_EULA=YES
ISAACSIM_PYTHON=/你的/isaacsim/python ./start_room_mesh.sh
```

## 运行两套场景

### Room_Mesh

```bash
./start_room_mesh.sh
./start_room_mesh.sh --camera detail
./start_room_mesh.sh --headless --camera overview \
  --screenshot room-mesh-overview.png --exit-after 1
```

组合场景：

```text
/home/unitree/isaacsim/assets/Room_Mesh/<generated-combined-stage>.usda
```

### Room_3DGS

```bash
./start_room_3dgs.sh
./start_room_3dgs.sh --camera detail
./start_room_3dgs.sh --headless --camera overview \
  --screenshot room-3dgs-overview.png --settle-seconds 30
```

组合场景：

```text
/home/unitree/isaacsim/assets/Room_3DGS/<generated-combined-stage>.usda
```

3DGS 视觉数据为：

```text
/home/unitree/isaacsim/assets/Room_3DGS/lcc-usdz-result/Room001_Fix.usdz
```

其中包含 `111.nurec`；碰撞代理为：

```text
/home/unitree/isaacsim/assets/Room_3DGS/mesh-files/Room001.usd
```

5 个新增 USD 物品可以独立选择、平移和旋转。原有沙发、电视、茶几等已经
烘焙进高斯视觉数据，不能像普通 USD 家具一样单独拖动。首次加载 Room_3DGS
需要等待 NuRec 初始化，不建议同时长期运行两个 Isaac Sim 实例。

## 截图和验证

```bash
python3 scripts/verify_package.py

export OMNI_KIT_ACCEPT_EULA=YES
./start_room_mesh.sh --headless --camera overview \
  --screenshot room-overview.png --exit-after 1
./start_room_mesh.sh --headless --camera detail \
  --screenshot room-detail.png --exit-after 1
```

本机验证结果：Room_Mesh 原包 CRC 全部通过；源 Stage 和组合 Stage 的 USD
composition errors 均为 0；组合 Stage 包含 3615 个源场景 Prim 和 5 件新资产；
RTX 两张截图均为 1280 x 720、非黑帧，材质和灯光正常。五件资产的刚体与
碰撞体均可解析，Cart018 的 8 个关节和 Toaster099 的 4 个关节没有失效引用。

两套最终组合 Stage 的验证命令：

```bash
ISAACSIM_ASSET_ROOT=/home/unitree/isaacsim/assets \
  "$ISAACSIM_PYTHON" scripts/verify_scenes.py
```

预期输出为两个 `SCENE_VERIFY PASS`，且 `composition_errors=0`。

当前结论：

| 项目 | Room_Mesh | Room_3DGS |
|---|---|---|
| 最终组合错误 | 0 | 0 |
| 独立物体资产加载 | 5/5 | 5/5 |
| 渲染结果 | 1280×720 概览/特写 | 1280×720 概览/特写 |
| 新增物品变换 | 平移/旋转/缩放 | 平移/旋转 |
| 原始房间家具是否可拆分 | 支持 USD 层级编辑 | 不支持，已烘焙进 NuRec |
| 推荐用途 | 物理、导航、碰撞、抓取 | 真实感展示、视觉感知 |

注意：`Room_3DGS/Scene.usd` 单独打开时会引用本地不存在的可选 payload
`MilkDrink014_clean_particle_asset`。组合脚本会禁用该 payload；实际运行应
使用生成的最终组合 USDA 场景。

## 运行代码清单

| 文件 | 作用 |
|---|---|
| `start_room_mesh.sh` | 启动 Room_Mesh，支持外部数据目录 |
| `scripts/prepare_scene.py` | 生成 Room_Mesh 组合层 |
| `scripts/open_scene.py` | 加载、验证和截图 Room_Mesh |
| `start_room_3dgs.sh` | 启动 Room_3DGS，支持外部数据目录 |
| `scripts/prepare_room_3dgs.py` | 生成 3DGS/NuRec 组合层 |
| `scripts/open_room_3dgs.py` | 加载、验证 NuRec 和截图 Room_3DGS |
| `scripts/verify_scenes.py` | 验证两套最终 Stage |
| `scripts/download_assets.sh` | 下载私有 Room_Mesh Release 资产 |

## 数据大小与校验

原始 Room_Mesh 压缩包为 2,454,033,960 字节，解压后约 4.4 GiB。由于超过
GitHub 单个 Release 附件 2 GiB 的上限，v1.0.0 分为 1,572,864,000 字节和
881,169,960 字节两个分卷；下载脚本会自动合并并核对原始 ZIP SHA-256：

```text
0be5acc7fe75d1982decd9c4f934c79e32b8c183cfc3928bd1d5b82819e1babc
```

主入口：

```text
assets/Room_Mesh/<generated-combined-stage>.usda
```

详细来源与授权边界见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
