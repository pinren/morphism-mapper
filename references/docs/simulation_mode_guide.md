# Simulation Mode Guide (No-ACK)

仅在 `TeamCreate` 返回 Team 不可用时使用。  
目标：在无 Team API 下，保持与 Swarm 同构流程，但不使用 ACK 机制。

## 1. 入口

- 合法：`Feature not available`
- 非法：因为“流程太重/更实用”而绕过 Swarm

## 2. 等价目标

1. Domain 输出严格 JSON
2. obstruction 先审后 clear
3. synthesizer 做交换图整合
4. `OBSTRUCTION_GATE_CLEARED` 前禁止 final synthesis

## 3. 状态机

`FALLBACK_INIT -> DOMAIN_ROUND1 -> OBSTRUCTION_ROUND1 -> (REVISION_LOOP)* -> GATE_CLEARED -> SYNTHESIS -> DONE`

## 4. 执行顺序（无 ACK）

1. Lead 产出 `metadata.json` + `category_skeleton.json`
2. 运行 `scripts/domain_selector.py`（或等价 helper）并记录 `DOMAIN_SELECTION_EVIDENCE`
3. Domain round1 双投递（obstruction + synthesizer）
4. obstruction round1 审查并输出 `OBSTRUCTION_ROUND1_COMPLETE`
5. 必要时修正轮
6. obstruction 发 `OBSTRUCTION_GATE_CLEARED`
7. synthesizer 输出 `SYNTHESIS_RESULT_JSON`

## 5. mailbox 驱动

用消息事件推进，不依赖 ACK：

- domain 发送映射消息
- obstruction 发布反馈/汇总
- synthesizer 发布初稿/最终结果

Lead 通过事件是否出现来推进下一步。

## 6. 持久化最小清单

- `metadata.json`
- `category_skeleton.json`
- `domain_results/{domain}_round1.json`（必要时 round2+）
- `obstruction_feedbacks/{domain}_obstruction.json`
- `obstruction_feedbacks/OBSTRUCTION_ROUND1_SUMMARY.json`
- `final_reports/synthesis.json`
- `logs/message_events.jsonl`（消息轨迹，不含 ACK 字段）
