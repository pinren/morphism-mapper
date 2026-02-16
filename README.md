# Morphism Mapper

> Swarm Experimental（no-ack mailbox mode）

## 本次调整

- 去除 ACK 机制（core/delivery/final ack 全部移除）
- 改为 `SendMessage + mailbox` 推进
- 保留原有门禁：团队级启动、obstruction 先审、gate clear 后 final synthesis
- obstruction 升级为字段级实审（schema gate + consistency checks + attack findings）

## 核心流程

1. `TeamCreate`
2. 运行 `domain_selector.py` 产出 `DOMAIN_SELECTION_EVIDENCE`
3. 团队级首批启动（core + selected domains）
4. core 在 mailbox 发布就绪信号
5. domain 双投递 JSON（给 obstruction + synthesizer）
6. obstruction round1 / gate clear
7. final synthesis

## 现在怎么判定“流程在推进”

不看 ACK，改看 mailbox 中是否出现关键业务消息：

- `OBSTRUCTION_PIPELINE_READY`
- `SYNTHESIS_PIPELINE_READY`
- `OBSTRUCTION_FEEDBACK`
- `OBSTRUCTION_ROUND1_COMPLETE`
- `OBSTRUCTION_GATE_CLEARED`
- `PRELIMINARY_SYNTHESIS` / `SYNTHESIS_RESULT_JSON`

## 关键约束

- 启动前必须有 `DOMAIN_SELECTION_EVIDENCE`（默认来自 `scripts/domain_selector.py`）
- 首批禁止 Lead 手动逐个 Task 启动
- `Task(..., team_name, subagent_type)` 不等于团队级首批启动
- Lead 不得代替 obstruction/synthesizer
- Domain 仍必须输出严格 JSON schema

## 主要文件

- `SKILL.md`
- `references/docs/bootstrap_contract.md`
- `references/docs/simulation_mode_guide.md`
- `assets/agents/system_prompts/leader.md`
- `assets/agents/system_prompts/domain_template.md`
- `assets/agents/system_prompts/obstruction.md`
- `assets/agents/system_prompts/synthesizer.md`
