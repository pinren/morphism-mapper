---
name: morphism-mapper
description: Category Theory Morphism Mapper v4.8 Swarm Mode（no-ack）。用于复杂问题的跨领域并行推理：TeamCreate 探测、团队级启动、Domain 严格 JSON 输出、Obstruction 审查、Synthesizer 交换图整合。流程由 SendMessage + mailbox 推进，不依赖 ACK 机制。
---

# Morphism Mapper v4.8（no-ack）

本版关键变化：去掉 ACK 机制，改为 mailbox 驱动。

## 1. 最小流程

1. 检查并初始化持久化，产出 `PERSISTENCE_READY`（固定根目录：`~/.morphism_mapper/explorations/...`）
2. 严格按可视化契约落盘：必须产出 `session_manifest.json` + `mailbox_events.ndjson`（禁止 legacy 事件主路径）
3. 同一 run 只允许一个持久化目录：`session_id` 必须等于目录名，格式 `YYYYMMDDTHHMMSSZ_xxxxxx_slug`
4. `TeamCreate`
5. 运行 `scripts/domain_selector.py`（或 `helpers.call_domain_selector`）并产出 `DOMAIN_SELECTION_EVIDENCE`
6. 构建首批 roster（core + selected domains）
7. 团队级首批启动
8. 等 core mailbox 就绪信号：
   - `OBSTRUCTION_PIPELINE_READY`
   - `SYNTHESIS_PIPELINE_READY`
9. 广播 `CATEGORY_SKELETON`
10. domain 双投递（obstruction + synthesizer）
11. obstruction `OBSTRUCTION_ROUND1_COMPLETE`
12. `OBSTRUCTION_GATE_CLEARED` 后请求 final synthesis
13. final 交付前执行 `scripts/validate_session_contract.py ${MORPHISM_EXPLORATION_PATH}` 并通过

## 2. 规则

1. TeamCreate 成功后禁止非法 fallback。
2. 未产出 `DOMAIN_SELECTION_EVIDENCE` 前，禁止进入首批启动。
3. 首批禁止 Lead 手动逐个 Task 启动。
4. `Task(..., team_name, subagent_type)` 不是团队级首批启动。
5. 流程推进不使用 ACK，不做 ACK 超时重发闭环。
6. Lead 只编排，不代替 core 干活。
7. obstruction 必须输出字段级实质审查（schema/errors/consistency/attack_findings），空 clear 不放行。
8. 不论 Swarm 还是 Fallback，未产出 `PERSISTENCE_READY` 前禁止进入分析阶段。
9. 禁止写入项目目录（cwd/workspace）和 `/tmp`；仅允许写入 `${MORPHISM_EXPLORATION_PATH}`。
10. 任意关键写入失败必须执行 failover 持久化；仅当主写入与 failover 均失败时中止并报错。

## 3. Domain 输出约束

- 必须是 `domain_mapping_result.v1` JSON
- 先读 skill 内 `references/` 绝对路径，再回退相对路径
- 必须双投递（obstruction + synthesizer）

## 4. mailbox 推进判据

Lead 通过消息出现推进，而非 ACK：

- core ready 信号出现
- obstruction 反馈出现
- synthesizer 初稿或拒收出现
- obstruction gate clear 出现
- synthesis final 出现

## 5. 关键文件

- `references/docs/bootstrap_contract.md`
- `references/docs/visualization_contract.md`
- `references/docs/persistence_guide.md`
- `assets/agents/system_prompts/leader.md`
- `assets/agents/system_prompts/domain_template.md`
- `assets/agents/system_prompts/obstruction.md`
- `assets/agents/system_prompts/synthesizer.md`
- `assets/agents/schemas/domain_mapping_result.v1.json`
- `assets/agents/schemas/session_manifest.v1.json`
- `assets/agents/schemas/mailbox_event.v1.json`
- `scripts/validate_session_contract.py`
