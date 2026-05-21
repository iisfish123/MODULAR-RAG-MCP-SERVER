# Modular RAG MCP Server — Skill 架构与 SOP 分析

> 本文档对项目内置的全部 Agent Skill 进行系统性梳理，涵盖架构分层、触发机制、Pipeline 流程、输入输出协议，以及从零到交付的完整 Skill 工作流 SOP。

---

## 一、Skill 全局架构概览

项目当前共有 **9 个 Agent Skill**，分为三层，外加 1 个元工具（skill-creator）：

```
┌─────────────────────────────────────────────────────────┐
│                    元工具层 (Meta)                        │
│  skill-creator  ——  创建/更新/打包 Skill 的 Skill        │
└─────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                 工程执行层 (Engineering)                   │
│                                                          │
│  setup  ──→  auto-coder  ──→  qa-tester  ──→  package   │
│  (一键配置)   (自动开发)       (自动测试)      (清理打包)  │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                学习面试层 (Learning & Interview)          │
│                                                          │
│  project-learner  ──→  project-review  ──→  interview-prep│
│  (交互式学习)          (老师式复习)          (模拟面试)    │
│                                                          │
│                 resume-writer (简历生成)                  │
└──────────────────────────────────────────────────────────┘
```

### 1.1 部署位置

Skill 在两个目录下存在（内容镜像）：

| 目录 | 包含的 Skill | 用途 |
|------|-------------|------|
| `.github/skills/` | **全部 9 个** + skill-creator | 主目录，GitHub Copilot 读取 |
| `.claude/skills/` | auto-coder, qa-tester, resume-writer, skill-creator | 子集，Claude Desktop 读取 |

### 1.2 Skill 文件结构约定

每个 Skill 遵循统一的目录结构：

```
skill-name/
├── SKILL.md              # 核心文件：YAML frontmatter(name+description) + Markdown 指令
├── scripts/              # 可执行脚本（Python），用于确定性操作
│   └── *.py
└── references/           # 参考文档，Agent 按需加载
    └── *.md / *.yaml
```

关键设计理念：
- **Progressive Disclosure**：三层加载 → (1) name+description 始终在上下文 (~100字) → (2) SKILL.md body 在 Skill 触发后加载 (<5k字) → (3) references 按需加载
- **description 是主要触发机制**：Agent 通过正则/语义匹配 description 中的触发词决定是否激活 Skill

---

## 二、Skill 逐项详解

### 2.1 setup — 一键环境配置向导

| 属性 | 值 |
|------|-----|
| **触发词** | `setup` / `set up` / `configure` / `init project` / `初始化` / `环境配置` / `项目配置` / `first run` / `get started` / `quick start` |
| **定位** | 交互式配置向导，从空白代码库到可运行项目 |
| **核心能力** | Provider选择 → API Key配置 → 依赖安装 → 配置生成 → Dashboard启动 → 自动修复 |

#### Pipeline（7 步）

```
Preflight Checks → Ask User (3批次) → Scaffold Providers → Generate Config
→ Install Deps → Validate & Auto-Fix (≤3轮) → Launch Dashboard → Usage Guide
```

#### Step 1: Preflight Checks（前置检查）
- 检查 Python 版本 ≥ 3.10
- 检查/创建 `.venv` 虚拟环境
- 使用 `--without-pip` 加速创建，然后 `ensurepip --upgrade` 引导 pip

#### Step 2: Ask User（分 3 批交互）
- **Batch 1（核心 Provider）**：LLM Provider / Embedding Provider / Vision 是否启用 / Rerank 方案
- **Batch 2（凭据配置）**：基于 Batch 1 选择，询问对应 API Key、模型名称
- **Batch 3（Vision 凭据）**：Vision LLM 有独立配置段（`vision_llm`），不自动共享主 LLM 凭据

#### Step 2.5: Scaffold Unimplemented Providers
- 若用户选择了未内置的 Provider（如 Qwen、Gemini），自动生成代码骨架：
  1. 创建 `src/libs/llm/{name}_llm.py`（继承 `BaseLLM`）
  2. 创建 `src/libs/embedding/{name}_embedding.py`
  3. 创建 `src/libs/llm/{name}_vision_llm.py`
  4. 注册到工厂的 `__init__.py`
  5. 安装对应 SDK
- 多数 Provider 是 OpenAI-compatible，子类化 `OpenAILLM` + 覆写 `DEFAULT_BASE_URL` 即可

#### Step 5: Validate & Auto-Fix（自动修复循环）
```
Round 0..2:
  读取错误 → 诊断根因 → 修复 settings.yaml / 安装依赖 → 重新验证
  → 通过则继续 / 失败则下一轮
Round 3 仍失败 → 报告用户
```

#### 输入/输出

| 输入 | 输出 |
|------|------|
| 用户对话式选择 Provider 和凭据 | `config/settings.yaml`（完整配置） |
| | `.venv`（已安装所有依赖） |
| | 成功启动的 Dashboard（`localhost:8501`） |

---

### 2.2 auto-coder — 自动化 Spec 驱动开发

| 属性 | 值 |
|------|-----|
| **触发词** | `auto code` / `自动开发` / `自动写代码` / `auto dev` / `一键开发` / `autopilot` |
| **定位** | 从 DEV_SPEC 读取任务 → 编码 → 测试 → 持久化的全自动 Agent |
| **可选参数** | 任务 ID（如 `auto code B2`）、`--no-commit` |

#### Pipeline（5 步循环）

```
Sync Spec → Find Task → Implement → Test & Auto-Fix (≤3轮) → Persist
```

#### Step 1: Sync Spec
运行 `sync_spec.py` 将 `DEV_SPEC.md` 按章节拆分为 `references/` 下 7 个文件：
- `01-overview.md` — 项目概述
- `02-features.md` — 功能规格
- `03-tech-stack.md` — 技术栈
- `04-testing.md` — 测试约定
- `05-architecture.md` — 架构与模块设计
- `06-schedule.md` — 任务排期与进度
- `07-future.md` — 扩展路线

#### Step 2: Find Task（任务选择策略）
1. 优先选 `IN_PROGRESS` (`[~]`) 的任务
2. 其次选第一个 `NOT_STARTED` (`[ ]`) 的任务
3. 若用户指定了任务 ID，直接使用
4. 前置依赖检查：仅做文件级检查，不阻塞

#### Step 3: Implement（实现策略）
1. 读取对应 references 获取架构/技术栈/测试约定
2. 从 SPEC 提取：输入输出、设计原则、文件清单、验收标准
3. **先规划文件再写代码**
4. 编码规则：SPEC 为唯一事实源、使用 `config/settings.yaml` 值、匹配现有代码风格
5. 同步编写测试文件（`tests/unit/` 或 `tests/integration/`）
6. Unit 测试中 Mock 外部依赖

#### Step 4: Test & Auto-Fix（自动修复）
```
Round 0..2:
  pytest <target_test_file>
  通过 → 进入 Persist
  失败 → 分析错误 → 修复 → 重跑
Round 3 仍失败 → STOP，展示失败报告
```

#### Step 5: Persist（持久化）
1. 更新 `DEV_SPEC.md` 中任务标记 `[ ]` → `[x]`
2. 重新运行 `sync_spec.py --force`
3. 询问用户: `commit` / `skip` / `next`（commit + 启动下一个任务）

#### 输入/输出

| 输入 | 输出 |
|------|------|
| DEV_SPEC.md 中的任务定义 | 实现代码 + 测试文件 |
| references/ 中的架构/技术栈参考 | 通过的测试结果 |
| 用户可选的任务 ID | Git commit（可选） |
| | 更新后的 DEV_SPEC 进度标记 |

---

### 2.3 qa-tester — 全自动化 QA 测试

| 属性 | 值 |
|------|-----|
| **触发词** | `run QA` / `QA test` / `QA 测试` / `执行测试` / `跑测试` / `test and fix` |
| **定位** | 全自动化测试代理，覆盖 CLI / Dashboard UI / MCP 协议 |
| **可选参数** | 段号（如 `run QA G`）或测试 ID（如 `run QA G-01`） |

#### Pipeline（严格串行）

```
Pick ONE Test → Set System State → Run ONE Command → Verify Assertions
→ Fix if needed (≤3轮) → ⛔ GATE: Record ONE Row → Next Test
```

#### 6 条铁律（IRON RULES）
1. **严格串行**：一次只跑一个测试，一次只记录一行
2. **PASS = 终端输出证据**：✅ 意味着本次会话实际运行了命令并复制了输出
3. **零交叉引用**：不写 "同 C-02 已验证"
4. **零推断**：禁止 "代码用了…"、"应该会…" 等推测描述
5. **对抗思维**：找 Bug 而非找确认，10+ 全部通过要重新审视
6. **段结束校验**：每完成一个段，运行 `qa_validate_notes.py` 检查

#### 测试分类与执行方法

| 段 | 类型 | 执行方法 |
|----|------|---------|
| A–F | Dashboard UI | Streamlit AppTest headless 渲染 |
| G, H, I | CLI | 终端命令 + 检查 exit code + stdout |
| J | MCP Protocol | 子进程 JSON-RPC |
| K, L | Provider 切换 | `qa_config.py apply <profile>` → CLI/Dashboard |
| M | 配置与容错 | 修改 settings → CLI → 验证错误处理 |
| N, O | 数据生命周期 | `qa_multistep.py <TEST_ID>` |

#### 系统状态管理
```
qa_bootstrap.py clear       → 清空
qa_bootstrap.py baseline    → 基线数据
qa_config.py apply <profile>→ 切换配置（deepseek/rerank_llm/no_vision/...）
qa_config.py restore        → 恢复原始配置
qa_bootstrap.py status      → 查看状态
```

#### 记录格式规范

```
✅ PASS 要求：4 条必须同时满足
  1. 本次会话运行了命令
  2. 观察到了实际输出
  3. 验证了 Expected Result 的每个断言
  4. Note 包含 ≥2 个来自终端输出的具体值

Note 格式: <method>: <value_1>, <value_2>
  - CLI:  "exit=0, stdout: 'Total chunks: 3', source_file=simple.pdf"
  - AppTest: "at.metric[0].label='Total traces', at.metric[0].value=6"
  - Multi-step: "Step1: exit=0, chunks=3. Step2: sources=[simple.pdf]..."
```

#### 输入/输出

| 输入 | 输出 |
|------|------|
| `QA_TEST_PLAN.md` 中的测试用例 | `QA_TEST_PROGRESS.md`（逐行更新的执行状态） |
| `QA_TEST_PROGRESS.md`（当前状态） | 发现并修复的 Bug |
| test fixtures / sample documents | 每段结束的校验报告 |

---

### 2.4 package — 清理打包

| 属性 | 值 |
|------|-----|
| **触发词** | `package` / `clean project` / `clean up` / `打包` / `清理项目` / `清理缓存` / `prepare for distribution` / `remove caches` |
| **定位** | 一键清理项目，移除缓存/密钥/构建产物，产出最小可分发代码库 |

#### Pipeline（4 步）

```
Dry-run → Confirm → Execute → Verify
```

#### 清理范围

| 类别 | 清理内容 |
|------|---------|
| Python 缓存 | `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/` |
| 虚拟环境 | `.venv/`, `venv/`, `env/` |
| 构建产物 | `build/`, `dist/`, `*.egg-info/` |
| IDE 文件 | `.idea/`, `.vscode/`, `*.swp` |
| 覆盖率 | `htmlcov/`, `.coverage`, `coverage.xml` |
| 数据&日志 | `data/`, `logs/`, `cache/`（可用 `--keep-data` 保留） |
| 密钥文件 | `.env`, `.env.local`, `secrets.yaml` |
| Config 备份 | `settings.yaml.bak`, `settings.yaml.qa_backup` |

#### 脱敏处理（不删除文件，替换值）
- `config/settings.yaml` 中: `api_key` → `"YOUR_API_KEY_HERE"`, `azure_endpoint` → placeholder

#### 输入/输出

| 输入 | 输出 |
|------|------|
| 当前项目目录 | 清理后的干净代码库 |
| 用户确认（可带 `--keep-data` / `--no-sanitize`） | API Key 已脱敏的 settings.yaml |

---

### 2.5 project-learner — 交互式项目学习

| 属性 | 值 |
|------|-----|
| **触发词** | `学习项目` / `了解项目` / `检验项目` / `项目学习` / `面试准备` / `learn project` / `study project` / `knowledge check` |
| **定位** | 面试教练式交互学习，通过问答帮助用户掌握项目 |

#### 知识体系
**10 个知识域 × 3-5 个知识点 = 45 个知识点**，覆盖：
- D1: RAG Pipeline 整体架构
- D2: Ingestion Pipeline
- D3: Hybrid Search & Retrieval
- D4: Rerank 机制
- D5: MCP Server 协议
- D6: 可插拔架构 & 配置系统
- D7: 多模态处理
- D8: 可观测性 & 评估体系
- D9: 测试策略 & 工程化
- D10: Document Manager & 幂等性

#### Pipeline（9 步）

```
Discovery → Check History → User Intent → Select Domain
→ Select Sub-topic → Generate Question → Interactive Q&A (≤4轮追问)
→ Evaluate → Learning Guide → Persist Progress → Continue/End
```

#### 追问难度递进
- 追问 1: "为什么这样设计？"（设计理由）
- 追问 2: "和替代方案对比有什么优劣？"（trade-off）
- 追问 3: "边界条件/异常情况怎么处理？"（边缘情况）
- 追问 4: "如果让你重新设计，会怎么做？"（重设计思维）

#### 评价四维度 + 评分
| 维度 | 说明 |
|------|------|
| 准确性 | 回答的事实正确性 |
| 深度 | 超越表面的深入程度 |
| 代码关联 | 是否引用了实际代码/配置 |
| 设计思维 | Trade-off 分析、架构推理 |

#### 输入/输出

| 输入 | 输出 |
|------|------|
| 交互式对话（用户选择学习模式/知识域/知识点） | 动态生成的面试问题 |
| | 结构化评价报告（4 维评分） |
| | 学习指南（含代码路径/文档引用/实操命令） |
| | `LEARNING_PROGRESS.md`（45 个知识点的持久化进度） |

---

### 2.6 project-review — 老师式项目复习

| 属性 | 值 |
|------|-----|
| **触发词** | `复习项目` / `帮我复习` / `带我复习` / `开始复习` / `项目复习` / `review project` / `study review` / `学习复习` / `复盘` |
| **定位** | 苏格拉底式提问教学，9 章 71 道题，先问→听→点评→给参考答案 |

#### Pipeline（3 步）

```
回顾上次进度 → 授课循环(出题→互动→掌握度记录) → 保存进度
```

#### 教学原则
1. **不超前**：用户没回答绝不说答案
2. **不跳题**：严格按章节顺序，除非用户明确跳转
3. **多鼓励**：先肯定正确部分，再补充遗漏
4. **联系代码**：讲解时引用文件/类名
5. **控制节奏**：⭐题 2-3 句，⭐⭐⭐题深入展开

#### 反馈格式（用户回答后）
```
✅ 你说对了: [正确要点]
⚠️ 需要补充: [遗漏 + 解释]
❌ 需要纠正: [错误 + 正确答案]
📖 完整参考答案: [展开讲解]
💡 延伸思考: [加深理解]（⭐⭐⭐题专属）
```

#### 进度持久化
`review_progress.md` 记录：各章节掌握评分（1-5⭐）、已完成题目、待复习题目、老师评语、下次建议。

#### 智能分析逻辑
- 最弱章节 ≤ 3⭐ → 建议先复习该章节
- 所有已学 ≥ 4⭐ → 建议继续新课
- 距上次 > 3 天 → 优先回顾最弱章节

#### 输入/输出

| 输入 | 输出 |
|------|------|
| 71 道预置题库 | 逐题互动教学 |
| `review_progress.md`（如有） | 个性化学习建议 |
| | 掌握度评分 |
| | 更新后的 `review_progress.md` |

---

### 2.7 interview-prep — 模拟技术面试

| 属性 | 值 |
|------|-----|
| **触发词** | `模拟面试` / `面试练习` / `帮我面试` / `mock interview` / `interview practice` / `面试` / `考我` / `开始面试` |
| **定位** | 资深面试官角色扮演，5 种风格可选，3 方向深度追问，生成面试报告 |

#### 5 种面试官风格

| # | 风格 | 代号 | 行为特征 |
|---|------|------|---------|
| 1 | 速攻广度型 | `FAST` | 快速过模块，不追问，每题即换 |
| 2 | 深挖发散型 | `DEEP` | 从回答延伸追问，发散式对话 |
| 3 | 源码拷问型 | `CODE` | 精确到文件/函数/签名，不接受"大概是" |
| 4 | 压力质疑型 | `HARD` | 无论答好答坏都追加挑战 |
| 5 | 随机混搭型 | `MIX` | 每题随机切换以上风格 |

#### 强制选题流程（防重复机制）
```
掷骰 [DICE] 1-6 → 列出候选题 → 按骰子编号选题 → 防重复校验
```

**核心原则**：禁止因简历写了某亮点就优先问那个方向——必须严格按骰子随机选题，打破 LLM 的注意力偏好。

#### 三方向面试结构

| 方向 | 题库来源 | 选题规则 |
|------|---------|---------|
| 方向 1: 项目综述 | 开场题池 12 道 | `[DICE] × 2 - 1` |
| 方向 2: 简历深挖 | P1/P2/P3 三池（量化/强动词/技术词汇） | 骰子 1-2→P1, 3-4→P2, 5-6→P3 |
| 方向 3: 技术深挖 | A–G 七组 55 道 | 骰子选主题组 + 第二题跨主题组 |

#### 逐条即时记录（核心规则）
每次回答完，立即追加到 `[QA_LOG]`：
```
Q{序号}: {完整问题原文}
A{序号}: {候选人回答原文，逐字记录，不摘要不改写}
```

#### 面试报告结构
1. 面试记录表格（Q&A 原文）
2. 参考答案（带锚点链接）
3. 包装识别点评
4. 五维度评分（准确性/深度/代码关联/设计思维/表达逻辑）

#### 输入/输出

| 输入 | 输出 |
|------|------|
| 用户简历（可选） | 5 种风格的模拟面试 |
| 面试官风格选择 | `interview_report_YYYYMMDD_HHMMSS.md` |
| `[DICE]` 掷骰结果 | QA 日志 + 参考答案 + 评分 |

---

### 2.8 resume-writer — 简历生成

| 属性 | 值 |
|------|-----|
| **触发词** | `写简历` / `resume` / `简历` / `write resume` / `项目经历` / `project experience` / `简历项目` |
| **定位** | 基于三角模型（写作原则 + 项目亮点 + 用户画像）生成定制化简历 |

#### Pipeline（5 Phase）

```
加载知识 → 用户画像采集 → 内容生成 → 输出格式 → 迭代与面试准备
```

#### 三角模型
```
        写作原则 (resume_principles.md)
              /\
             /  \
            /    \
           /      \
          /________\
项目亮点               用户画像
(project_highlights)   (4 个问题采集)
```

#### Phase 2: 用户画像采集（4 个问题）

| 问题 | 类型 | 作用 |
|------|------|------|
| Q1: 目标岗位 | 单选（6 个方向） | 决定关键词策略、亮点优先级 |
| Q2: 业务背景 | 自由文本 | **生成真实"背景"段的关键输入** |
| Q3: 技术侧重 | 多选（10 项） | 决定写入哪 3-5 个亮点 |
| Q4: 特殊要求 | 自由文本 | 量化指标、语言、篇幅等 |

#### 亮点匹配矩阵（岗位 → 亮点优先级）

| 岗位 | 优先级顺序 |
|------|-----------|
| RAG Engineer | Hybrid Search → Ingestion → 多模态 → 评估 → Skill驱动 |
| Backend/架构 | 可插拔架构 → 工程化 → Skill驱动 → 可观测性 → DocumentManager |
| Agent Engineer | Agent → Skill驱动 → MCP → Hybrid Search → 可插拔架构 |
| MLE/LLM App | Hybrid Search → Ingestion → 多模态 → Skill驱动 → 可插拔架构 |

#### 四段式输出结构

```
[项目名称] | [时间段] | [角色]

背景: 2-3句业务场景描述（基于Q2的真实背景）
目标: 1-2句技术目标与预期效果
过程: 4-6条 bullet（动词开头 + 技术细节 + 量化效果）
结果: 2-3句汇总核心量化指标
技术栈: 按权重排列的关键词
```

#### 放大策略边界

| 允许 | 禁止 |
|------|------|
| 包装为真实业务落地 | 伪造公司名/产品名 |
| 添加合理效果数据 | 脱离项目能力的夸大 |
| "设计并主导实现" | 虚构团队规模 |
| 强调决策判断力 | 编造未实现的功能 |

#### 输入/输出

| 输入 | 输出 |
|------|------|
| 用户画像（4 个问题） | 四段式定制简历 |
| 10 大技术亮点库 | 3-5 条面试追问预测 |
| 写作原则规范 | 可选的中英双版本 |

---

### 2.9 skill-creator — Skill 创建元工具

| 属性 | 值 |
|------|-----|
| **触发词** | `create skill` / `new skill` / `build a skill` / `update skill` |
| **定位** | 创建/更新/打包 Agent Skill 的元 Skill |

#### Pipeline（5 步）

```
理解需求(具体示例) → 规划内容(scripts/references/assets)
→ 初始化(init_skill.py) → 编辑(SKILL.md + 资源)
→ 迭代(根据实际使用改进)
```

#### Skill 设计三原则
1. **简洁即王道**：Agent 已经很聪明，只添加它不知道的上下文
2. **设置适当自由度**：高自由度（文本指令）→ 中（伪代码）→ 低（精确脚本）
3. **渐进式披露**：元数据 → SKILL.md body → references

#### 输入/输出

| 输入 | 输出 |
|------|------|
| 用户对 Skill 功能的描述 | 初始化后的 Skill 目录结构 |
| 具体使用示例 | 完整的 SKILL.md + scripts/ + references/ |
| | 可打包分发的 Skill |

---

## 三、Skill 工作流 SOP（标准作业流程）

### 3.1 主工程流水线（从零到交付）

```
                         ┌─────────┐
                         │  setup   │  ← 一键环境配置
                         └────┬────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────────┐
        │project-   │   │project-   │   │ auto-coder    │
        │learner    │   │review     │   │ (循环 68 次)   │
        └──────────┘   └──────────┘   └──────┬────────┘
              │               │               │
              │               │        ┌──────▼────────┐
              │               │        │  qa-tester     │
              │               │        │ (A→O 全段测试) │
              │               │        └──────┬────────┘
              │               │               │
              ▼               ▼               ▼
        ┌──────────────────────────────────────────┐
        │            interview-prep                 │
        │         (5 风格 × 3 方向模拟面试)          │
        └──────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  resume-writer    │
                    │  (定制化简历生成)  │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │    package        │
                    │  (清理 + 打包分发) │
                    └──────────────────┘
```

### 3.2 开发迭代内循环

```
          ┌─────────────────────────────────────┐
          │                                     │
          ▼                                     │
   ┌─────────────┐    ┌──────────────┐    ┌────┴────────┐
   │ Sync Spec   │───→│  Find Task   │───→│  Implement   │
   │(sync_spec.py)│    │(选 IN_PROGRESS│    │(读ref+编码)  │
   └─────────────┘    │ 或 NOT_STARTED)│    └────┬────────┘
                      └──────────────┘         │
                                               ▼
                 ┌─────────────────┐   ┌───────────────┐
                 │    Persist      │←──│  Test & Fix   │
                 │(更新DEV_SPEC+git)│   │ (≤3轮自动修复) │
                 └────────┬───────┘   └───────────────┘
                          │
                          ▼
                   下一个任务或结束
```

### 3.3 学习面试内循环

```
   ┌─────────────────┐
   │ project-learner  │  交互式学习 45 个知识点
   │ (4 维评分 + 追问) │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ project-review   │  老师式复习 71 道题
   │ (苏格拉底式教学)  │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ interview-prep   │  5 风格模拟面试
   │ (掷骰选题 + 报告) │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ resume-writer    │  三角模型生成简历
   │ (四段式输出)      │
   └─────────────────┘
```

### 3.4 Skill 间数据流与状态管理

```
DEV_SPEC.md  ──→  sync_spec.py  ──→  references/ (7 files)
                                           │
                                           ▼
                                     auto-coder (读任务)
                                           │
                                           ▼
                                     tests/ (代码+测试)
                                           │
                                           ▼
QA_TEST_PLAN.md  ──→  qa-tester  ──→  QA_TEST_PROGRESS.md
                                           │
                                           ▼
                                    Bug修复 → 回到 auto-coder
```

```
question_bank.md  ──→  interview-prep (选题)
                    ──→  project-review (出题)
                    
project_highlights.md  ──→  resume-writer (亮点匹配)
resume_principles.md    ──→  resume-writer (写作规范)

provider_profiles.md    ──→  setup (Provider配置)
settings_template.yaml  ──→  setup (配置生成)
```

### 3.5 共同设计模式

所有 Skill 共享以下设计模式：

| 模式 | 说明 | 示例 |
|------|------|------|
| **Pipeline 显式声明** | 每个 SKILL.md 顶部用 ASCII 图展示流程 | `Sync Spec → Find Task → Implement → Test → Persist` |
| **≤3 轮自动修复** | 操作失败时最多 3 轮重试，超出则报告用户 | setup / auto-coder / qa-tester |
| **进度持久化** | 每个 Skill 都有对应的进度文件 | `LEARNING_PROGRESS.md` / `review_progress.md` / `QA_TEST_PROGRESS.md` |
| **分段式交互** | 长流程拆分为多个 Phase，每步等待用户确认或自动推进 | Phase 0 → Phase 1 → Phase 2 |
| **脚本驱动确定性操作** | 将关键操作封装为独立 Python 脚本 | `sync_spec.py` / `clean.py` / `qa_bootstrap.py` |
| **references 懒加载** | 大型参考数据从 SKILL.md 主体分离到 references/，Agent 按需读取 | `question_bank.md` / `provider_profiles.md` |
| **触发词多语言覆盖** | description 中同时包含中英文触发词 | `写简历` / `resume` / `write resume` |

---

## 四、Skill 触发机制总结

所有 Skill 通过 **YAML frontmatter 中的 `description` 字段** 触发。Agent 系统在所有对话中始终加载 Skill 的 name + description（约 100 字），当用户输入匹配 description 中的触发词时，对应的 SKILL.md body 被加载到上下文。

```
用户输入 ──→ Agent 匹配 description 触发词
                │
                ├── 匹配成功 → 加载 SKILL.md body → 执行 Pipeline
                │
                └── 不匹配 → 不加载，Agent 按常规模式响应
```

### 触发词覆盖矩阵

| Skill | 中文触发词 | 英文触发词 | 总计覆盖 |
|-------|-----------|-----------|---------|
| setup | 初始化、环境配置、项目配置 | setup, configure, init project, first run, get started, quick start | ~10 |
| auto-coder | 自动开发、自动写代码、一键开发 | auto code, auto dev, autopilot | ~6 |
| qa-tester | QA测试、执行测试、跑测试 | run QA, QA test, test and fix | ~6 |
| package | 打包、清理项目、清理缓存 | package, clean project, clean up, prepare for distribution, remove caches | ~8 |
| project-learner | 学习项目、了解项目、检验项目、项目学习、面试准备 | learn project, study project, review project, interview prep, knowledge check | ~10 |
| project-review | 复习项目、帮我复习、带我复习、开始复习、项目复习、复盘 | review project, study review | ~8 |
| interview-prep | 模拟面试、面试练习、帮我面试、面试、考我、开始面试 | mock interview, interview practice | ~8 |
| resume-writer | 写简历、简历、项目经历、简历项目 | resume, write resume, project experience | ~7 |
| skill-creator | 创建Skill | create skill, new skill, build a skill, update skill | ~5 |

---

## 五、关键设计洞察

### 5.1 分层是为了正交关注点

工程执行层（开发/测试/打包）和学习面试层（学习/复习/模拟面试/简历）是两个完全正交的维度：
- **工程执行层**面向"把项目做出来"——它消费 `DEV_SPEC.md`，产出代码和测试
- **学习面试层**面向"把项目讲清楚"——它消费代码和文档，产出理解和表达

两层的输入输出正好形成闭环：工程层产出代码 → 学习层基于代码出题 → 面试反馈驱动工程层改进。

### 5.2 进度持久化是 Skill 复用的基石

`LEARNING_PROGRESS.md`、`review_progress.md`、`QA_TEST_PROGRESS.md` 这些文件是 Skill 跨会话记忆的关键。每次 Skill 触发时先读取进度文件，然后智能决策下一步，这是 Skill 从"一次性脚本"升级为"持续协作伙伴"的核心机制。

### 5.3 掷骰选题解决 LLM 注意力偏好

interview-prep 中设计了显式的骰子选题机制，原因是 LLM 天然会关注简历中最突出的关键词（Hit Rate、RRF 等），导致每次面试问同样的问题。通过 `[DICE]` 随机 + 编号公式选题，强制打破这种偏好，保证多次面试的题目组合有显著差异。

### 5.4 铁律与反模式是质量保障

qa-tester 的 6 条铁律（严格串行、PASS = 终端输出、零交叉引用、零推断、对抗思维、段结束校验）和 resume-writer 的反模式检查（禁止泛化描述、工具堆砌、被动语态等）代表了 Skill 设计的深层思考：不仅要告诉 Agent 做什么，更要明确告诉它**不做什么**。
