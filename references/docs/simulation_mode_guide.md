# Simulation Mode Guide (模拟模式指南)

**当单个 AI 助手扮演所有 Agent 角色时的执行规范**

## 什么是模拟模式？

- ✅ **单个AI助手**扮演所有Agent角色（Team Lead、Obstruction、Synthesizer、Domain Agents）
- ✅ 所有"Agent通信"实际上是**同一会话内的上下文切换**
- ✅ 没有真正的Agent Swarm基础设施（没有独立的Agent进程、没有SendMessage系统）
- ✅ **持久化必须自动执行**（即使模拟模式，分析完成后立即保存文件）

---

## 核心原则：模拟模式也必须自动持久化

**无论生产模式还是模拟模式，持久化都是强制要求。**

```
生产模式：                        模拟模式：
┌──────────────┐                ┌──────────────┐
│ Agent Team   │                │ 单个AI助手   │
│ 多进程并行   │                │ 单一会话     │
│ SendMessage  │                │ 角色扮演     │
│ 自动持久化   │                │ 自动持久化   │ ← 同样要求！
└──────────────┘                └──────────────┘
```

**区别仅在于触发时机**:
- **生产模式**: Agent发送`SaveFile`消息 → 系统自动保存
- **模拟模式**: 我完成每个Agent分析 → **我必须立即执行保存代码**

### 自动执行时机表

**我必须在以下时刻立即保存**:

| 步骤 | 执行时刻 | 保存文件 | 格式 |
|------|---------|---------|------|
| **Step 0** | 分析开始前 | `metadata.json` | JSON |
| **Step 4** | Domain Agents Round 1 完成后 | `{domain}_round1.json` (每个领域一个) | JSON |
| **Step 5** | Obstruction Theorist 审查后 | `{domain}_obstruction.json` (每个领域一个) | JSON |
| **Step 6** | Domain Agents Round 2 修正后 | `{domain}_round2.json` (每个领域一个) | JSON |
| **Step 7** | Synthesizer 整合后 | `synthesis.json` | JSON |
| **Step 8** | 最终报告完成后 | `index.json` + `latest` 软链接 | JSON + symlink |

---

## 领域文件读取规范 (v4.5.5+)

**关键缺陷警示**: 在之前的模拟模式执行中，Domain Agents **没有读取** `references/{domain}_v2.md` 领域文件，而是直接使用通用知识生成分析，这严重违反了 V2 标准。

### 强制读取流程

**当我扮演 Domain Agent 时，我必须**：

#### Step 1: 检查领域文件是否存在

```python
import os

def check_domain_file(domain: str) -> str:
    """
    检查领域文件是否存在
    Returns: 文件路径或 None
    """
    # 标准路径
    base_path = "~/.claude/skills/morphism-mapper/references"
    
    # 尝试内置领域
    file_path = os.path.join(base_path, f"{domain}_v2.md")
    if os.path.exists(file_path):
        return file_path
    
    # 尝试自定义领域
    custom_path = os.path.join(base_path, "custom", f"{domain}_v2.md")
    if os.path.exists(custom_path):
        return custom_path
    
    return None
```

#### Step 2: 读取并解析领域文件

```python
def read_domain_knowledge(domain: str) -> dict:
    """
    读取领域文件并提取关键信息
    必须在扮演 Domain Agent 之前执行
    """
    file_path = check_domain_file(domain)
    
    if not file_path:
        # 触发补盲生成
        return generate_blind_domain(domain)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析 V2 标准结构
    knowledge = {
        "domain": domain,
        "file_path": file_path,
        "philosophy": extract_section(content, "哲学观"),  # 18条
        "principles": extract_section(content, "核心原则"),  # 22条
        "mental_models": extract_section(content, "心智模型"),  # 28条
        "methodology": extract_section(content, "方法论"),  # 22条
        "pitfalls": extract_section(content, "避坑指南"),  # 10条
        "core_objects": extract_section(content, "Core Objects"),  # 14个
        "core_morphisms": extract_section(content, "Core Morphisms"),  # 14个
        "theorems": extract_theorems(content),  # 18个定理
    }
    
    return knowledge
```

#### Step 3: 在分析中强制引用

**我的分析必须包含**：

```markdown
## 领域知识基础

**来源**: `references/{domain}_v2.md`

### 使用的定理
- **Theorem X**: {theorem_name}
  - **内容**: {theorem_content}
  - **适用结构**: {applicable_structure}
  - **映射提示**: {mapping_hint}
  - **案例**: {case_study}

### 概念映射
- `问题中的概念` → **{Core Object}** (引用领域文件定义)
- `动态关系` → **{Core Morphism}** (引用领域文件定义)

### 方法论应用
- **使用的方法**: {来自22条方法论的具体条目}
- **避开的坑**: {来自10条避坑指南的具体条目}
```

### 未读取领域文件的分析无效

**如果我在分析中没有**:
- [ ] 明确声明读取了 `references/{domain}_v2.md`
- [ ] 引用了至少 **2-3 个定理** (18个定理中的)
- [ ] 使用了 **Core Objects** 和 **Core Morphisms** 进行概念映射
- [ ] 提供了 **Case_Study** 支持洞察

**则该分析应被视为不完整，需要重新执行。**
