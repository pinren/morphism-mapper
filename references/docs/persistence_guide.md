# Persistence Guide (持久化指南)

**Morphism Mapper v4.5+ 强制持久化与权限管理规范**

## 核心架构

- **按问题组织**: `~/.morphism_mapper/explorations/{timestamp}_{problem_slug}/`
- **自动索引**: 所有探索自动记录在 `~/.morphism_mapper/explorations/index.json`
- **软链接**: `~/.morphism_mapper/explorations/latest` 指向最新探索

---

## 🚨 强制执行规则

### 规则 1: 写入权限前置检查

**在启动任何分析之前，Team Lead 必须执行以下检查**:

```python
import os

def check_persistence_prerequisites():
    """
    检查持久化前提条件
    Returns: (bool, str) - (是否通过, 错误信息)
    """
    base_path = os.path.expanduser("~/.morphism_mapper")
    
    # 1. 检查目录是否存在或可创建
    try:
        os.makedirs(base_path, exist_ok=True)
    except PermissionError:
        return False, f"❌ 无法创建目录 {base_path}：权限被拒绝"
    except Exception as e:
        return False, f"❌ 无法创建目录 {base_path}：{str(e)}"
    
    # 2. 检查写入权限
    test_file = os.path.join(base_path, ".write_test")
    try:
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
    except PermissionError:
        return False, f"❌ 没有写入权限：{base_path}"
    except Exception as e:
        return False, f"❌ 写入测试失败：{str(e)}"
    
    return True, "✅ 持久化权限检查通过"

# 在 Step 0 执行
passed, message = check_persistence_prerequisites()
if not passed:
    # 必须向用户申请权限，不能继续
    request_user_permission(message)
```

### 规则 2: 按需申请写入权限

**如果权限检查失败，必须停止分析并向用户申请权限**:

```markdown
⚠️ **权限申请通知**

Morphism Mapper 需要写入权限以保存分析结果。这是 v4.5+ 的强制要求。

**需要访问的目录**:
- `~/.morphism_mapper/explorations/` - 保存所有探索记录
- `~/.morphism_mapper/explorations/index.json` - 探索索引

**为什么需要写入权限**:
1. **多轮迭代依赖**: Round 2 需要读取 Round 1 的结果
2. **历史追踪**: 支持回顾和对比多次分析
3. **质量保证**: Obstruction Theorist 需要审查历史输出
4. **审计合规**: 所有分析过程可追溯

**可选方案**:
- **方案 A**: 授予 `~/.morphism_mapper/` 目录的写入权限（推荐）
- **方案 B**: 指定自定义路径，需提供该路径的写入权限
- **方案 C**: 使用临时模式（不推荐，功能受限，无法多轮迭代）

请授权或选择方案，分析将在获得权限后继续。
```

### 规则 3: 临时模式降级（仅应急）

**如果用户拒绝授权，可以进入临时模式，但功能受限**:

```python
class PersistenceMode:
    FULL = "full"           # 完整持久化（推荐）
    TEMPORARY = "temporary" # 临时模式（功能受限）
    MEMORY_ONLY = "memory"  # 仅内存（单轮，不推荐）

def set_persistence_mode(mode: PersistenceMode):
    """
    设置持久化模式
    """
    if mode == PersistenceMode.FULL:
        os.environ["MORPHISM_PERSISTENCE_MODE"] = "full"
        os.environ["MORPHISM_EXPLORATION_PATH"] = create_exploration_dir(problem)
    elif mode == PersistenceMode.TEMPORARY:
        os.environ["MORPHISM_PERSISTENCE_MODE"] = "temporary"
        # 使用 /tmp，但用户会被警告
        temp_path = f"/tmp/morphism_mapper_{timestamp}"
        os.environ["MORPHISM_EXPLORATION_PATH"] = temp_path
        print("⚠️ 警告：使用临时模式，分析结果将在会话结束后丢失")
        print("⚠️ 限制：无法执行多轮迭代（Round 2 需要 Round 1 的历史文件）")
    elif mode == PersistenceMode.MEMORY_ONLY:
        os.environ["MORPHISM_PERSISTENCE_MODE"] = "memory"
        print("🚨 警告：使用内存模式，仅限单轮分析")
        print("🚨 Obstruction Theorist 将无法审查历史输出")
```

---

## 📋 权限检查清单

**Team Lead 必须在分析开始前确认**:

- [ ] **目录权限**: `~/.morphism_mapper/` 目录可创建/可写入
- [ ] **子目录权限**: `explorations/`、`domain_results/` 等子目录可创建
- [ ] **文件权限**: 可以创建和修改 `.json` 文件
- [ ] **索引更新**: 可以更新 `index.json` 索引文件
- [ ] **软链接**: 可以创建/更新 `latest` 软链接（非 Windows）

---

## 失败恢复机制与合规

### 失败恢复

**如果写入过程中失败，必须优雅降级**:

```python
def safe_write_file(filepath: str, content: str, max_retries: int = 3):
    """
    安全写入文件，失败时提供恢复选项
    """
    for attempt in range(max_retries):
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已保存: {filepath}")
            return True
            
        except PermissionError as e:
            print(f"❌ 写入失败 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                # 最终失败，提供备选方案
                print("\n⚠️ 无法持久化，备选方案：")
                print(f"1. 手动创建目录: mkdir -p {os.path.dirname(filepath)}")
                print(f"2. 更改路径权限: chmod 755 {os.path.dirname(filepath)}")
                print(f"3. 使用内存模式继续（功能受限）")
                return False
        except Exception as e:
            print(f"❌ 意外错误: {e}")
            return False
```

### 🚫 禁止行为 (Critical Violations)

以下行为在 v4.5.2+ 中被视为严重违规：

| 违规行为 | 风险等级 | 后果 |
|---------|---------|------|
| **跳过权限检查直接分析** | 🔴 Critical | 可能导致 Round 2 无法读取 Round 1 结果 |
| **在内存中缓存而不写入** | 🔴 Critical | 进程重启后所有分析丢失 |
| **用户拒绝授权后仍强制继续** | 🟡 High | 用户体验差，分析质量无法保证 |
| **使用 `/tmp` 而不告知用户** | 🟡 High | 临时文件可能被清理，用户不知情 |
| **写入失败时静默忽略** | 🔴 Critical | 用户误以为已保存，实际未持久化 |

---

## 各 Agent 的持久化责任

### 1. Domain Agent (ROUND 1)

**输出要求**:
```yaml
# MAPPING_RESULT_ROUND1必须包含：
domain: "domain_name"
timestamp: "ISO 8601格式"
round: 1
problem: "原始问题"
category_skeleton:
  objects: [...]
  morphisms: [...]
concept_mapping: {...}
insights: [...]
verification_proof: {...}
confidence_assessment: {...}
```

**保存指令**:
```
===SAVE_TO_FILE===
filepath: ${MORPHISM_EXPLORATION_PATH}/domain_results/{domain}_round1.json
content: <完整JSON内容>
```

### 2. Obstruction Theorist

**输入**: 读取 `${MORPHISM_EXPLORATION_PATH}/domain_results/{domain}_round1.json`

**输出要求**:
```json
{
  "obstruction_id": "{domain}_round1",
  "theorist": "obstruction-theorist",
  "agent_target": "{domain}",
  "attack_matrix": { ... },
  "feedback": {
    "status": "REQUIRES_REVISION | PASS",
    "critical_issues": [...],
    "revision_requirements": [...]
  },
  "diagnosis": "30字风险预警",
  "risk_tags": [...]
}
```

**保存指令**:
```
===SAVE_TO_FILE===
filepath: ${MORPHISM_EXPLORATION_PATH}/obstruction_feedbacks/{domain}_obstruction.json
```

### 3. Domain Agent (ROUND 2)

**输入**（必须读取）:
1. 自己的第一轮输出: `${MORPHISM_EXPLORATION_PATH}/domain_results/{domain}_round1.json`
2. Obstruction反馈: `${MORPHISM_EXPLORATION_PATH}/obstruction_feedbacks/{domain}_obstruction.json`

**输出要求**:
```json
{
  "round": 2,
  "obstruction_response": {
    "addressed_issues": [...],
    "defense_strategy": "..."
  },
  "refined_mapping": { ... },
  "proposal": {
    "title": "...",
    "steps": [...]
  }
}
```

**保存指令**:
```
===SAVE_TO_FILE===
filepath: ${MORPHISM_EXPLORATION_PATH}/domain_results/{domain}_round2.json
```
