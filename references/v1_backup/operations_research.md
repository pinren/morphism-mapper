# Domain: Operations Research
# Source: George Dantzig, John von Neumann, Leonid Kantorovich, Russell Ackoff
# Structural_Primitives: optimization, constraint, objective_function, linear_programming, queue

## Core Objects
- **Decision Variable**: 决策者可控制的变量，其取值决定方案优劣
- **Objective Function**: 需要最大化或最小化的目标（利润、成本、时间等）
- **Constraint**: 限制决策可行域的条件（资源、时间、法规等）
- **Feasible Region**: 满足所有约束的解空间
- **Optimal Solution**: 在可行域中使目标函数最优的决策点

## Core Morphisms
- **Optimization**: 在约束条件下寻找目标函数的最优值
- **Sensitivity Analysis**: 参数变化对最优解的影响程度
- **Shadow Price**: 约束条件右端项增加一个单位时目标函数的改进量
- **Trade-off**: 多个目标之间的权衡，帕累托前沿上的非支配解
- **Decomposition**: 将复杂问题分解为子问题，分别优化后协调

## Theorems / Patterns

### 1. Linear Programming Duality
**内容**: 每个线性规划问题（原问题）都有对应的对偶问题，原问题最优值 = 对偶问题最优值（强对偶定理）

**Applicable_Structure**: 资源分配与定价的对应关系，最小成本与最大收益的等价

**Mapping_Hint**: 映射到"资源预算与市场定价的双向验证"、"成本中心与利润中心的平衡"、"约束条件的价值评估"

**Case_Study**: 生产计划问题中，对偶变量的影子价格揭示原材料的边际价值，指导采购决策

### 2. Little's Law
**内容**: 在稳态系统中，平均在制品数量 L = 到达率 λ × 平均停留时间 W

**Applicable_Structure**: 任何具有流入、处理和流出的排队系统

**Mapping_Hint**: 映射到"库存管理与周转率"、"客服中心人员配置"、"产品开发 pipeline 的 WIP 控制"

**Case_Study**: 丰田生产系统通过限制 WIP（看板机制）强制暴露瓶颈，缩短整体生产周期

### 3. Pareto Principle (80/20 Rule)
**内容**: 在许多现象中，约80%的结果来自20%的原因，分布高度不均

**Applicable_Structure**: 资源、收益、问题等分布不均匀的场景

**Mapping_Hint**: 映射到"客户细分与重点服务"、"产品功能优先级"、"质量问题根因分析"

**Case_Study**: 零售业中，通常20%的商品贡献80%的销售额，指导库存和促销策略

### 4. Critical Path Method (CPM)
内容: 项目网络中最长的路径决定最短完成时间，关键路径上的任务延误直接导致项目延期

**Applicable_Structure**: 多任务并行、存在依赖关系的项目管理

**Mapping_Hint**: 映射到"产品开发里程碑规划"、"供应链协调"、"组织变革的时序安排"

**Case_Study**: 阿波罗登月计划使用关键路径法协调2万家企业、40万人员、700万零件的复杂项目

### 5. Newsvendor Model
**内容**: 在需求不确定且产品易逝（报纸、机票、时装）时，存在最优订货量平衡缺货成本与过剩成本

**Applicable_Structure**: 一次性决策、需求不确定、过剩库存价值大幅贬值的场景

**Mapping_Hint**: 映射到"新产品首单生产量"、"促销活动备货"、"季节性产品采购"、"云计算资源预留"

**Case_Study**: 航空公司使用超售策略（overbooking）应对乘客爽约，基于统计模型优化座位利用率

## Tags
- operations_research
- optimization
- linear_programming
- queueing_theory
- critical_path
- pareto
- inventory
- scheduling
- constraint
- decision_analysis
