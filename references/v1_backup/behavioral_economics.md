# Domain: Behavioral Economics
# Source: Daniel Kahneman, Amos Tversky, Richard Thaler, Dan Ariely
# Structural_Primitives: cognitive_bias, prospect_theory, nudge, mental_accounting, anchoring

## Core Objects
- **Economic Agent**: 具有有限理性、受认知约束的决策者，非传统经济学中的完全理性人
- **Reference Point**: 决策者评估得失的基准，决定效用是收益还是损失
- **Heuristic**: 快速但可能产生偏差的决策捷径（可得性、代表性、锚定）
- **Mental Account**: 心理上对资金进行分类记账，违反 fungibility 原则
- **Choice Architecture**: 选项的呈现方式（默认、排序、框架）影响决策

## Core Morphisms
- **Prospect Evaluation**: 潜在结果 × 权重函数 → 决策价值（非线性概率加权）
- **Loss Aversion**: 损失厌恶，损失的痛苦约为同等收益快乐的2-2.5倍
- **Mental Accounting**: 资金标签化 → 不同账户间的非替代性消费决策
- **Social Proof**: 观察他人行为 → 调整自身决策（从众效应）
- **Present Bias**: 对即时满足的偏好 → 长期规划的折扣

## Theorems / Patterns

### 1. Prospect Theory
**内容**: 人们根据相对于参考点的得失而非最终财富状态做决策；损失厌恶；对小概率事件高估、对中大概率事件低估

**Applicable_Structure**: 涉及风险决策和不确定收益的场景

**Mapping_Hint**: 映射到"产品定价策略"、"会员续费设计"、"损失框架vs收益框架的营销话术"

**Case_Study**: 手术存活率90% vs 死亡率10%的表述导致截然不同的患者选择，尽管数学等价

### 2. Endowment Effect
**内容**: 人们对自己拥有的物品赋予更高价值，放弃所需的补偿 > 获得所愿支付的代价

**Applicable_Structure**: 涉及所有权、试用、退换货政策的商业设计

**Mapping_Hint**: 映射到"免费试用策略"、"无理由退货政策"、"虚拟所有权（定制、预览）"

**Case_Study**: 实验参与者获得咖啡杯后，愿意卖出的价格显著高于未获得者的愿意购买价格

### 3. Hyperbolic Discounting
**内容**: 人们对即时奖励的偏好强于远期，贴现率随时间递减，导致时间不一致的偏好

**Applicable_Structure**: 需要用户延迟满足或坚持长期行为的场景

**Mapping_Hint**: 映射到"订阅制用户留存"、"健身/学习类产品的持续使用"、"储蓄/投资产品设计"

**Case_Study**: 多数人选择今天拿50元而非两周后拿55元，但选择一年后拿55元而非50周5元

### 4. Default Bias
**内容**: 人们倾向于维持默认选项，即使改变的成本很低，默认设置成为强有力的选择架构工具

**Applicable_Structure**: 需要引导用户选择又不剥夺自由意志的场景

**Mapping_Hint**: 映射到"产品默认配置设计"、"隐私设置选项"、"自动续费/升级策略"

**Case_Study**: 器官捐赠同意率在国家间巨大差异，主要由默认选项（加入vs退出）决定，而非文化差异

### 5. Decoy Effect (Asymmetric Dominance)
**内容**: 引入一个明显劣于目标选项的诱饵，改变相对偏好，使目标选项更具吸引力

**Applicable_Structure**: 多选项产品线的定价和设计

**Mapping_Hint**: 映射到"三级定价策略"、"产品组合设计"、"引导用户选择高利润选项"

**Case_Study**: 《经济学人》订阅选项中，引入"仅电子版= $59，仅印刷版= $125，两者= $125"使组合选项销量激增

## Tags
- behavioral_economics
- cognitive_bias
- prospect_theory
- loss_aversion
- nudge
- anchoring
- mental_accounting
- choice_architecture
- heuristics
- irrationality
