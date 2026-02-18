# Strict Mode 最小重跑模板

用于重跑并确保新 run 满足严格模式（domain schema + session contract 双门禁）。

## 1) 预设环境（新 run）

在 skill 根目录执行：

```bash
cd /Users/pinren/.claude/skills/morphism-mapper

export MORPHISM_RUN_ID="$(python3 - <<'PY'
from datetime import datetime
import os
print(datetime.utcnow().strftime('%Y%m%dT%H%M%SZ') + '_' + os.urandom(3).hex())
PY
)"
export MORPHISM_SESSION_SLUG="mother_in_law_daughter_in_law"
unset MORPHISM_EXPLORATION_PATH
```

## 2) 初始化持久化目录（必须）

```bash
python3 - <<'PY'
from scripts.helpers import ensure_exploration_path
print(ensure_exploration_path("mother_in_law_daughter_in_law"))
PY
```

记录输出路径为 `${MORPHISM_EXPLORATION_PATH}`，后续所有 agent 必须复用该目录。

## 3) 先做 skeleton 提取 + 选域（必须）

```bash
python3 scripts/prepare_domain_selection.py \
  --topic "婆媳关系" \
  --session-path "${MORPHISM_EXPLORATION_PATH}" \
  --top-n 6
```

这一步会强制写入：

- `category_skeleton.json`
- `category_extraction_evidence.json`
- `domain_selection_evidence.json`
- `artifacts/domain_selection/selector_input.json`
- `artifacts/domain_selection/selector_output.json`
- `artifacts/domain_selection/domain_catalog_snapshot.json`
- `artifacts/domain_selection/domain_knowledge_snapshot.json`
- `mailbox_events.ndjson` 中的 `CATEGORY_SKELETON_EXTRACTED` 与 `DOMAIN_SELECTION_EVIDENCE`

## 4) 运行会话（Swarm 或 Fallback）

- 按 `SKILL.md` 与 `bootstrap_contract.md` 执行完整流程。
- 每个 domain round 结果落盘后，立即执行一次 domain 门禁（替换 `<domain>`）：

```bash
python3 scripts/strict_gate.py --phase domain "${MORPHISM_EXPLORATION_PATH}" --domain <domain>
```

返回非 0：立即阻塞并修正，不得进入 gate clear。

## 5) Final 前总门禁（必须）

```bash
python3 scripts/strict_gate.py --phase final "${MORPHISM_EXPLORATION_PATH}"
```

返回非 0：不得宣布完成。

## 6) 快速定位最近 run（可选）

```bash
ls -1dt /Users/pinren/.morphism_mapper/explorations/* | head -n 3
```
