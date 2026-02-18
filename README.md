# Morphism Mapper

> Swarm Experimental（no-ack mailbox mode）

## 本次调整

- 去除 ACK 机制（core/delivery/final ack 全部移除）
- 改为 `SendMessage + mailbox` 推进
- 保留原有门禁：团队级启动、obstruction 先审、gate clear 后 final synthesis
- obstruction 升级为字段级实审（schema gate + consistency checks + attack findings）
- Swarm/Fallback 统一持久化硬门禁：必须先产出 `PERSISTENCE_READY`，并写入 `~/.morphism_mapper/explorations/...`
- 持久化策略升级为“主写入 + failover 分块包”，覆盖 leader/domain/obstruction/synthesizer
- 可视化契约硬门禁：必须产出 `session_manifest.json` + `mailbox_events.ndjson`（禁止以 legacy 日志作为主事件源）
- run 目录唯一性：同一 run 只允许一个 `${MORPHISM_EXPLORATION_PATH}`，目录名必须等于 `session_id`（`YYYYMMDDTHHMMSSZ_xxxxxx_slug`）
- 新增严格门禁包装器：`scripts/strict_gate.py`（domain schema + session contract 一体化阻断）

## 核心流程

1. 先通过持久化门禁（`PERSISTENCE_READY`）
2. `TeamCreate`
3. 先提取并落盘 `CATEGORY_SKELETON`（推荐 `scripts/prepare_domain_selection.py`）
4. 再运行 `domain_selector.py` 产出 `DOMAIN_SELECTION_EVIDENCE`
5. 团队级首批启动（core + selected domains）
6. core 在 mailbox 发布就绪信号
7. domain 双投递 JSON（给 obstruction + synthesizer）
8. obstruction round1 / gate clear
9. final synthesis

## 现在怎么判定“流程在推进”

不看 ACK，改看 mailbox 中是否出现关键业务消息：

- `OBSTRUCTION_PIPELINE_READY`
- `SYNTHESIS_PIPELINE_READY`
- `OBSTRUCTION_FEEDBACK`
- `OBSTRUCTION_ROUND1_COMPLETE`
- `OBSTRUCTION_GATE_CLEARED`
- `PRELIMINARY_SYNTHESIS` / `SYNTHESIS_RESULT_JSON`

## 关键约束

- 启动前必须有 `CATEGORY_SKELETON_EXTRACTED` 证据（`category_extraction_evidence.json`）
- 启动前必须有 `DOMAIN_SELECTION_EVIDENCE`（默认来自 `scripts/domain_selector.py`）
- 若 `selector_ok=true`，必须有 selector 输入/输出与 domain catalog 证明链，且 `selected_domains` 只能来自 selector 输出
- `selected_domains` 必须都对应现有领域知识文件（`references/*_v2.md`）；否则必须自动替换或阻断
- 首批禁止 Lead 手动逐个 Task 启动
- `Task(..., team_name, subagent_type)` 不等于团队级首批启动
- Lead 不得代替 obstruction/synthesizer
- Domain 仍必须输出严格 JSON schema

## 主要文件

- `SKILL.md`
- `references/docs/bootstrap_contract.md`
- `references/docs/simulation_mode_guide.md`
- `references/docs/visualization_contract.md`
- `assets/agents/system_prompts/leader.md`
- `assets/agents/system_prompts/domain_template.md`
- `assets/agents/system_prompts/obstruction.md`
- `assets/agents/system_prompts/synthesizer.md`
- `assets/agents/schemas/session_manifest.v1.json`
- `assets/agents/schemas/mailbox_event.v1.json`
- `scripts/prepare_domain_selection.py`
- `scripts/strict_gate.py`
- `scripts/validate_session_contract.py`
- `references/docs/strict_rerun_template.md`
