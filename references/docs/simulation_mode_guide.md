# Simulation Mode Guide (模拟模式指南)

> 本文档仅用于 `bootstrap_contract` 进入 `FALLBACK` 时。

## 入口条件（唯一）

只有当 `TeamCreate` 返回 `Feature not available`（或等效 Team 功能不可用）时，才允许进入模拟模式。

若是 `Already leading team XXX`，必须复用 team，不得进入模拟模式。

## 协议来源

- 启动协议：`references/docs/bootstrap_contract.md`
- 输出结构：`assets/agents/schemas/domain_mapping_result.v1.json`
- 版本来源：`assets/version.json`

## 核心原则

1. 即使是模拟模式，也必须输出严格 JSON（`domain_mapping_result.v1`）
2. 即使是模拟模式，也必须读取领域文件并记录 `domain_file_hash`
3. 即使是模拟模式，也必须持久化所有中间结果

## 单 AI 顺序执行流程

1. Team Lead 角色：提取 Category Skeleton + 领域选择
2. Domain Agent 角色（逐个）：
   - 读取 `references/{domain}_v2.md`
   - 产出严格 JSON 映射结果
   - 字段必须包含 `domain_file_path`、`domain_file_hash`、`evidence_refs`、`kernel_loss`
3. Obstruction 角色：执行 schema gate + 五维十四式审查
4. Synthesizer 角色：仅消费 JSON，执行交换图校验 + Limit/Colimit
5. 生成最终报告并持久化

## 持久化最低清单

- `domain_results/{domain}_round1.json`
- `obstruction_feedbacks/{domain}_review.json`
- `commutative_checks/diagram_report.json`
- `final_reports/final_report.md`

## 无效结果判定

以下任一条件满足则结果无效，必须重跑：

- 缺失 `domain_file_hash`
- 缺失 `kernel_loss`
- 输出不是合法 JSON 主体
- 未标记 `schema_version: domain_mapping_result.v1`
