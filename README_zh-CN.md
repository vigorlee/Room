# Isaac Sim Room 两套场景运行说明

这是一个面向 NVIDIA Isaac Sim 6.0.0.1 的运行代码仓库，包含
`Room_Mesh` 和 `Room_3DGS` 两套房间场景的组合、加载和验证脚本。
README 和运行代码上传到 GitHub；数 GB 的原始数据不
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

代码仓库为 public，但 `Room_Mesh.zip` 内没有许可证或来源说明。原始场景
数据不在普通代码 checkout 中；在确认授权和来源前，不要再分发原始数据。
五个独立物体资产使用 CC BY-NC 4.0，仅限非商业用途。

## 数据在哪里

数据不在 GitHub 仓库中。当前机器上的实际数据位置是：

```text
/home/unitree/isaacsim/assets/Room_Mesh
/home/unitree/isaacsim/assets/Room_3DGS
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
- Git
- Python 3.12 与 `venv`
- NVIDIA Isaac Sim 6.0.0.1（已有安装，或使用仓库内安装脚本）
- 至少 40 GiB 可用空间

## 安装和运行

### 1. 克隆代码仓库

```bash
git clone https://github.com/vigorlee/Room.git
cd Room
```

### 2. 确认本地数据

当前已验证的数据位于以下两个路径：

```text
/home/unitree/isaacsim/assets/Room_Mesh
/home/unitree/isaacsim/assets/Room_3DGS
```

运行前检查两个源场景文件：

```bash
test -f /home/unitree/isaacsim/assets/Room_Mesh/Scene.usd
test -f /home/unitree/isaacsim/assets/Room_3DGS/Scene.usd
```

两个目录的父目录还必须包含场景引用的 5 个独立物体 USD 资产。原始数据
不随 `git clone` 下载。

### 3. 安装或定位 Isaac Sim，并配置数据根目录

如果当前机器已经安装 Isaac Sim，使用：

```bash
export ISAACSIM_ASSET_ROOT=/home/unitree/isaacsim/assets
export ISAACSIM_PYTHON=/home/unitree/isaacsim/env/bin/python
export OMNI_KIT_ACCEPT_EULA=YES  # 阅读 NVIDIA EULA 后设置
```

如果尚未安装 Isaac Sim，仓库内提供安装脚本，会创建 `.venv` 并从 NVIDIA
软件源安装 Isaac Sim 6.0.0.1：

```bash
./scripts/install_isaacsim.sh
export ISAACSIM_PYTHON="$PWD/.venv/bin/python"
export ISAACSIM_ASSET_ROOT=/home/unitree/isaacsim/assets
export OMNI_KIT_ACCEPT_EULA=YES  # 阅读 NVIDIA EULA 后设置
```

其他机器只需替换 `ISAACSIM_PYTHON`，并将 `ISAACSIM_ASSET_ROOT` 指向同时
包含 `Room_Mesh/` 和 `Room_3DGS/` 的父目录。

可选环境检查：

```bash
test -x "$ISAACSIM_PYTHON"
"$ISAACSIM_PYTHON" -c 'import isaacsim; print("Isaac Sim Python: OK")'
```

### 4. 验证两套场景

```bash
ISAACSIM_ASSET_ROOT=/home/unitree/isaacsim/assets \
  "$ISAACSIM_PYTHON" scripts/verify_scenes.py
```

预期输出两个 `SCENE_VERIFY PASS`，并且两套场景的
`composition_errors=0`。

### 5. 启动场景

启动网格房间：

```bash
./start_room_mesh.sh
```

启动 NuRec 房间：

```bash
./start_room_3dgs.sh
```

需要特写视角时，在命令后加 `--camera detail`。启动脚本会在外部数据目录
下生成组合 USDA 层，不修改原始场景。首次启动 NuRec 场景需要等待初始化，
不建议同时运行两个 Isaac Sim 实例。

当前结论：

| 项目 | Room_Mesh | Room_3DGS |
|---|---|---|
| 最终组合错误 | 0 | 0 |
| 独立物体资产加载 | 5/5 | 5/5 |
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
| `scripts/open_scene.py` | 加载和验证 Room_Mesh |
| `start_room_3dgs.sh` | 启动 Room_3DGS，支持外部数据目录 |
| `scripts/prepare_room_3dgs.py` | 生成 3DGS/NuRec 组合层 |
| `scripts/open_room_3dgs.py` | 加载和验证 Room_3DGS |
| `scripts/verify_scenes.py` | 验证两套最终 Stage |
| `scripts/install_isaacsim.sh` | 创建虚拟环境并安装 Isaac Sim 6.0.0.1 |

## 外部数据目录结构

GitHub 仓库只包含运行代码，不包含大型原始数据。运行前需要准备以下目录：

```text
/home/unitree/isaacsim/assets/
├── Room_Mesh/
│   └── Scene.usd
├── Room_3DGS/
│   └── Scene.usd
└── <5 个被引用的独立物体 USD 资产>
```

启动脚本会在对应外部数据目录中生成最终组合 USDA 层，原始场景保持不变。
不要把未获授权的原始数据提交到这个 public 代码仓库。

详细来源与授权边界见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
