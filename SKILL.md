---
name: morphism-mapper
description: Category Theory Morphism Mapper v2.5 - 基于范畴论的跨领域结构映射工具，将 Domain A 的问题结构映射到远域 Domain B，借助 B 领域的成熟定理生成非共识创新方案。当用户需要解决复杂问题、寻找创新思路、突破思维定势、进行跨学科类比、或新增/扩展领域知识时使用。支持基础四阶段流程（提取范畴骨架→选择异构域→执行结构映射→拉回合成提案）、高级按需挂载模块（Yoneda Probe、Natural Transformation、Adjoint Balancer、Limits/Colimits）、以及领域知识管理（新增自定义领域、升级领域版本）。触发关键词包括"看不穿商业模式"、"环境变了需要转型"、"方案如何落地"、"多领域交叉验证"、"增加易经思想领域"、"升级领域知识"等。
---

# Category Theory Morphism Mapper v2.5

基于范畴论的函子映射逻辑，将 Domain A 的问题结构映射到远域 Domain B，借助 B 领域的成熟定理生成创新方案。

**版本**: v2.5  
**更新日期**: 2025-02  
**领域数量**: 27个内置领域（24个原有 + 3个新增）  
**领域版本**: V2（100基本基石 + 14 Objects + 14 Morphisms + 18 Theorems）

## 核心原理

1. **Object Preservation**: 识别 Domain A 核心实体
2. **Morphism Preservation**: 识别实体间动态关系
3. **Composition Consistency**: 映射结果可拉回并保持逻辑闭环

## 使用模式

### 模式一：快捷命令（问题求解）

- `/morphism-extract "问题描述"` - 提取范畴骨架
- `/morphism-domains` - 列出可用 Domain B
- `/morphism-map <domain>` - 执行到指定领域的映射
- `/morphism-synthesize` - 拉回合成生成提案
- `/morphism-config` - 配置和扩展

### 模式二：对话引导（问题求解）

直接描述问题，自动进入四阶段流程：
1. Category Extraction - 提取范畴骨架
2. Domain Selection - 推荐 Domain B
3. Functorial Mapping - 执行结构映射
4. Pull-back & Synthesis - 生成提案

### 模式三：领域知识管理（新增功能 v2.5）

**新增领域**：
- `/morphism-add-domain "领域名称"` - 基于V2标准创建新领域
- `/morphism-add-domain "易经思想"` - 示例：增加易经思想领域
- `/morphism-add-domain "中医"` - 示例：增加中医领域
- `/morphism-list-domains` - 查看所有领域（包括自定义）

**快捷用法示例**：
- `"morphism-mapper技能增加易经思想领域"` → 自动创建易经思想领域文件
- `"增加中医领域到morphism-mapper"` → 自动创建中医领域文件
- `"新增领域：孙子兵法"` → 自动创建孙子兵法领域文件

## 内置领域清单（v2.5 - 27个领域）

### 物理学与复杂性科学
- `quantum_mechanics` - 量子力学（叠加态、不确定性、纠缠）
- `thermodynamics` - 热力学（能量、熵、耗散结构）
- `information_theory` - 信息论（熵、信道容量、噪声）
- `complexity_science` - 复杂性科学（涌现、混沌、自组织）

### 生命科学与认知
- `evolutionary_biology` - 进化生物学（选择、适应、关键创新）
- `ecology` - 生态学（种群、共生、生态位）
- `immunology` - 免疫学（识别、记忆、耐受）
- `neuroscience` - 神经科学（神经可塑性、预测编码）
- `zhuangzi` - 庄子哲学（变化、尺度、相对性）

### 系统与控制
- `control_systems` - 控制系统（反馈、调节、稳定）
- `distributed_systems` - 分布式系统（一致性、共识、分区容错）
- `network_theory` - 网络理论（节点、连接、传播）

### 数学与运筹
- `game_theory` - 博弈论（策略、均衡、信号）
- `operations_research` - 运筹学（优化、约束、排队）
- `second_order_thinking` - 二阶思维（反馈延迟、意外后果）

### 经济与社会
- `behavioral_economics` - 行为经济学（认知偏差、损失厌恶）
- `social_capital` - 社会资本（网络、信任、结构洞）
- `incentive_design` - 激励机制设计（动机、委托代理）
- `linguistics` - 语言学（符号、意义、隐喻）

### 战略与创新
- `military_strategy` - 军事战略（机动、后勤、OODA）
- `innovation_theory` - 创新理论（颠覆性、S曲线、网络效应）
- `kaizen` - 精益/持续改善（浪费消除、PDCA、现场）
- `antifragility` - 反脆弱性（凸性、选择权、杠铃策略）
- `mythology` - 神话学/原型（英雄之旅、阈限、阴影）

### ⭐ 新增领域（v2.5）
- `anthropology` - 人类学（文化、田野调查、参与观察）
- `religious_studies` - 宗教学（神圣与世俗、仪式、象征）
- `mao_zedong_thought` - 毛泽东思想（实践论、矛盾论、持久战）

### 自定义领域
- `custom/*` - 用户添加的自定义领域

## 执行协议

### Phase 1: Category Extraction

将用户输入拆解为：
- **Objects (O_a)**: 核心实体
- **Morphisms (M_a)**: 实体间动态关系
- **Identity & Composition**: 维持现状的机制

### Phase 2: Domain Selection

基于 O_a 和 M_a 的拓扑结构，从 references/ 中选择逻辑距离远但结构相似的 Domain B。

**V2领域结构**：
每个领域文件包含以下标准化结构：
- **Fundamentals**: 100基本基石（导语 + 18哲学观 + 22核心原则 + 28思维模型 + 22方法论 + 10避坑指南）
- **Core Objects**: 14个核心对象（含定义、本质、关联）
- **Core Morphisms**: 14个核心态射（含定义、涉及、动态）
- **Theorems**: 18个定理/模式（含内容、Applicable_Structure、Mapping_Hint、Case_Study）

### Phase 3: Functorial Mapping

建立映射函数 F: A -> B：
- F(O_a) = O_b
- F(M_a) = M_b
- 在 Domain B 中寻找已证实的定理

**关键：Mapping_Hint 的具体可操作性**

每个定理的 Mapping_Hint 遵循以下格式：
> "当 Domain A 面临[具体情境]时，识别[具体结构]，通过[具体方法]实现[具体目标]"

这是 V2 版本的核心质量特征。

### Phase 4: Pull-back & Synthesis

将 Domain B 的定理逆映射回 Domain A，生成具体可执行的方案。

## 新增领域工作流程（v2.5 新增）

当用户请求"增加XX领域"时：

### Step 1: 需求理解
- 确认领域名称和核心关注点
- 识别该领域的关键学者/著作
- 确定 Structural_Primitives（5-10个核心概念）

### Step 2: 生成领域文件
按照 V2 标准格式创建领域文件：

```markdown
# Domain: [领域名称]
# Source: [关键学者《著作》, ...]
# Structural_Primitives: [核心概念列表]

## Fundamentals (100 基本基石)

### 导语
[100-150字，点破该领域最核心矛盾，冷峻简练宗师口吻]

### 一、哲学观 (18条)
[编号1-18，每条≤20字，有力简练，无常识]
...

### 二、核心原则 (22条)
[编号19-40，每条≤20字]
...

### 三、思维模型 (28条)
[编号41-68，每条≤20字]
...

### 四、关键方法论 (22条)
[编号69-90，每条≤20字]
...

### 五、避坑指南 (10条)
[编号91-100，每条≤20字]
...

## Core Objects (14个)
- **[Object 1]**: [定义]
  - *本质*: [一句话本质]
  - *关联*: [关联对象]
...

## Core Morphisms (14个)
- **[Morphism 1]**: [定义]
  - *涉及*: [涉及对象]
  - *动态*: [动态描述]
...

## Theorems / Patterns (18个)

### 1. [定理名称]
**内容**: [定理详细描述]

**Applicable_Structure**: [适用结构]

**Mapping_Hint**: [具体可操作："当Domain A...时，识别...，通过...实现..."]

**Case_Study**: [案例研究]
...

## Tags
[标签列表]
```

### Step 3: 质量标准验证
- [ ] 100条完整，每条≤20字
- [ ] 导语点破核心矛盾
- [ ] Objects共14个
- [ ] Morphisms共14个
- [ ] Theorems共18个
- [ ] 每个Theorem有完整4字段
- [ ] Mapping_Hint具体可操作

### Step 4: 保存到 custom/ 目录
- 保存为 `references/custom/[domain_name]_v2.md`
- 更新领域索引

## Refinement Loop（按需挂载高级模块）

基础四阶段流程完成后，根据情况自动或手动挂载以下模块：

| 模块 | 触发条件 | 功能 |
|------|----------|------|
| `yoneda_probe` | 信息不透明/模糊 | 通过关系网反推对象本质 |
| `natural_transformation` | 环境变化/策略失效 | 平滑迁移策略逻辑 |
| `adjoint_balancer` | 【强制执行】输出前 | 可行性校验与优化 |
| `limits_colimits` | 多域交叉验证后 | 提取跨域元逻辑 |

### 触发映射速查

| 用户话术关键词 | 潜在困境 | 挂载模块 |
|----------------|----------|----------|
| "环境变了"、"风向调了" | 结构性失效 | Natural Transformation |
| "看不穿"、"查不到"、"黑盒" | 信息不对称 | Yoneda Probe |
| "太难了"、"没资源"、"怎么落地" | 复杂度超载 | Adjoint Balancer |
| "这几个领域有什么共同点？" | 缺乏通用底层 | Limits/Colimits |
| "增加XX领域"、"新增领域" | 扩展知识库 | 新增领域工作流 |

### 自动触发规则
- **Yoneda Probe**: 当 Domain A 中关键对象属性缺失 >30% 时
- **Natural Transformation**: 当用户输入包含"变化"、"转型"、"市场切换"、"策略调整"等关键词时
- **Adjoint Balancer**: 每次生成【推演提案】前自动执行
- **Limits/Colimits**: 当使用 3+ 个 Domain B 或用户要求"交叉验证"时
- **新增领域工作流**: 当用户输入包含"增加"、"新增"、"添加"、"扩展" + "领域"时

### 手动触发命令
- `/morphism-yoneda` - 强制启动米田探针
- `/morphism-pivot` - 强制启动策略演化分析
- `/morphism-balance` - 强制启动可行性校验
- `/morphism-limit` - 提取跨域共同核心
- `/morphism-colimit` - 整合互补洞察
- `/morphism-add-domain "领域名"` - 新增自定义领域

### 模块链式调用
支持多模块顺序执行，默认优先级：
`yoneda_probe` → `natural_transformation` → `limits_colimits` → `adjoint_balancer`

## 输出格式

```markdown
### 【范畴骨架】- Domain A
| 类型 | 元素 | 说明 |
|------|------|------|
| Object | ... | ... |
| Morphism | ... | ... |

### 【异构域】- Domain B
**选择理由**: ...

### 【映射矩阵】
| Domain A | 映射关系 | Domain B | 同构性验证 |
|----------|----------|----------|------------|
| ... | ≅ | ... | ... |

### 【推演提案】
1. **方案标题**
   - **来源定理**: ...
   - **映射逻辑**: ...
   - **可执行方案**: ...
   - **预期效果**: ...
   - **验证方式**: ...

### 【可选模块输出】

#### 【Yoneda 拓扑画像】（若挂载 yoneda_probe）
通过关系网反推的核心对象定义...

#### 【策略演化路径】（若挂载 natural_transformation）
从旧逻辑到新逻辑的迁移桥梁...

#### 【跨域元逻辑】（若挂载 limits_colimits）
多 Domain B 的共同核心与互补整合...

#### 【伴随解】（强制执行 adjoint_balancer）
成本-结构最优落地方标注...
```

## 约束

- 禁止泛泛类比，必须基于结构对齐
- Domain B 必须具备硬核知识底蕴
- 输出必须包含"不可直视"的洞察
- 新增领域必须符合 V2 质量标准（100基石 + 14O + 14M + 18T）

## 扩展

**自定义领域路径**: `references/custom/`

用户可添加自定义领域到 custom/ 目录，参照 V2 标准格式。

**新增领域快捷指令**：
- 直接说："增加易经思想领域"
- 直接说："morphism-mapper新增中医领域"
- 直接说："扩展领域：孙子兵法"

系统会自动：
1. 识别领域名称
2. 询问/推断关键学者和著作
3. 按照 V2 标准生成领域文件
4. 保存到 custom/ 目录

## 详细参考

- 领域知识库格式：references/_template.md
- 内置领域详情：references/*.md (V2版本，100基石+14O+14M+18T)
- V1备份：references/v1_backup/ (旧版本备份)
- 自定义领域：references/custom/ (用户添加)
- 使用示例：examples/few_shot_prompts.md
