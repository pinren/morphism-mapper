# Morphism Mapper 领域知识库

本目录包含用于跨领域映射的 Domain B 知识库，涵盖人类知识精华。

## 目录结构

```
references/
├── README.md                    # 本文件
├── _template.md                 # 创建新领域的模板
│
├── 物理学与复杂性科学
│   ├── quantum_mechanics.md     # 量子力学
│   ├── thermodynamics.md        # 热力学
│   ├── information_theory.md    # 信息论
│   └── complexity_science.md    # 复杂性科学
│
├── 生命科学与认知
│   ├── evolutionary_biology.md  # 进化生物学
│   ├── ecology.md               # 生态学
│   ├── immunology.md            # 免疫学
│   ├── neuroscience.md          # 神经科学
│   └── zhuangzi.md              # 庄子哲学
│
├── 系统与控制
│   ├── control_systems.md       # 控制系统
│   ├── distributed_systems.md   # 分布式系统
│   └── network_theory.md        # 网络理论
│
├── 数学与运筹
│   ├── game_theory.md           # 博弈论
│   ├── operations_research.md   # 运筹学
│   └── second_order_thinking.md # 二阶思维
│
├── 经济与社会
│   ├── behavioral_economics.md  # 行为经济学
│   ├── social_capital.md        # 社会资本
│   ├── incentive_design.md      # 激励机制设计
│   └── linguistics.md           # 语言学/符号学
│
├── 战略与创新
│   ├── military_strategy.md     # 军事战略
│   ├── innovation_theory.md     # 创新理论
│   ├── kaizen.md                # 精益/持续改善
│   ├── antifragility.md         # 反脆弱性
│   └── mythology.md             # 神话学/原型
│
└── custom/                      # 用户自定义领域
    └── (用户添加的文件)
```

## 内置领域速查表

### 物理学与复杂性科学

| 领域 | 核心结构 | 适用场景 |
|------|----------|----------|
| quantum_mechanics | 叠加态、不确定性、纠缠 | 战略模糊期、多线并行、观测者效应 |
| thermodynamics | 能量、熵、耗散结构 | 系统效率、组织熵增、能量流动 |
| information_theory | 熵、信道容量、噪声 | 沟通效率、信息压缩、信号传递 |
| complexity_science | 涌现、混沌、自组织 | 规模效应、临界相变、路径依赖 |

### 生命科学与认知

| 领域 | 核心结构 | 适用场景 |
|------|----------|----------|
| evolutionary_biology | 选择、适应、关键创新 | 竞争策略、品类进化、适应辐射 |
| ecology | 种群、共生、生态位 | 用户生态、平台治理、承载力 |
| immunology | 识别、记忆、耐受 | 风控系统、欺诈识别、自适应防御 |
| neuroscience | 神经可塑性、预测编码 | 用户习惯培养、预期管理、学习机制 |
| zhuangzi | 变化、尺度、相对性 | 认知重构、时间焦虑、视角转换 |

### 系统与控制

| 领域 | 核心结构 | 适用场景 |
|------|----------|----------|
| control_systems | 反馈、调节、稳定 | 流程优化、自动调节、系统振荡 |
| distributed_systems | 一致性、共识、分区容错 | 多团队协作、跨地域管理、去中心化 |
| network_theory | 节点、连接、传播 | 影响力、信息流动、级联效应 |

### 数学与运筹

| 领域 | 核心结构 | 适用场景 |
|------|----------|----------|
| game_theory | 策略、均衡、信号 | 定价策略、竞争分析、可信承诺 |
| operations_research | 优化、约束、排队 | 资源配置、排程优化、库存管理 |
| second_order_thinking | 反馈延迟、二阶效应 | 政策设计、激励机制、意外后果 |

### 经济与社会

| 领域 | 核心结构 | 适用场景 |
|------|----------|----------|
| behavioral_economics | 认知偏差、损失厌恶、框架 | 用户决策、定价策略、选择架构 |
| social_capital | 网络、信任、结构洞 | 人脉资源、组织协作、信息套利 |
| incentive_design | 动机、委托代理、锦标赛 | 绩效体系、股权设计、团队激励 |
| linguistics | 符号、意义、语境 | 品牌传播、用户理解、语义场 |

### 战略与创新

| 领域 | 核心结构 | 适用场景 |
|------|----------|----------|
| military_strategy | 机动、后勤、OODA | 市场竞争、战略纵深、快速决策 |
| innovation_theory | 颠覆性、S曲线、网络效应 | 技术战略、市场进入、平台竞争 |
| kaizen | 持续改善、浪费消除、现场 | 运营优化、质量提升、流程精简 |
| antifragility | 反脆弱、选择权、凸性 | 风险管理、不确定性收益、韧性建设 |
| mythology | 原型、仪式、转化 | 品牌叙事、用户体验、英雄之旅 |

## 领域选择逻辑

系统基于 Domain A 的 Objects 和 Morphisms 拓扑结构，匹配最合适的 Domain B：

### 按问题类型

- **信息不足/不透明** → yoneda_probe 模块 + quantum_mechanics, social_capital
- **环境变化/策略调整** → natural_transformation 模块 + evolutionary_biology, innovation_theory
- **多方案选择/资源分配** → game_theory, operations_research, behavioral_economics
- **团队协作/组织设计** → distributed_systems, social_capital, incentive_design
- **风险管理/不确定性** → antifragility, complexity_science, second_order_thinking
- **用户行为/决策** → behavioral_economics, neuroscience, mythology
- **竞争战略/市场进入** → military_strategy, game_theory, innovation_theory
- **效率优化/流程改进** → kaizen, operations_research, control_systems

### 按关键词触发

- "不确定"、"叠加"、"纠缠" → quantum_mechanics
- "涌现"、"临界点"、"幂律" → complexity_science
- "反馈"、"延迟"、"二阶效应" → second_order_thinking, control_systems
- "生态"、"共生"、"承载力" → ecology
- "颠覆"、"S曲线"、"创新者窘境" → innovation_theory
- "反脆弱"、"期权"、"凸性" → antifragility
- "OODA"、"战略"、"纵深" → military_strategy
- "精益"、"浪费"、"持续改善" → kaizen
- "网络"、"信任"、"结构洞" → social_capital
- "激励"、"锦标赛"、"委托代理" → incentive_design

## 添加自定义领域

1. 复制 `_template.md` 到 `custom/` 目录
2. 按模板填写内容（Core Objects, Core Morphisms, Theorems）
3. 确保包含 Applicable_Structure 和 Mapping_Hint
4. 使用 `/morphism-config validate` 验证格式

## 多域交叉验证

当使用 3+ 个 Domain B 时，自动挂载 `limits_colimits` 模块提取跨域元逻辑。

推荐组合：
- **竞争战略**: game_theory + military_strategy + innovation_theory
- **组织设计**: distributed_systems + social_capital + incentive_design
- **用户洞察**: behavioral_economics + neuroscience + mythology
- **风险管理**: antifragility + complexity_science + second_order_thinking
