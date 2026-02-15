# Simulation Mode Guide (模拟模式指南)

> 本文档仅用于 `bootstrap_contract` 进入 `FALLBACK` 时。  
> 目标不是“简化流程”，而是在无 Team API 条件下**等价模拟 Swarm 协议**。

## 1. 入口条件（唯一）

仅当 `TeamCreate` 返回 `Feature not available`（或等效 Team 功能不可用）时允许进入模拟模式。

- 若返回 `Already leading team XXX`：必须复用 team，继续 Swarm，禁止进入本模式。
- 若用户要求“生产模式”，仍应先尝试 TeamCreate，再按上述条件决定。

## 2. 协议对齐目标

Fallback 必须保持与 Swarm 相同的关键机制：

1. Domain 输出严格 JSON（`domain_mapping_result.v1`）
2. Obstruction Round 1 -> Round 2 门禁闭环
3. Synthesizer 交换图校验 + Limit/Colimit
4. `OBSTRUCTION_GATE_CLEARED` 前禁止最终整合
5. `message_id` + ACK 握手 + 超时重试
6. 产物路径与字段尽量与主流程一致

## 3. 角色模拟（单 AI 多角色）

单 AI 顺序执行时，必须显式标注当前角色上下文：

- `ROLE=team-lead`：流程控制、门禁判定、持久化
- `ROLE=domain-agent[{domain}]`：单域映射 JSON 产出
- `ROLE=obstruction-theorist`：Schema Gate + 风险分层审查
- `ROLE=synthesizer`：交换图计算与最终整合

禁止在未切换角色语义时混写结论。

## 4. 状态机（Fallback 等价版）

`FALLBACK_INIT -> DOMAIN_ROUND1 -> OBSTRUCTION_ROUND1 -> (REVISION_LOOP)* -> GATE_CLEARED -> SYNTHESIS -> DONE`

### 状态约束

- `DOMAIN_ROUND1`：所有 active domains 必须先产出 round1 JSON
- `OBSTRUCTION_ROUND1`：必须覆盖所有 active domains 才能进入下一步
- `REVISION_LOOP`：存在 `REVISE/REJECT` 才进入；修正后必须复审
- `GATE_CLEARED`：仅当所有 active domains `PASS`（或显式剔除并记因）才成立
- `SYNTHESIS`：仅在 `GATE_CLEARED` 后执行

## 5. ACK 握手（本地模拟版，必须）

即使单 AI 顺序执行，也必须落地 ACK 记录，确保可审计可定位。

### 5.1 Domain 发送事件

每个 domain round1 结果必须生成同一 `message_id` 并写入“发送事件”：

- `MAPPING_RESULT_ROUND1 -> obstruction-theorist`
- `MAPPING_RESULT_JSON -> synthesizer`

### 5.2 ACK 事件

必须写入两类 ACK：

- `OBSTRUCTION_ACK_RECEIVED` + `OBSTRUCTION_DELIVERY_ACK`
- `SYNTHESIZER_ACK_RECEIVED` + `SYNTHESIZER_DELIVERY_ACK`

若缺 ACK 或 `message_id` 缺失：

- 记录 `DELIVERY_ACK_TIMEOUT`
- 对应消息重发一次（同一 `message_id`）
- 标记域状态 `DELIVERY_BLOCKED` 并优先排障

### 5.3 推荐 ACK 日志文件

- `logs/message_events.jsonl`
- 每行一条事件，字段建议：
  - `timestamp`
  - `role`
  - `event_type`
  - `domain`
  - `message_id`
  - `status`
  - `details`

## 6. 顺序执行流程（与 Swarm 同构）

### Step A: Team Lead 提取骨架并选域

输出：

- `metadata.json`（包含 `problem`、`selected_domains`、`mode=fallback`）
- `category_skeleton.json`

### Step B: Domain Round 1（逐域）

每个域必须：

1. 读取 `references/{domain}_v2.md` 或 `references/custom/{domain}_v2.md`
2. 输出 `domain_mapping_result.v1` JSON
3. 生成并记录双发送 + 双 ACK 事件
4. 持久化 `domain_results/{domain}_round1.json`

### Step C: Obstruction Round 1（全集中审查）

对所有 active domains 执行：

1. Schema Gate（含 evidence section 覆盖）
2. 风险分层审查（LOW/MEDIUM/HIGH）
3. 输出每域反馈：`obstruction_feedbacks/{domain}_obstruction.json`
4. 输出汇总：`obstruction_feedbacks/OBSTRUCTION_ROUND1_SUMMARY.json`
5. 写入信号：`OBSTRUCTION_ROUND1_COMPLETE`

### Step D: Revision Loop（仅在需要时）

若任一域 `REVISE/REJECT`：

1. 该域进入 round2 修正：`domain_results/{domain}_round2.json`
2. Obstruction 对该域复审并更新反馈
3. 循环直到 `PASS` 或达到终止阈值

### Step E: Gate 判定

仅当以下条件满足才写入 `OBSTRUCTION_GATE_CLEARED`：

- active domains 全部 `PASS`，或
- 显式剔除部分域并记录剔除理由与影响范围

### Step F: Synthesizer 计算

输入只允许消费结构化 JSON（Domain + Obstruction 输出）。

执行：

1. Commutativity 计算（pairwise + verdict）
2. Limit / Colimit 生成
3. 非交换场景输出 bifurcation

输出：

- `commutative_checks/round1_commutativity.json`（或最新 round 命名）
- `final_reports/synthesis.json`（最终结构化结论）

## 7. 持久化最低清单（升级版）

- `metadata.json`
- `category_skeleton.json`
- `domain_results/{domain}_round1.json`（必要时 `round2+`）
- `obstruction_feedbacks/{domain}_obstruction.json`
- `obstruction_feedbacks/OBSTRUCTION_ROUND1_SUMMARY.json`
- `obstruction_feedbacks/overall_obstruction_summary.json`（若可生成）
- `synthesizer_inputs/synthesis_input.json`（或 `preliminary_synthesis.json`）
- `commutative_checks/round1_commutativity.json`
- `final_reports/synthesis.json`
- `logs/message_events.jsonl`（ACK 与重试审计）

## 8. 阻塞恢复（Fallback 版）

若合成阶段未能生成 `SYNTHESIS_RESULT_JSON`：

1. 标记 `SYNTHESIS_BLOCKED`
2. 记录缺失输入或门禁状态
3. 继续按“催促/重试/升级”语义推进
4. 禁止 Team Lead 直接代写最终整合结论

## 9. 无效结果判定

以下任一条件满足则本轮无效，必须重跑对应阶段：

- 缺失 `domain_file_hash`
- 缺失 `kernel_loss`
- `evidence_refs` 未覆盖 `Fundamentals/Core Morphisms/Theorems`
- 输出不是合法 `domain_mapping_result.v1` JSON 主体
- `OBSTRUCTION_GATE_CLEARED` 前已执行最终 synthesis
- ACK 未闭环（存在 `DELIVERY_BLOCKED` 未处理）

## 10. 与 Swarm 的差异边界（仅基础设施差异）

允许不同：

- 无真实 Team API / 无真实并行消息传输

不允许不同：

- 门禁规则
- 输出契约
- Obstruction 参与深度
- Synthesizer 交换图计算
- 角色边界（Lead 不代写结论）
