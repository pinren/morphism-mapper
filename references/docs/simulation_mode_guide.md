# Simulation Mode Guide (No-ACK)

仅在 `TeamCreate` 返回 Team 不可用时使用。  
目标：在无 Team API 下，保持与 Swarm 同构流程，但不使用 ACK 机制，并保持同等级持久化约束。

可视化契约强制要求：`references/docs/visualization_contract.md`。

重要：Fallback 不允许简化文件集；必须与 Swarm 输出同一套 JSON 路径，仅字段值允许模式差异。

## 1. 入口

- 合法：`Feature not available`
- 非法：因为“流程太重/更实用”而绕过 Swarm

## 2. 等价目标

1. Domain 输出严格 JSON
2. obstruction 先审后 clear
3. synthesizer 做交换图整合
4. `OBSTRUCTION_GATE_CLEARED` 前禁止 final synthesis
5. 持久化要求与 Swarm 完全一致（必须先通过 `PERSISTENCE_READY`）
6. 占位符门禁：禁止模板文本（如“定理名称/映射依据/引用或摘要”）通过 obstruction 放行

## 3. 状态机

`FALLBACK_INIT -> PERSISTENCE_READY -> DOMAIN_ROUND1 -> OBSTRUCTION_ROUND1 -> (REVISION_LOOP)* -> GATE_CLEARED -> SYNTHESIS -> DONE`

## 4. 执行顺序（无 ACK）

1. 初始化 `${MORPHISM_EXPLORATION_PATH}`，产出 `PERSISTENCE_READY`
1.1 仅 Lead 允许创建目录；目录名必须为 `session_id`（`YYYYMMDDTHHMMSSZ_xxxxxx_slug`）
1.2 同一 run 严禁二次创建目录，后续阶段必须复用同一个 `${MORPHISM_EXPLORATION_PATH}`
1.3 通过 `MORPHISM_RUN_ID` 绑定目录，所有 agent 进程必须复用同一个 `MORPHISM_RUN_ID`
2. Lead 产出 `${MORPHISM_EXPLORATION_PATH}/metadata.json` + `${MORPHISM_EXPLORATION_PATH}/category_skeleton.json`
2.1 Lead 同步产出 `${MORPHISM_EXPLORATION_PATH}/session_manifest.json`（`run_mode=fallback`）
3. 运行 `scripts/domain_selector.py`（或 `helpers.call_domain_selector`）并记录 `DOMAIN_SELECTION_EVIDENCE`
4. Domain round1 双投递（obstruction + synthesizer）
5. obstruction round1 审查并输出 `OBSTRUCTION_ROUND1_COMPLETE`
6. 必要时修正轮
7. obstruction 发 `OBSTRUCTION_GATE_CLEARED`
8. synthesizer 输出 `SYNTHESIS_RESULT_JSON`

## 5. mailbox 驱动

用消息事件推进，不依赖 ACK：

- domain 发送映射消息
- obstruction 发布反馈/汇总
- synthesizer 发布初稿/最终结果

Lead 通过事件是否出现来推进下一步。

事件聚合落盘要求（必须）：

- 所有关键业务事件必须写入 `${MORPHISM_EXPLORATION_PATH}/mailbox_events.ndjson`
- 每行字段至少包含：`timestamp/signal/actor/target/domain/payload_ref/summary`
- 禁止以 `logs/message_events.jsonl` 作为主事件源

## 6. 持久化门禁（必须）

必须满足：

- `MORPHISM_EXPLORATION_PATH` 位于 `~/.morphism_mapper/explorations/` 目录树下
- 可创建并写入：`domain_results/`、`obstruction_feedbacks/`、`final_reports/`、`logs/`
- 严禁写入项目目录（cwd/workspace）和 `/tmp`
- 任意关键写入失败必须先执行 failover 持久化，仅当主写入与 failover 都失败才中止

## 7. 持久化最小清单

- `${MORPHISM_EXPLORATION_PATH}/session_manifest.json`
- `${MORPHISM_EXPLORATION_PATH}/mailbox_events.ndjson`
- `${MORPHISM_EXPLORATION_PATH}/metadata.json`
- `${MORPHISM_EXPLORATION_PATH}/category_skeleton.json`
- `${MORPHISM_EXPLORATION_PATH}/domain_results/{domain}_round1.json`（必要时 round2+）
- `${MORPHISM_EXPLORATION_PATH}/obstruction_feedbacks/{domain}_obstruction.json`
- `${MORPHISM_EXPLORATION_PATH}/obstruction_feedbacks/OBSTRUCTION_ROUND1_SUMMARY.json`
- `${MORPHISM_EXPLORATION_PATH}/final_reports/synthesis.json`
- `${MORPHISM_EXPLORATION_PATH}/launch_evidence.json`（fallback 等价证据）
