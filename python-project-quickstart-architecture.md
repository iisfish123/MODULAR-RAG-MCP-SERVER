# Python 工程快速启动 & 架构流程指南

> 以本项目（MODULAR-RAG-MCP-SERVER）为实例，梳理从零到运行 Python 工程的完整架构流程。

---

## 先纠正一个概念：`activate` 不是解释器！

### `.venv/bin/activate` 到底做了什么？

```bash
source .venv/bin/activate
```

`activate` 是一个纯粹的 **shell 脚本**，它只做四件事（源码见 `.venv/bin/activate`）：

| 行号 | 做了什么 | 代码 |
|---|---|---|
| 49 | 设置 `VIRTUAL_ENV` 环境变量 | `export VIRTUAL_ENV='/path/to/.venv'` |
| 54 | **把 `.venv/bin` 插到 PATH 最前面** | `PATH="$VIRTUAL_ENV/bin:$PATH"` |
| 71 | 修改终端提示符前缀 | `PS1="(.venv) $PS1"` |
| 4-33 | 注册 `deactivate` 函数 | 反向恢复上述修改 |

**核心就一行**：
```bash
PATH="$VIRTUAL_ENV/bin:$PATH"   # ← 这就是激活的本质
```

激活后，当你输入 `python`，shell 在 PATH 中按顺序找，先找到 `.venv/bin/python`（符号链接），它启动时会自动把 `sys.prefix` 指向 `.venv/`，于是 `import` 就会去 `.venv/lib/python3.12/site-packages/` 找包。

### 角色分工图

```
┌─────────────────────────────────────────────────────┐
│  source .venv/bin/activate                          │
│  ├── 修改 PATH（把 .venv/bin 放最前面）              │
│  ├── 修改 PS1（终端提示符显示 (.venv)）              │
│  └── 注册 deactivate 函数                           │
│                                                     │
│  ↑ 这是"导航员"，告诉你该往哪走                       │
│                                                     │
│  .venv/bin/python3.12                               │
│  ├── 符号链接 → 系统 Python 解释器                   │
│  └── 启动时检查自身路径，设置 sys.prefix = .venv/     │
│                                                     │
│  ↑ 这是"司机"，真正执行 Python 代码                   │
└─────────────────────────────────────────────────────┘
```

---

## 完整架构流程：从零到运行

### 阶段 0：环境准备

#### 0.1 安装 Python

```bash
# macOS（推荐 pyenv 管理多版本）
brew install pyenv
pyenv install 3.12.13
pyenv global 3.12.13

# 或直接用 Homebrew
brew install python@3.12
```

#### 0.2 验证安装

```bash
python3.12 --version
# Python 3.12.13
```

---

### 阶段 1：创建项目骨架

```bash
# 第一步：建目录
mkdir my-python-project && cd my-python-project

# 第二步：初始化 Git
git init
echo ".venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
```

#### 目录结构选型

Python 社区两大流派：

| 流派 | 结构 | 适用场景 |
|---|---|---|
| **src layout** ✅ 本项目采用 | `src/mypackage/` | 正式项目、库、大型工程 |
| **flat layout** | 直接 `mypackage/` | 简单脚本、小工具 |

src layout 的优势：
- 强制以「已安装包」的视角 import（避免 import 当前目录的意外行为）
- `pip install -e .` 后测试和运行的行为与用户安装后完全一致

---

### 阶段 2：创建虚拟环境

```bash
# 在项目根目录创建 .venv
python3.12 -m venv .venv

# 目录结构
# .venv/
# ├── bin/           ← Python 解释器符号链接 + activate + pip
# │   ├── python → python3.12
# │   ├── python3 → python3.12
# │   ├── python3.12 → /opt/homebrew/.../python3.12
# │   ├── activate
# │   ├── pip
# │   └── ...
# ├── lib/
# │   └── python3.12/
# │       └── site-packages/   ← 所有依赖安装到这里
# ├── include/
# ├── pyvenv.cfg               ← 记录 home、版本、隔离策略
# └── share/
```

#### `pyvenv.cfg` 详解

```ini
home = /opt/homebrew/opt/python@3.12/bin
include-system-site-packages = false   ← false = 隔离模式，不碰系统全局包
version = 3.12.13
```

`include-system-site-packages = false` 是关键：**即使系统装了一堆全局包，这里也完全看不见**，真正实现依赖隔离。

---

### 阶段 3：激活虚拟环境

```bash
# 激活（必须 source，不能直接执行）
source .venv/bin/activate

# 终端提示符会变化
# (.venv) user@host ~/project $

# 验证当前用的是 .venv 里的 Python
which python
# → /path/to/project/.venv/bin/python

python -c "import sys; print(sys.prefix)"
# → /path/to/project/.venv
```

#### 激活 vs 不激活

```bash
# 方式 A：激活后使用（方便交互式开发）
source .venv/bin/activate
python main.py
pytest

# 方式 B：不激活，直接用解释器绝对路径（适合脚本/CI）
.venv/bin/python main.py
.venv/bin/pytest

# 方式 C：使用 pipx run / tox / nox（适合 CI）
```

**三种方式等价**，最终都是 `.venv/bin/python` 在运行，自然都找 `.venv/lib/.../site-packages/`。

---

### 阶段 4：编写 `pyproject.toml`

这是 Python 项目的 **声明式配置文件**，相当于 `package.json` + `tsconfig.json` + `.eslintrc` 等的集合体。

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-project"
version = "0.1.0"
description = "项目描述"
requires-python = ">=3.12"
dependencies = [
    "requests>=2.31.0",
    "click>=8.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24.0",
    "ruff>=0.5.0",
]

# 入口点（命令行工具）
[project.scripts]
mycli = "my_package.cli:main"

# 如果使用 src layout
[tool.setuptools.packages.find]
where = ["src"]
```

#### pyproject.toml 各段职责

| 段落 | npm 类比 | 作用 |
|---|---|---|
| `[build-system]` | 构建工具声明 | 告诉 pip 用什么构建（setuptools/flit/hatch） |
| `[project]` | `package.json` 核心字段 | 包名、版本、依赖、入口 |
| `[project.scripts]` | `"bin"` 字段 | 注册 CLI 命令 |
| `[tool.xxx]` | `tsconfig.json` 等 | 各工具的配置（pytest、ruff、mypy） |

---

### 阶段 5：安装依赖

```bash
# 安装生产依赖（从 pyproject.toml 读取）
pip install -e .

# -e 的含义：editable mode（开发模式）
# 不复制代码到 site-packages，而是创建指向 src/ 的符号链接
# 修改源码立即生效，无需重新安装

# 安装生产 + 开发依赖
pip install -e ".[dev]"

# 安装后 site-packages 里会多出：
# __editable__.my_project-0.1.0.pth  ← 指向 src/ 的路径文件
# requests/
# click/
# pytest/
# ...
```

#### 安装流程原理

```
pip install -e .
      │
      ▼
读取 pyproject.toml → [build-system] 确定构建后端
      │
      ▼
setuptools 读取 [project].dependencies
      │
      ▼
下载包到 pip 缓存 → 解压到 .venv/lib/.../site-packages/
      │
      ▼
创建 __editable__.*.pth 文件，指向项目 src/
```

---

### 阶段 6：编写代码

```
my-project/
├── .venv/              ← 虚拟环境（不提交 Git）
├── .gitignore
├── pyproject.toml      ← 项目配置
├── README.md
├── main.py             ← 入口文件
├── config/
│   └── settings.yaml   ← 配置文件
├── src/                ← 源代码（src layout）
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── api.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
└── tests/              ← 测试
    ├── __init__.py
    ├── conftest.py     ← pytest 共享 fixtures
    ├── unit/
    │   └── test_settings.py
    └── integration/
        └── test_api.py
```

---

### 阶段 7：运行项目

```bash
# 直接运行入口文件
python main.py

# 如果注册了 CLI 入口
mycli --help

# 等效于（pip install -e 后 CLI 命令自动可用）
python -m my_package.cli --help
```

---

### 阶段 8：运行测试

```bash
# 运行全部测试
pytest

# 仅单元测试
pytest tests/unit/ -v

# 带覆盖率报告
pytest --cov=src --cov-report=html

# 仅运行特定标记的测试
pytest -m unit
pytest -m "not slow"
```

---

### 阶段 9：退出虚拟环境

```bash
deactivate
# 自动恢复原始 PATH、原始 PS1
```

---

## 进阶：依赖锁定与多环境管理

仅靠 `pyproject.toml` 的不足是无法锁定传递依赖版本。不同时间 `pip install` 可能装到不同版本。

### 方案对比

| 工具 | 复杂度 | 锁文件 | 适用场景 |
|---|---|---|---|
| `pip freeze` | 低 | `requirements.txt` | 简单项目 |
| `pip-tools` | 中 | `requirements.in` → `requirements.txt` | 中等项目 |
| **Poetry** | 中 | `poetry.lock` | 正式项目（npm/yarn 体验） |
| **uv** | 低 | `uv.lock` | 追求性能（pnpm 体验，Rust 实现） |

### pip freeze（最简）

```bash
pip freeze > requirements.txt        # 锁定当前全部依赖
# 其他人用：
pip install -r requirements.txt      # 精确复现
```

### Poetry 工作流

```bash
poetry init                          # 交互式创建 pyproject.toml
poetry add requests                  # 添加依赖（自动更新 lock）
poetry add --group dev pytest        # 开发依赖
poetry install                       # 安装（lock 优先）
poetry run python main.py            # 在 venv 中运行
poetry run pytest                    # 在 venv 中运行测试
```

### uv 工作流（推荐，与 Ruff 同门）

```bash
uv init                             # 创建项目
uv add requests                     # 添加依赖
uv add --dev pytest                 # 开发依赖
uv run python main.py               # 自动创建/使用 .venv + 运行
uv run pytest                       # 运行测试
uv sync                             # 仅安装依赖（不运行）
```

---

## 完整生命周期速查表（npm 对照）

| 动作 | npm | Python (pip) |
|---|---|---|
| 创建项目 | `npm init` | 手动写 `pyproject.toml` 或用 `poetry init` / `uv init` |
| 创建虚拟环境 | 自动（`node_modules/`） | `python -m venv .venv` |
| 激活环境 | 无需激活 | `source .venv/bin/activate` |
| 安装依赖 | `npm install` | `pip install -e .` |
| 含 dev 依赖 | 默认都装 | `pip install -e ".[dev]"` |
| 添加新依赖 | `npm install pkg` | 手动编辑 `pyproject.toml` + `pip install -e .` |
| 添加 dev 依赖 | `npm install -D pkg` | 编辑 `[project.optional-dependencies].dev` |
| 运行项目 | `npm start` / `node .` | `python main.py` |
| 运行测试 | `npm test` | `pytest` |
| 锁定版本 | `package-lock.json` | `pip freeze > requirements.txt` 或 `poetry.lock` / `uv.lock` |
| 退出环境 | 无需（切换目录即可） | `deactivate` |

---

## 设计哲学差异总结

```
npm 思路：目录就是环境
  cd my-project/  →  node_modules/ 就在脚底下  →  开箱即用

Python 思路：解释器就是环境
  python3.12 -m venv .venv  →  创建独立解释器副本  →  显式激活  →  .venv/bin/python
```

| | npm / Node.js | Python |
|---|---|---|
| 隔离单位 | 目录（`node_modules/` 就近原则） | 解释器（`sys.prefix` 指向 `.venv/`） |
| 激活 | 无（自动） | 可选（手动 `source activate`） |
| 全局 vs 本地 | `-g` 标志 | 系统 site-packages vs .venv site-packages |
| 多版本共存 | nvm | pyenv |
| 包管理器 | npm / yarn / pnpm | pip / Poetry / uv / PDM |
