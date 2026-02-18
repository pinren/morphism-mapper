# Persistence Guide (持久化指南)

**Morphism Mapper v5.0 强约束持久化规范（Swarm/Fallback 同标准）**

补充：可视化输出契约见 `references/docs/visualization_contract.md`。

## 1. 单一主持久化策略

Morphism Mapper 只允许一种生产持久化模式：

- 根目录：`~/.morphism_mapper/explorations/`
- 单次探索目录：`~/.morphism_mapper/explorations/{session_id}/`
- `session_id` 格式：`YYYYMMDDTHHMMSSZ_xxxxxx_slug`
- 索引文件：`~/.morphism_mapper/explorations/index.json`
- run 注册表：`~/.morphism_mapper/explorations/run_registry.json`（`run_id -> exploration_path`）
- 最新软链接：`~/.morphism_mapper/explorations/latest`

运行约束：

- Lead 在 run 启动时生成 `MORPHISM_RUN_ID`（格式 `YYYYMMDDTHHMMSSZ_xxxxxx`）。
- 目录创建后，`run_registry.json` 固化 `MORPHISM_RUN_ID -> exploration_path` 映射。
- 同一 run 后续调用必须复用该映射，不允许新建第二目录。

禁止：

- 写入项目目录（cwd/workspace）作为主持久化路径
- 使用 `/tmp` 作为主持久化路径
- memory-only 或 temporary 模式继续生产流程

---

## 2. 启动前硬门禁（必须）

在任何分析开始前（包括 Swarm 和 Fallback），Lead 必须先完成：

```json
{
  "signal": "PERSISTENCE_READY",
  "persistence_mode": "production",
  "exploration_path": "/home/<user>/.morphism_mapper/explorations/<session_id>",
  "writable": true
}
```

若失败：

- 立即阻塞流程并报错
- 标记 `PROTOCOL_BLOCKED_PERSISTENCE_UNAVAILABLE`
- 不允许进入 TeamCreate 之后的任何分析阶段

---

## 3. 参考实现（前置检查 + 初始化）

```python
import json
import os
from pathlib import Path
from datetime import datetime

def ensure_persistence_ready(problem_slug: str) -> str:
    base = Path.home() / ".morphism_mapper" / "explorations"
    base.mkdir(parents=True, exist_ok=True)

    run_id = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ") + "_abc123"
    session_id = f"{run_id}_{problem_slug}"
    exploration = base / session_id
    exploration.mkdir(parents=True, exist_ok=False)

    required_dirs = [
        "domain_results",
        "obstruction_feedbacks",
        "final_reports",
        "logs",
        "artifacts",
    ]
    for d in required_dirs:
        (exploration / d).mkdir(parents=True, exist_ok=True)

    test_file = exploration / ".write_test"
    test_file.write_text("ok", encoding="utf-8")
    test_file.unlink(missing_ok=True)

    index_file = base / "index.json"
    index = []
    if index_file.exists():
        index = json.loads(index_file.read_text(encoding="utf-8"))
    index.append({
        "timestamp": datetime.now().isoformat(),
        "exploration_path": str(exploration)
    })
    index_file.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    latest = base / "latest"
    if latest.exists() or latest.is_symlink():
        latest.unlink()
    latest.symlink_to(exploration, target_is_directory=True)

    os.environ["MORPHISM_EXPLORATION_PATH"] = str(exploration)
    os.environ["MORPHISM_PERSISTENCE_MODE"] = "production"
    return str(exploration)
```

---

## 4. 持久化执行策略（必须）

所有关键产物写入必须满足：

1. 路径前缀为 `${MORPHISM_EXPLORATION_PATH}/`
2. 不得静默丢弃，必须留下可追溯落盘结果（主文件或 failover 包）
3. 写入失败不可自动切换到 `/tmp` 或内存模式
4. 仅当主写入与 failover 写入都失败时，才允许阻塞流程
5. 所有 write 调用必须使用单行压缩 JSON；结果文件 payload 目标 `<= 3500`，硬上限 `<= 6000` 字符
6. `mailbox_events.ndjson` 每行目标 `<= 800`、硬上限 `<= 1200` 字符；禁止内嵌完整正文，只允许 `payload_ref + summary`

```python
import json
import hashlib
from pathlib import Path

def durable_write_json(filepath: str, obj: dict, artifact_type: str) -> dict:
    """
    返回:
      {"status": "PRIMARY_OK" | "DEGRADED_CHUNKED", "path": "..."}
    """
    target = Path(filepath).expanduser().resolve()
    root = Path(os.environ["MORPHISM_EXPLORATION_PATH"]).expanduser().resolve()
    if not str(target).startswith(str(root) + os.sep):
        raise RuntimeError(f"Illegal persistence path: {target}")

    # 主路径：单行 JSON，减小 write 参数解析失败概率
    payload = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    if len(payload) > 6000:
        # 先由业务侧压缩字段，再进入写入；这里仍允许进入 failover
        pass
    json.loads(payload)  # 先做反序列化校验

    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(payload, encoding="utf-8")
        return {"status": "PRIMARY_OK", "path": str(target)}
    except Exception as e:
        # failover：分块持久化，保证“总有东西落盘”
        fail_root = root / "artifacts" / "failover"
        fail_root.mkdir(parents=True, exist_ok=True)
        sha = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        chunks = [payload[i:i+4000] for i in range(0, len(payload), 4000)]
        chunk_files = []
        for idx, chunk in enumerate(chunks):
            cpath = fail_root / f"{artifact_type}.{sha}.part{idx:04d}.jsonl"
            cpath.write_text(chunk, encoding="utf-8")
            chunk_files.append(str(cpath))
        envelope = {
            "status": "DEGRADED_CHUNKED",
            "artifact_type": artifact_type,
            "original_target": str(target),
            "payload_sha256": sha,
            "chunk_count": len(chunk_files),
            "chunk_files": chunk_files,
            "primary_error": str(e),
        }
        env_path = fail_root / f"{artifact_type}.{sha}.envelope.json"
        env_path.write_text(json.dumps(envelope, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": "DEGRADED_CHUNKED", "path": str(env_path)}
```

---

## 5. 全 Agent 最小持久化清单（可视化契约，统一）

必需（缺失即协议违规）：

- `${MORPHISM_EXPLORATION_PATH}/session_manifest.json`
- `${MORPHISM_EXPLORATION_PATH}/mailbox_events.ndjson`
- `${MORPHISM_EXPLORATION_PATH}/metadata.json`
- `${MORPHISM_EXPLORATION_PATH}/category_skeleton.json`
- `${MORPHISM_EXPLORATION_PATH}/category_extraction_evidence.json`
- `${MORPHISM_EXPLORATION_PATH}/domain_selection_evidence.json`
- `${MORPHISM_EXPLORATION_PATH}/launch_evidence.json`（fallback 写入等价字段）
- `${MORPHISM_EXPLORATION_PATH}/domain_results/{domain}_round1.json`
- `${MORPHISM_EXPLORATION_PATH}/domain_results/{domain}_round2.json`（如触发修正轮）
- `${MORPHISM_EXPLORATION_PATH}/obstruction_feedbacks/{domain}_obstruction.json`
- `${MORPHISM_EXPLORATION_PATH}/obstruction_feedbacks/OBSTRUCTION_ROUND1_SUMMARY.json`
- `${MORPHISM_EXPLORATION_PATH}/obstruction_feedbacks/OBSTRUCTION_GATE_CLEARED.json`
- `${MORPHISM_EXPLORATION_PATH}/final_reports/preliminary_synthesis.json`
- `${MORPHISM_EXPLORATION_PATH}/final_reports/synthesis.json`

可选调试：

- `${MORPHISM_EXPLORATION_PATH}/logs/lead_events.jsonl`
- `${MORPHISM_EXPLORATION_PATH}/logs/persistence_events.jsonl`
- `${MORPHISM_EXPLORATION_PATH}/logs/obstruction_events.jsonl`
- `${MORPHISM_EXPLORATION_PATH}/logs/synthesis_events.jsonl`
- `${MORPHISM_EXPLORATION_PATH}/artifacts/failover/*.envelope.json`（仅主写入失败时）

禁止（不再作为主事件流）：

- `${MORPHISM_EXPLORATION_PATH}/logs/message_events.jsonl`

---

## 6. Critical 违规项

| 违规行为 | 违规码 | 处理 |
|---|---|---|
| 未产出 `PERSISTENCE_READY` 就继续 | `PROTOCOL_BREACH_PERSISTENCE_NOT_READY` | 立即中止 |
| 写入项目目录或 `/tmp` | `PROTOCOL_BREACH_ILLEGAL_PERSISTENCE_PATH` | 立即中止 |
| 主写入失败后不做 failover | `PROTOCOL_BREACH_PERSISTENCE_FAILOVER_SKIPPED` | 立即中止 |
| 主写入+failover 都失败仍继续 | `PROTOCOL_BLOCKED_PERSISTENCE_UNAVAILABLE` | 立即中止 |
| 仅保存在内存中 | `PROTOCOL_BREACH_PERSISTENCE_NOT_READY` | 立即中止 |
| 缺失 `session_manifest.json` 或 `mailbox_events.ndjson` | `PROTOCOL_BREACH_VISUALIZATION_ARTIFACT_MISSING` | 立即中止 |
| 使用 `logs/message_events.jsonl` 作为主事件流 | `PROTOCOL_BREACH_LEGACY_EVENT_STREAM` | 立即中止 |
| 同一 run 产生多个探索目录 | `PROTOCOL_BREACH_RUN_DIRECTORY_SPLIT` | 立即中止 |
