# Python 工程快速启动：uv 方式

> `uv` 是 Astral 团队（Ruff 同门）用 Rust 实现的极速 Python 包管理器，定位 ≈ pnpm for Python。

---

## 为什么选 uv？

| | pip + venv | Poetry | **uv** |
|---|---|---|---|
| 速度 | 🐢 慢 | 🐇 中 | 🚀 极快（Rust，并行下载） |
| 学习成本 | 低 | 中 | **低**（API 直观） |
| 锁文件 | ❌ 需手动 pip freeze | ✅ poetry.lock | ✅ uv.lock |
| 虚拟环境 | 手动创建激活 | 自动管理 | **自动管理 + 可选手动** |
| Python 版本管理 | 需 pyenv 配合 | 需 pyenv 配合 | **内置 `uv python`** |
| 工具管理 | 需 pipx | 需 pipx | **内置 `uv tool`** |
| CLI 风格 | 分散多工具 | 自成一体 | **统一 `uv` 前缀，像 npm/cargo** |

---

## 阶段 0：安装 uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或 Homebrew
brew install uv

# 验证
uv --version
# uv 0.x.x
```

---

## 阶段 1：创建项目

```bash
# 一条命令创建完整项目骨架
uv init my-python-project
cd my-python-project
```

自动创建的结构：

```
my-python-project/
├── .gitignore          ← 预配置（含 .venv/, __pycache__/）
├── .python-version     ← Python 版本声明（类似 .nvmrc）
├── pyproject.toml      ← 项目配置
├── README.md
└── hello.py            ← 示例入口文件
```

生成的 `pyproject.toml` 初始内容：

```toml
[project]
name = "my-python-project"
version = "0.1.0"
description = "Add your description here"
requires-python = ">=3.12"
dependencies = []
```

---

## 阶段 2：Python 版本管理（无需 pyenv）

```bash
# 查看已安装的 Python
uv python list

# 安装指定版本（自动下载）
uv python install 3.12
uv python install 3.11

# 切换项目 Python 版本
uv python pin 3.12          # 写入 .python-version
```

`uv python` 内置了 pyenv 的能力——管理 Python 版本不再需要额外工具。

---

## 阶段 3：虚拟环境（自动 or 手动）

### 自动模式（推荐，默认行为）

```bash
# uv 自动在 .venv/ 创建和管理虚拟环境
# 无需手动 python -m venv，无需 source activate
```

`uv run` 会自动检测或创建 `.venv/`，你几乎不用感知它的存在。

### 显式控制（可选）

```bash
# 手动创建
uv venv                     # 在 .venv/ 创建

# 指定 Python 版本创建
uv venv --python 3.12       # 使用 .python-version 或指定版本

# 自定义路径
uv venv my-env              # 在 my-env/ 创建

# 激活（如果习惯手动交互）
source .venv/bin/activate   # 仍然兼容传统方式
```

---

## 阶段 4：依赖管理

### 添加依赖

```bash
# 生产依赖
uv add requests
# → 下载 + 安装 + 更新 pyproject.toml + 更新 uv.lock

uv add "langchain>=1.0.0"
uv add chromadb pyyaml mcp

# 开发依赖（--dev / --group dev）
uv add --dev pytest
uv add --dev pytest-asyncio pytest-cov ruff mypy

# 可选依赖组
uv add --group docs mkdocs
uv add --group test pytest-xdist
```

### 删除依赖

```bash
uv remove requests
uv remove --dev pytest
```

### 安装全部依赖

```bash
uv sync                                     # 安装所有依赖
uv sync --no-dev                            # 仅生产依赖
uv sync --group dev --group docs            # 安装指定组
```

### pyproject.toml 变化示例

执行 `uv add requests` 后自动变成：

```toml
[project]
name = "my-python-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "requests>=2.32.3",
]

[dependency-groups]
dev = [
    "pytest>=8.3.5",
]
```

`uv.lock` 同时自动更新，锁定所有传递依赖的精确版本。

---

## 阶段 5：运行代码

### uv run（最常用）

```bash
# 运行脚本（自动确保 .venv 存在且依赖已安装）
uv run python main.py

# 运行模块
uv run python -m my_package.cli

# 运行测试
uv run pytest

# 运行任何已安装的命令行工具
uv run ruff check .
uv run mypy src/
```

`uv run` = `npm run` 的 Python 版。它自动处理：

1. 检查 `.venv/` 是否存在，不存在则创建
2. 检查依赖是否与 `uv.lock` 一致，不一致则提示 `uv sync`
3. 在该虚拟环境中执行命令

### 如果注册了 CLI 入口

```toml
[project.scripts]
mycli = "my_package.cli:main"
```

```bash
uv run mycli --help    # 直接调用
```

---

## 阶段 6：锁文件

```bash
# uv.lock 自动维护，通常不需要手动操作

# 更新所有依赖到最新兼容版本
uv lock --upgrade

# 更新特定包
uv lock --upgrade-package requests

# 仅重新生成锁文件，不安装
uv lock
```

`uv.lock`（类似 `package-lock.json`）记录精确版本，提交到 Git：

```bash
git add uv.lock
git commit -m "chore: update dependencies"
```

---

## 阶段 7：项目目录结构

```bash
uv init my-project
cd my-project
uv add langchain chromadb pyyaml mcp
uv add --dev pytest pytest-asyncio pytest-cov ruff
```

最终结构：

```
my-project/
├── .venv/                  ← 虚拟环境（自动管理，不提交 Git）
├── .gitignore              ← uv 生成，已忽略 .venv/
├── .python-version         ← Python 版本声明
├── pyproject.toml          ← 项目配置 + 依赖声明
├── uv.lock                 ← 精确锁文件（提交 Git）
├── README.md
├── main.py                 ← 入口
├── config/
│   └── settings.yaml
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── settings.py
│   └── services/
│       ├── __init__.py
│       └── api.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── unit/
    │   └── test_settings.py
    └── integration/
        └── test_api.py
```

---

## 阶段 8：额外能力

### 全局工具管理（替代 pipx）

```bash
# 安装全局工具
uv tool install ruff
uv tool install mypy
uv tool install pre-commit

# 运行工具
uv tool run ruff check .

# 列出/卸载
uv tool list
uv tool uninstall ruff
```

### 构建 & 发布

```bash
# 构建 wheel + sdist
uv build

# 发布到 PyPI
uv publish
```

---

## 完整速查：npm → uv 对照

| 动作 | npm | uv |
|---|---|---|
| 创建项目 | `npm init` | `uv init` |
| 安装 Python | nvm / 系统 | `uv python install 3.12` |
| 切换版本 | `nvm use 18` | `uv python pin 3.12` |
| 添加依赖 | `npm install pkg` | `uv add pkg` |
| 添加 dev 依赖 | `npm install -D pkg` | `uv add --dev pkg` |
| 删除依赖 | `npm uninstall pkg` | `uv remove pkg` |
| 安装全部 | `npm install` | `uv sync` |
| 运行脚本 | `npm run dev` | `uv run python main.py` |
| 运行测试 | `npm test` | `uv run pytest` |
| 锁文件 | `package-lock.json` | `uv.lock` |
| 更新依赖 | `npm update` | `uv lock --upgrade` |
| 全局工具 | `npm install -g pkg` | `uv tool install pkg` |
| 构建 | `npm run build` | `uv build` |

---

## pip 项目迁移到 uv（本项目为例）

```bash
# 1. 在项目根目录初始化 uv
cd /path/to/project
uv init --no-readme --no-pin            # 已有 pyproject.toml，不覆盖

# 2. 添加依赖（uv 读取现有 pyproject.toml）
uv add pyyaml langchain chromadb mcp

# 3. 添加 dev 依赖
uv add --dev pytest pytest-asyncio pytest-cov pytest-mock

# 4. 安装全部
uv sync

# 5. 把 .venv/ 加入 .gitignore（如未添加）
echo ".venv/" >> .gitignore

# 6. 运行测试验证
uv run pytest

# 7. 运行项目
uv run python main.py
```

迁移后的 `pyproject.toml` 对比：

```toml
# 迁移前（pip + setuptools）
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
dependencies = ["pyyaml>=6.0", ...]

[project.optional-dependencies]
dev = ["pytest>=8.0", ...]
```

```toml
# 迁移后（uv）
[project]
dependencies = ["pyyaml>=6.0", ...]

[dependency-groups]
dev = ["pytest>=8.0", ...]
```

主要变化：`[build-system]` 可去（uv 用 hatchling 替代 setuptools），`[project.optional-dependencies]` 变成 `[dependency-groups].dev`。

---

## 一条命令体验全部流程

```bash
# 从零到运行的 5 条命令
uv init demo-project && cd demo-project
uv add requests click pyyaml
uv add --dev pytest ruff
uv run python -c "import requests; print(requests.__version__)"
uv run pytest
```

这就是 uv 的设计哲学：**能用一条命令的绝不用两条，能自动的绝不手动**。

---

# 进阶：uv workspaces（Monorepo）

> `uv workspaces` 是 Python 原生 monorepo 方案，设计上对标 pnpm workspaces / Cargo workspaces。

---

## 为什么需要 Monorepo？

```
典型场景：一个项目拆成多个可复用的包

pnpm monorepo:
packages/
├── shared-utils/        ← pnpm-workspace.yaml 声明
├── api-server/          ← "shared-utils": "workspace:*"
└── web-frontend/        ← "shared-utils": "workspace:*"

Python 的等价方案：
packages/
├── shared-utils/        ← [tool.uv.workspace] 声明
├── api-server/          ← dependencies = ["shared-utils"]
└── cli-tool/            ← dependencies = ["shared-utils"]
```

---

## 目录结构

```
my-monorepo/
├── pyproject.toml          ← 根工作区配置（workspace root）
├── uv.lock                 ← 全局唯一锁文件（类似 pnpm-lock.yaml）
├── .python-version
├── .gitignore
│
├── packages/
│   ├── core/                       ← 基础库
│   │   ├── pyproject.toml
│   │   └── src/
│   │       └── my_core/
│   │           ├── __init__.py
│   │           ├── models.py
│   │           └── utils.py
│   │
│   ├── rag/                        ← RAG 引擎（依赖 core）
│   │   ├── pyproject.toml
│   │   └── src/
│   │       └── my_rag/
│   │           ├── __init__.py
│   │           ├── loader.py
│   │           └── retriever.py
│   │
│   └── mcp-server/                 ← MCP 服务（依赖 core + rag）
│       ├── pyproject.toml
│       └── src/
│           └── my_mcp_server/
│               ├── __init__.py
│               ├── server.py
│               └── tools.py
│
├── tests/
│   ├── unit/
│   └── integration/
│
└── tools/
    └── scripts/
        ├── pyproject.toml
        └── src/scripts/
            └── migrate.py
```

---

## 配置文件详解

### 根 `pyproject.toml`（workspace root）

```toml
[project]
name = "my-monorepo"
version = "0.1.0"
requires-python = ">=3.12"
# 根包不需要 dependencies，子包各自声明

[tool.uv.workspace]
members = ["packages/*", "tools/*"]

[tool.uv.sources]
# 声明工作区内哪些包是 workspace 成员
my-core = { workspace = true }
my-rag = { workspace = true }
my-mcp-server = { workspace = true }
my-scripts = { workspace = true }
```

| 字段 | 作用 | pnpm 对照 |
|---|---|---|
| `[tool.uv.workspace]` | 声明这是工作区根 | `pnpm-workspace.yaml` |
| `members` | glob 匹配子包目录 | `packages:` 列表 |
| `[tool.uv.sources]` | 标记哪些依赖来自工作区内部 | `workspace:*` 协议 |

### 子包 `packages/core/pyproject.toml`

```toml
[project]
name = "my-core"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "pydantic>=2.0",
    "pyyaml>=6.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### 子包 `packages/rag/pyproject.toml`

```toml
[project]
name = "my-rag"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "my-core",              # ← 引用工作区内其他包（无需路径、无需版本号）
    "langchain>=1.0.0",
    "chromadb>=0.5.0",
]
```

### 子包 `packages/mcp-server/pyproject.toml`

```toml
[project]
name = "my-mcp-server"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "my-core",              # ← 引用 core
    "my-rag",               # ← 引用 rag（传递依赖 core）
    "mcp>=1.0.0",
    "fastapi>=0.115",
]

[project.scripts]
mcp-serve = "my_mcp_server.server:main"

[dependency-groups]
dev = [
    "pytest>=8.0",
    "ruff>=0.5.0",
]
```

---

## 核心命令

```bash
# ========== 在任意子包目录下，uv 都会在根工作区上下文执行 ==========

# 安装全部子包依赖
uv sync

# 仅安装指定子包（--package 过滤）
uv sync --package my-core
uv sync --package my-mcp-server

# 给指定子包添加依赖
cd packages/rag
uv add "openai>=1.0"                    # 只加到 my-rag 的 dependencies

cd packages/mcp-server
uv add --dev pytest-mock                # 只加到 my-mcp-server 的 dev

# 运行指定子包的代码
uv run --package my-mcp-server python -m my_mcp_server.server
uv run --package my-rag pytest

# 构建全部子包
uv build --all

# 构建单个子包
uv build --package my-core
```

---

## pnpm workspaces ↔ uv workspaces 对照

| 动作 | pnpm | uv |
|---|---|---|
| 声明 workspace | `pnpm-workspace.yaml` | `[tool.uv.workspace]` |
| 内部依赖协议 | `"my-lib": "workspace:*"` | `"my-lib"` + `{ workspace = true }` |
| 安装全部 | `pnpm install` | `uv sync` |
| 给子包加依赖 | `pnpm add pkg --filter api` | `cd packages/api && uv add pkg` |
| 运行子包脚本 | `pnpm run build --filter api` | `uv run --package api python -m api` |
| 全局锁文件 | `pnpm-lock.yaml` | `uv.lock`（根级唯一） |
| 构建全部 | `pnpm -r build` | `uv build --all` |
| 运行测试 | `pnpm -r test` | 写脚本遍历，或 `uv run pytest` |

---

## 其他 Monorepo 方案一览

| 方案 | 类比 | 适用场景 |
|---|---|---|
| **uv workspaces** | pnpm workspaces | 中小型 monorepo，纯 Python |
| pip editable install | 手动 `npm link` | 小型项目，临时使用 |
| Poetry + path deps | yarn workspaces | 已用 Poetry 的团队 |
| Pantsbuild | Turborepo / Nx | 大型多语言 monorepo |
| Bazel | Turborepo / Nx | Google 级别巨型 monorepo |

---

## 迁移建议

```
当前项目（单仓 pip + setuptools）
  → 如果未来拆分多个子包（core / rag / mcp-server / cli）
    → 迁移到 uv workspaces

迁移步骤：
1. 删除旧的 [build-system] setuptools 配置
2. 添加 [tool.uv.workspace] 和 [tool.uv.sources]
3. 各子包创建独立 pyproject.toml
4. uv sync 生成全局 uv.lock
5. 各子包用 uv run --package xxx 运行
```

---

## 总结：uv 能力的完整图谱

```
uv（统一 CLI）
├── uv init              ← 创建项目（npm init）
├── uv python            ← Python 版本管理（nvm/pyenv）
├── uv venv              ← 虚拟环境（python -m venv）
├── uv add / remove      ← 依赖管理（npm install/uninstall）
├── uv sync              ← 安装依赖（npm install）
├── uv lock              ← 锁文件管理（package-lock.json）
├── uv run               ← 运行命令（npm run）
├── uv build / publish   ← 构建发布（npm publish）
├── uv tool              ← 全局工具（npx / pipx）
└── uv workspaces        ← 多包管理（pnpm workspaces）
```

一套工具覆盖 npm + nvm + pnpm 的全部能力，且 Rust 实现、秒级响应。
