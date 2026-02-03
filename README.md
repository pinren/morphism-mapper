# 🌊 Morphism Mapper

> **基于范畴论的跨领域结构映射工具**
> 
> 将 Domain A 的问题结构映射到远域 Domain B，借助 B 领域的成熟定理生成非共识创新方案。

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v2.6-green.svg)](https://github.com/pinren/morphism-mapper/releases)
[![Domains](https://img.shields.io/badge/domains-27+-orange.svg)](#built-in-domains)

---

## 🤖 这是一个 Claude Code / OpenCode Skill

Morphism Mapper 是一个为 **Claude Code** 和 **OpenCode** 设计的智能体技能 (Agent Skill)。它通过结构化的提示词和领域知识库，让 AI 能够系统化地进行跨域思维映射。

### 安装方法

#### Claude Code 环境

```bash
# 克隆到 Claude Code 的 skills 目录
cd ~/.claude/skills
git clone https://github.com/pinren/morphism-mapper.git

# 重启 Claude Code 即可使用
```

#### OpenCode 环境

```bash
# 克隆到 OpenCode 的 skills 目录
cd ~/.config/opencode/skills
git clone https://github.com/pinren/morphism-mapper.git

# 重启 OpenCode 即可使用
```

> **提示**: 安装完成后，在对话中直接描述问题即可触发 Morphism Mapper。例如："帮我分析一下这个商业模式"、"如何用庄子哲学看待创业困境？"

---

## 📖 这是什么？

Morphism Mapper 是一个基于**范畴论 (Category Theory)** 的跨域思维工具。

当你面对复杂问题时，大脑往往被局限在熟悉的认知框架中。Morphism Mapper 通过将问题结构**映射**到看似无关的领域，借助那些领域已经验证的定理和模式，为你提供**突破性的洞察**。

### 核心隐喻

想象你正在解决一个商业问题，但你看不清楚。

Morphism Mapper 的工作方式是：
1. **提取骨架** - 将问题的结构抽象出来（实体、关系、约束）
2. **寻找同构** - 在完全不同的领域中找到**相同的结构**
3. **借用智慧** - 那个领域解决类似问题的成熟方案是什么？
4. **拉回应用** - 将那个方案翻译回你的问题

就像用 X 光透视骨骼，不管外表多么不同，深层的结构往往惊人地相似。

---

## 🚀 快速开始

### 模式一：直接描述问题（推荐）

直接描述你的困境，系统自动进入四阶段流程：

```
"面对抑郁症的朋友，我应该扮演一个什么角色？"
```

**输出示例**:
- 🌿 **生态学视角**: 你不是医生，是"共生伙伴"——创造适宜微环境
- 🛡️ **免疫学视角**: 你是"调节T细胞"——防止过度反应，维持耐受
- 🌊 **庄子哲学视角**: 你是"无用之用的陪伴者"——接纳"此刻无用"的状态

### 模式二：快捷命令

| 命令 | 功能 |
|------|------|
| `/morphism-extract "问题"` | 提取范畴骨架 |
| `/morphism-domains` | 列出所有可用领域 |
| `/morphism-map <domain>` | 执行到指定领域的映射 |
| `/morphism-synthesize` | 拉回合成生成提案 |
| `/morphism-scale` | **全息缩放** - 局部成功如何全局复制 (Kan Extension) |

### 模式三：新增自定义领域

```
"增加易经思想领域"
"新增领域：孙子兵法"
"扩展领域：中医"
```

---

## 🗺️ 内置领域（27个）

<details>
<summary><b>物理学与复杂性科学</b></summary>

- **quantum_mechanics** - 量子力学（叠加态、不确定性、纠缠）
- **thermodynamics** - 热力学（能量、熵、耗散结构）
- **information_theory** - 信息论（熵、信道容量、噪声）
- **complexity_science** - 复杂性科学（涌现、混沌、自组织）

</details>

<details>
<summary><b>生命科学与认知</b></summary>

- **evolutionary_biology** - 进化生物学（选择、适应、关键创新）
- **ecology** - 生态学（种群、共生、生态位）
- **immunology** - 免疫学（识别、记忆、耐受）
- **neuroscience** - 神经科学（神经可塑性、预测编码）
- **zhuangzi** - 庄子哲学（变化、尺度、相对性）

</details>

<details>
<summary><b>系统与控制</b></summary>

- **control_systems** - 控制系统（反馈、调节、稳定）
- **distributed_systems** - 分布式系统（一致性、共识、分区容错）
- **network_theory** - 网络理论（节点、连接、传播）

</details>

<details>
<summary><b>数学与运筹</b></summary>

- **game_theory** - 博弈论（策略、均衡、信号）
- **operations_research** - 运筹学（优化、约束、排队）
- **second_order_thinking** - 二阶思维（反馈延迟、意外后果）

</details>

<details>
<summary><b>经济与社会</b></summary>

- **behavioral_economics** - 行为经济学（认知偏差、损失厌恶）
- **social_capital** - 社会资本（网络、信任、结构洞）
- **incentive_design** - 激励机制设计（动机、委托代理）
- **linguistics** - 语言学（符号、意义、隐喻）

</details>

<details>
<summary><b>战略与创新</b></summary>

- **military_strategy** - 军事战略（机动、后勤、OODA）
- **innovation_theory** - 创新理论（颠覆性、S曲线、网络效应）
- **kaizen** - 精益/持续改善（浪费消除、PDCA、现场）
- **antifragility** - 反脆弱性（凸性、选择权、杠铃策略）
- **mythology** - 神话学/原型（英雄之旅、阈限、阴影）

</details>

<details>
<summary><b>⭐ v2.5 新增领域</b></summary>

- **anthropology** - 人类学（文化、田野调查、参与观察）
- **religious_studies** - 宗教学（神圣与世俗、仪式、象征）
- **mao_zedong_thought** - 毛泽东思想（实践论、矛盾论、持久战）

</details>

---

## 🔬 技术原理

### 范畴论基础

Morphism Mapper 基于三个核心原理：

1. **Object Preservation** - 识别核心实体
2. **Morphism Preservation** - 识别实体间动态关系  
3. **Composition Consistency** - 映射结果可拉回并保持逻辑闭环

### 四阶段流程

```
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: Category Extraction                                │
│  将问题拆解为 Objects（实体）、Morphisms（关系）、Constraints（约束）│
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 2: Domain Selection                                   │
│  基于拓扑结构，选择逻辑距离远但结构相似的 Domain B              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 3: Functorial Mapping                                 │
│  建立映射 F: A → B，在 Domain B 中寻找已证实的定理            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 4: Pull-back & Synthesis                              │
│  将 Domain B 的定理逆映射回 Domain A，生成可执行方案          │
└─────────────────────────────────────────────────────────────┘
```

### 高级模块（按需挂载）

| 模块 | 触发条件 | 功能 |
|------|----------|------|
| **Yoneda Probe** | 信息不透明/模糊 | 通过关系网反推对象本质 |
| **Natural Transformation** | 环境变化/策略失效 | 平滑迁移策略逻辑 |
| **Adjoint Balancer** | 【强制执行】输出前 | 可行性校验与优化 |
| **Limits/Colimits** | 多域交叉验证后 | 提取跨域元逻辑 |
| **Kan Extension** ⭐v2.6新增 | 局部成功→全局复制 | 全息缩放：激进/保守扩展策略 |

#### Kan Extension 详解

**解决什么问题？**

当你在一线城市/美国市场/ToB业务验证成功后，想扩展到下沉市场/欧洲/ToC时：
- 直接复制？可能失败（市场差异大）
- 完全重做？太慢（错失窗口期）

Kan Extension 提供**两种极端策略**帮助你做出理性决策：

**Left Kan Extension (激进扩展)**
- 假设：新市场与源市场**结构相似**
- 策略：最大化复制成功要素（80%+）
- 风险：高（假设可能不成立）
- 收益：高（如果成功，指数级增长）
- 适用：市场相似度高、窗口期短

**Right Kan Extension (保守扩展)**
- 假设：新市场存在**未知约束**
- 策略：最大化本地适配（80%+）
- 风险：低（基于已知约束）
- 收益：中等（稳健但可能错失机会）
- 适用：市场差异大、资源有限

**触发方式**：
- 自动触发：当 Adjoint Balancer 检测到"核心定理无法落地"时
- 手动触发：`/morphism-scale`
- 关键词："复制到XX市场"、"如何规模化"、"下沉市场"

**完整示例**：参见 [`examples/kan_extension_example.md`](examples/kan_extension_example.md)

---

## 💡 使用示例

### 示例 1：ETF 用户留存问题

**输入**: "我想设计 ETF 产品的用户留存体系，目前用户流失严重。"

**映射到**: 庄子哲学

**洞察**: 
> 问题核心在于用户对短期波动的过度反应。庄子"小知不及大知，小年不及大年"——需要改变观察尺度。

**提案**: 开发"冥灵模式"UI
- 将净值曲线的最小观测单位设为"季度"而非"日"
- 默认展示 3 年/5 年视角
- 引入"时间胶囊"功能：投资后锁定查看权限

---

### 示例 2：AI 时代的个人意义

**输入**: "既然 AI 终将整合所有知识，我现在整理的意义是什么？"

**映射到**: 进化生物学 + 神话学 + 复杂性科学 + 存在主义

**洞察**:
> 你的行为类似于"主动选择成为祖先"——清醒地接受个体终将消亡，但通过在关键转折点将积累传递给"下一代"（AI），获得某种进化连续性。

> 这不是失败者的自我安慰，而是**悲剧英雄的高级形态**：清楚代价，仍选择参与。

---

## 📂 仓库结构

```
morphism-mapper/
├── SKILL.md                    # 核心技能文档
├── commands/                   # 快捷命令定义
│   ├── extract.md             # 范畴提取
│   ├── map.md                 # 结构映射
│   ├── synthesize.md          # 合成提案
│   ├── add-domain.md          # 新增领域
│   └── config.md              # 配置管理
├── modules/                    # 高级模块
│   ├── yoneda_probe.md        # 米田探针
│   ├── natural_transformation.md  # 自然变换
│   ├── adjoint_balancer.md    # 伴随平衡器
│   └── limits_colimits.md     # 极限/余极限
├── references/                 # 领域知识库
│   ├── *_v2.md                # V2标准领域 (100+14+14+18)
│   ├── custom/                # 自定义领域
│   └── v1_backup/             # V1版本备份
├── examples/                   # 使用示例
│   └── few_shot_prompts.md
└── assets/                     # 资源文件
```

---

## 🛠️ 领域标准 (V2)

每个领域文件遵循 V2 标准格式：

- **100 基本基石**: 导语 + 18哲学观 + 22核心原则 + 28思维模型 + 22方法论 + 10避坑指南
- **14 核心对象 (Objects)**: 含定义、本质、关联
- **14 核心态射 (Morphisms)**: 含定义、涉及、动态
- **18 定理/模式**: 含内容、适用结构、映射提示、案例研究

---

## 🤝 贡献

欢迎添加新的领域！请遵循 V2 标准格式：

1. 在 `references/custom/` 创建 `[domain_name]_v2.md`
2. 包含完整的 100+14+14+18 结构
3. 每个定理必须有具体可操作的 Mapping_Hint

---

## 📜 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

感谢范畴论提供的强大数学框架，以及所有跨学科思想家——从庄子到塔勒布，从普里高津到塔内特——他们的智慧构成了这个工具的领域知识库。

---

> *"人皆知有用之用，而莫知无用之用也。" —— 庄子*

**在 AI 时代，跨域思考可能是人类最后的领地。**
