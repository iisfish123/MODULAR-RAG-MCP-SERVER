# Python 包管理 vs npm 对照指南

> 当前项目（MODULAR-RAG-MCP-SERVER）使用 `pyproject.toml` + `pip` + `setuptools`，即 Python 官方标准方案。

---

## 📦 对照表

| npm 生态 | Python 生态 | 说明 |
|---|---|---|
| `package.json` | **`pyproject.toml`** | PEP 621 标准，当前项目正是这个 |
| `npm install` | `pip install -e .` | 安装当前项目依赖 |
| `npm install --save-dev` | `pip install -e ".[dev]"` | 安装开发依赖 |
| `package-lock.json` | `poetry.lock` / `uv.lock` | 锁文件（取决于使用的工具） |
| `node_modules/` | `site-packages/`（在虚拟环境内） | 依赖存放目录 |
| `npx` | `pipx` | 临时运行某个包 |
| npm registry | PyPI (`pypi.org`) | 中央包仓库 |

---

## 🔧 主要工具对比

### 当前使用：`pyproject.toml` + `pip` + `setuptools`

这是 Python 官方标准方案，最基础但功能有限：
- ✅ 声明依赖（`pyproject.toml` 中 `[project]` 块）
- ✅ 安装依赖（`pip install -e .`）
- ❌ 没有锁文件（无法锁定依赖版本）
- ❌ 没有内置依赖解析器

### 主流替代方案

| 工具 | 类比 | 特点 |
|---|---|---|
| **Poetry** | ≈ npm / yarn | 最成熟的 npm 风格工具，自带锁文件、依赖解析、发布流程 |
| **uv** | ≈ pnpm | Astral 出品（Ruff 同门），Rust 实现，极快，势头最猛 |
| **PDM** | ≈ yarn | PEP 582 标准实现，也支持虚拟环境 |

---

## 📄 `pyproject.toml` 结构解析（以本项目为例）

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]       # 构建工具声明
build-backend = "setuptools.build_meta"

[project]
name = "modular-rag-mcp-server"                 # 包名
version = "0.1.0"                                # 版本号
requires-python = ">=3.11"                       # Python 版本要求
dependencies = [                                  # 生产依赖（≈ dependencies）
    "pyyaml>=6.0",
    "langchain>=1.0.0",
    "chromadb>=0.5.0",
    "mcp>=1.0.0",
]

[project.optional-dependencies]
dev = [                                           # 开发依赖（≈ devDependencies）
    "pytest>=8.0",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=5.0.0",
    "pytest-mock>=3.14.0",
]
```

- `[project].dependencies` → npm 的 `dependencies`
- `[project.optional-dependencies].dev` → npm 的 `devDependencies`

---

## 🚀 常用命令速查

| 操作 | npm | Python (pip) |
|---|---|---|
| 安装全部依赖 | `npm install` | `pip install -e .` |
| 含开发依赖 | `npm install`（默认含） | `pip install -e ".[dev]"` |
| 安装单个包 | `npm install pkg` | `pip install pkg` |
| 卸载包 | `npm uninstall pkg` | `pip uninstall pkg` |
| 列出已安装 | `npm ls` | `pip list` |
| 运行脚本 | `npm run test` | `pytest`（直接调用） |
| 查看过时包 | `npm outdated` | `pip list --outdated` |
