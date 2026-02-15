#!/usr/bin/env python3
"""
Dynamic Agent Generator v4.7
动态生成 Domain Agent 的完整系统 prompt

Usage:
    from dynamic_agent_generator import DynamicAgentGenerator
    generator = DynamicAgentGenerator()

    # 生成基础 prompt（不含范畴骨架）
    base_prompt = generator.generate_base_prompt('game_theory')

    # 生成完整 prompt（含范畴骨架）
    full_prompt = generator.generate_full_prompt(
        domain='game_theory',
        category_skeleton={
            'objects': [...],
            'morphisms': [...],
            '核心问题': '...'
        }
    )

    # 批量生成多个领域
    prompts = generator.generate_batch(
        domains=['game_theory', 'evolutionary_biology'],
        category_skeleton=category_skeleton
    )
"""

import re
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass


@dataclass
class DomainKnowledge:
    """领域知识数据结构"""
    domain: str
    domain_file_path: str
    domain_file_hash: str
    fundamentals: str      # 100基本基石
    core_objects: str      # 14 Core Objects
    core_morphisms: str    # 14 Core Morphisms
    theorems: str          # 18 Theorems
    philosophy: str        # 导语/哲学观


class DynamicAgentGenerator:
    """动态 Agent Prompt 生成器"""

    def __init__(self, references_dir: Optional[str] = None):
        """
        初始化生成器

        Args:
            references_dir: 领域知识文件目录，默认 scripts/../references
        """
        if references_dir is None:
            script_dir = Path(__file__).parent.parent
            self.references_dir = script_dir / "references"
        else:
            self.references_dir = Path(references_dir)

    def resolve_domain_file(self, domain: str) -> Path:
        """解析领域文件绝对路径"""
        domain_file = self.references_dir / f"{domain}_v2.md"
        if domain_file.exists():
            return domain_file
        custom_file = self.references_dir / "custom" / f"{domain}_v2.md"
        if custom_file.exists():
            return custom_file
        raise FileNotFoundError(f"领域文件不存在: {domain}_v2.md")

    def to_repo_relative_path(self, file_path: Path) -> str:
        """转换为 references 开头的相对路径（用于协议审计）"""
        try:
            return str(file_path.relative_to(self.references_dir.parent)).replace("\\", "/")
        except ValueError:
            return str(file_path).replace("\\", "/")

    def load_domain_file(self, domain: str) -> str:
        """加载领域知识文件"""
        domain_file = self.resolve_domain_file(domain)
        with open(domain_file, 'r', encoding='utf-8') as f:
            return f.read()

    def compute_sha256(self, content: str) -> str:
        """计算文本 SHA256"""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def extract_knowledge(self, content: str, domain: str) -> DomainKnowledge:
        """从文件内容提取结构化知识（标题锚点解析，降低正则脆弱性）"""
        normalized = content.replace("\r\n", "\n")

        f_match = re.search(r"^## Fundamentals.*$", normalized, re.MULTILINE)
        o_match = re.search(r"^## Core Objects.*$", normalized, re.MULTILINE)
        m_match = re.search(r"^## Core Morphisms.*$", normalized, re.MULTILINE)
        t_match = re.search(r"^## Theorems.*$", normalized, re.MULTILINE)
        if not all([f_match, o_match, m_match, t_match]):
            missing = []
            if not f_match:
                missing.append("Fundamentals")
            if not o_match:
                missing.append("Core Objects")
            if not m_match:
                missing.append("Core Morphisms")
            if not t_match:
                missing.append("Theorems")
            raise ValueError(f"{domain} 缺少必须章节: {', '.join(missing)}")

        fundamentals = normalized[f_match.start():o_match.start()].strip()
        core_objects = normalized[o_match.start():m_match.start()].strip()
        core_morphisms = normalized[m_match.start():t_match.start()].strip()
        theorems = normalized[t_match.start():].strip()

        philosophy = ""
        intro_match = re.search(r"### 导语\s*\n(.*?)(?=\n### |\n---|\Z)", fundamentals, re.DOTALL)
        if intro_match:
            philosophy = intro_match.group(1).strip()

        domain_file = self.resolve_domain_file(domain)
        domain_file_path = self.to_repo_relative_path(domain_file)
        domain_file_hash = self.compute_sha256(normalized)

        return DomainKnowledge(
            domain=domain,
            domain_file_path=domain_file_path,
            domain_file_hash=domain_file_hash,
            fundamentals=fundamentals,
            core_objects=core_objects,
            core_morphisms=core_morphisms,
            theorems=theorems,
            philosophy=philosophy,
        )

    def truncate(self, text: str, max_chars: int = 2000, indicator: str = "...") -> str:
        """智能截断文本，保留完整句子"""
        if len(text) <= max_chars:
            return text

        # 在max_chars处找到最后一个句号
        truncated = text[:max_chars]
        last_period = truncated.rfind('。')
        last_newline = truncated.rfind('\n\n')

        cut_point = max(last_period, last_newline)
        if cut_point > max_chars * 0.7:  # 确保截断点不要太靠前
            return text[:cut_point + 1] + indicator
        else:
            return truncated + indicator

    def generate_base_prompt(self, domain: str) -> str:
        """
        生成基础 Prompt（不含范畴骨架）

        这是 Step 1-3 的输出，供 Team Lead 调用
        """
        content = self.load_domain_file(domain)
        knowledge = self.extract_knowledge(content, domain)

        domain_display = domain.replace('_', ' ').title()
        schema_path = "assets/agents/schemas/domain_mapping_result.v1.json"

        prompt = f"""你是 Morphism Mapper v4.7.0 的 Domain Agent，代表 **{domain_display}** 领域。

---

## 🔴 身份声明（不可串台）

**你是谁**:
- 你的唯一身份: `{domain}-agent`
- 你的唯一职责: 从 {domain_display} 领域视角分析问题
- 你的唯一任务: 生成严格 JSON 映射结果并发送给 `synthesizer` 和 `obstruction-theorist`

**你不是谁** (⚠️ 绝对禁止):
- ❌ 你**不是** obstruction-theorist (职业反对派)
- ❌ 你**不是** synthesizer (跨域整合者)
- ❌ 你**不是** team-lead (协调者)

---

## 领域文件审计链路（强制）

**你必须先读取领域文件，再分析。**

- `domain_file_path`: `{knowledge.domain_file_path}`
- `expected_domain_file_hash`: `{knowledge.domain_file_hash}`
- `schema_path`: `{schema_path}`

执行步骤:
1. 第一步必须 `read_file({knowledge.domain_file_path})`
2. 分析时引用证据，填入 `evidence_refs`
3. 输出 `domain_file_hash` 字段，必须与 `expected_domain_file_hash` 一致
4. 不得输出缺字段 JSON。缺失 `domain_file_hash` 或 `kernel_loss` 视为无效结果

---

## 输出协议（严格 JSON，单一主体）

你必须输出 **一个且仅一个** JSON 对象，字段遵循 `domain_mapping_result.v1`：

```json
{{
  "schema_version": "domain_mapping_result.v1",
  "domain": "{domain}",
  "domain_file_path": "{knowledge.domain_file_path}",
  "domain_file_hash": "{knowledge.domain_file_hash}",
  "evidence_refs": [
    {{
      "section": "Fundamentals",
      "quote_or_summary": "引用或摘要"
    }},
    {{
      "section": "Core Morphisms",
      "quote_or_summary": "引用或摘要"
    }},
    {{
      "section": "Theorems",
      "quote_or_summary": "引用或摘要"
    }}
  ],
  "objects_map": [
    {{
      "a_obj": "Domain A Object",
      "b_obj": "{domain_display} Object",
      "rationale": "映射依据"
    }}
  ],
  "morphisms_map": [
    {{
      "a_mor": "Domain A Morphism",
      "b_mor": "{domain_display} Morphism",
      "dynamics": "动态对应关系"
    }}
  ],
  "theorems_used": [
    {{
      "id": "T1",
      "name": "定理名称",
      "mapping_hint_application": "如何用于当前问题"
    }},
    {{
      "id": "T2",
      "name": "定理名称",
      "mapping_hint_application": "如何用于当前问题"
    }}
  ],
  "kernel_loss": {{
    "lost_nuances": [
      {{
        "element": "丢失元素",
        "description": "为什么丢失",
        "severity": "HIGH"
      }}
    ],
    "preservation_score": 0.0
  }},
  "strategy_topology": {{
    "topology_type": "distributed_mesh",
    "core_action": "increase_redundancy",
    "resource_flow": "diffuse",
    "feedback_loop": "negative_feedback",
    "time_dynamics": "irreversible",
    "agent_type": "adaptive_learning"
  }},
  "topology_reasoning": "一句话说明策略拓扑选择",
  "confidence": 0.0
}}
```

硬性校验:
- `evidence_refs` 必须覆盖 `Fundamentals/Core Morphisms/Theorems`
- `objects_map` 至少 1 条
- `morphisms_map` 至少 1 条
- `theorems_used` 至少 2 条
- `kernel_loss.lost_nuances` 至少 1 条
- `confidence` 取值 0-1
- 不要用 markdown 表格作为主输出

发送前必须执行 `PRE_SEND_SCHEMA_GATE`：

```text
必须同时满足:
1) 必填字段全部存在:
   - schema_version, domain, domain_file_path, domain_file_hash, evidence_refs
   - objects_map, morphisms_map, theorems_used
   - kernel_loss, strategy_topology, topology_reasoning, confidence
2) schema_version == "domain_mapping_result.v1"
3) domain_file_path 匹配 references/(custom/)?*_v2.md
4) domain_file_hash 为 64 位十六进制
5) evidence_refs 为数组且 >= 3 条，并覆盖:
   - Fundamentals
   - Core Morphisms
   - Theorems
6) objects_map >= 1, morphisms_map >= 1, theorems_used >= 2
7) kernel_loss 是对象，且包含:
   - lost_nuances(数组, >=1)
   - preservation_score(0~1)
8) strategy_topology 存在且包含 6 个字段:
   - topology_type, core_action, resource_flow
   - feedback_loop, time_dynamics, agent_type
9) topology_reasoning 非空字符串
10) confidence 为 0~1 数值

若任一不满足:
- 不得发送消息
- 立即修复 JSON 后重新自检
```

常见错误（禁止）:
- ❌ `"kernel_loss": 0.12`（标量错误）
- ❌ 缺失 `"schema_version"`
- ❌ 缺失 `"strategy_topology"`
- ❌ `evidence_refs` 缺失 `Fundamentals/Core Morphisms/Theorems` 任一 section

---

## SendMessage 协议（强制）

分析完成后，必须发送 2 条消息（内容都包含同一个 JSON 主体和 `message_id`）:

1) `MAPPING_RESULT_ROUND1` -> `obstruction-theorist`
2) `MAPPING_RESULT_JSON` -> `synthesizer`

```
MAPPING_RESULT_ROUND1
message_id={domain}-{{timestamp}}-round1
{{JSON主体验证通过后粘贴在这里}}
```

```
MAPPING_RESULT_JSON
message_id={domain}-{{timestamp}}-round1
{{同一份JSON主体验证通过后粘贴在这里}}
```

⚠️ **重要**: 两个消息都必须发送，缺一不可！

ACK 握手（必须）:
- 等待 `OBSTRUCTION_ACK_RECEIVED` 与 `SYNTHESIZER_ACK_RECEIVED`
- 若 90s 内缺任一 ACK：
  1) 重发对应消息一次（同一 `message_id`）
  2) 向 Team Lead 发送 `DELIVERY_ACK_TIMEOUT`

---

## 应对 Obstruction 审查

当收到 obstruction-theorist 的质疑时：

1. 不防御，先检查 JSON 字段是否完整
2. 用 `evidence_refs` + `theorems_used` 回应质疑
3. 若修正，必须重发完整 JSON 主体（不是补丁片段）

---

## 等待范畴骨架注入

**Team Lead 将在启动后通过 SendMessage 注入 CATEGORY_SKELETON**。

在收到以下消息前，不要开始分析：
- 消息标题包含 "CATEGORY_SKELETON 注入"
- 包含 Objects、Morphisms、核心问题

收到后，将范畴骨架与你的领域知识结合，开始分析。
"""

        return prompt

    def inject_skeleton(self, base_prompt: str, category_skeleton: Dict[str, Any]) -> str:
        """
        注入范畴骨架到 Prompt

        这是 Step 4，由 Team Lead 调用

        支持两种输入格式：
        1. 字典格式（标准）: objects=[{'name': 'xxx', 'attributes': 'xxx'}]
        2. 字符串格式（兼容）: objects=['xxx'] 自动转换为字典
        """
        # 构建范畴骨架文本
        skeleton_text = f"""
## CATEGORY_SKELETON 注入（统一标准格式）

**Objects**：
"""
        for obj in category_skeleton.get('objects', []):
            if isinstance(obj, str):
                # 字符串格式：直接使用
                skeleton_text += f"- {obj}\n"
            elif isinstance(obj, dict):
                # 字典格式：标准处理
                attrs = obj.get('attributes', '')
                skeleton_text += f"- {obj['name']}（{attrs}）\n"
            else:
                # 其他格式：转为字符串
                skeleton_text += f"- {str(obj)}\n"

        skeleton_text += "\n**Morphisms**：\n"
        for mor in category_skeleton.get('morphisms', []):
            if isinstance(mor, str):
                # 字符串格式：直接使用
                skeleton_text += f"- {mor}\n"
            elif isinstance(mor, dict):
                # 字典格式：标准处理
                dynamics = mor.get('dynamics', '')
                skeleton_text += f"- {mor['from']} → {mor['to']}: {dynamics}\n"
            else:
                # 其他格式：转为字符串
                skeleton_text += f"- {str(mor)}\n"

        skeleton_text += f"\n**核心问题**：{category_skeleton.get('核心问题', '')}\n"

        # 替换或追加到 prompt
        if "等待范畴骨架注入" in base_prompt:
            # 替换占位符
            full_prompt = base_prompt.replace(
                "## 等待范畴骨架注入\n\n**Team Lead 将在启动后通过 SendMessage 注入 CATEGORY_SKELETON**。",
                skeleton_text + "\n\n## 开始分析\n\n请基于上述领域知识和范畴骨架，执行你的分析任务。"
            )
        else:
            # 直接追加
            full_prompt = base_prompt + "\n" + skeleton_text + "\n\n请开始分析。"

        return full_prompt

    def generate_full_prompt(
        self,
        domain: str,
        category_skeleton: Dict[str, Any]
    ) -> str:
        """
        生成完整 Prompt（含范畴骨架）

        一次性生成，用于调试模式
        """
        base_prompt = self.generate_base_prompt(domain)
        return self.inject_skeleton(base_prompt, category_skeleton)

    def check_and_create_domain(
        self,
        domain: str,
        domain_source: Optional[str] = None,
        auto_create: bool = False
    ) -> Tuple[bool, str]:
        """
        检查领域是否存在，不存在则创建

        Args:
            domain: 领域名称
            domain_source: 领域来源描述（用于自动生成时参考）
            auto_create: 是否自动创建缺失的领域

        Returns:
            (exists, file_path) - 是否存在，文件路径
        """
        # 检查标准目录
        domain_file = self.references_dir / f"{domain}_v2.md"
        if domain_file.exists():
            return True, str(domain_file)

        # 检查 custom 目录
        custom_file = self.references_dir / "custom" / f"{domain}_v2.md"
        if custom_file.exists():
            return True, str(custom_file)

        # 如果不自动创建，返回不存在
        if not auto_create:
            return False, str(custom_file)

        # 自动生成领域文件
        print(f"领域 {domain} 不存在，正在自动生成...")
        return self._auto_create_domain(domain, domain_source, custom_file)

    def _auto_create_domain(
        self,
        domain: str,
        domain_source: Optional[str],
        output_file: Path
    ) -> Tuple[bool, str]:
        """
        自动生成领域文件（参考 add-domain 提示词）

        返回生成提示词，由 Team Lead 调用 LLM 生成实际内容
        """
        # 构建生成提示词
        generation_prompt = f"""你是领域知识生成专家。请基于以下信息生成完整的 V2 标准领域知识文件。

## 领域信息

**领域名称**: {domain}
**英文标识**: {domain}
**来源参考**: {domain_source or '请基于领域常识生成'}

## V2 标准格式要求

```markdown
# Domain: [领域名称]
# Source: [学者《著作》, ...]
# Structural_Primitives: [5-10个核心概念]

## Fundamentals (100 基本基石)

### 导语
[100-150字，点破该领域最核心矛盾，冷峻简练宗师口吻]

### 一、哲学观 (18条)
[编号1-18，每条≤20字，有力简练，宗师口吻]

### 二、核心原则 (22条)
[编号19-40，每条≤20字，该领域的铁律]

### 三、思维模型 (28条)
[编号41-68，每条≤20字，认知工具箱]

### 四、关键方法论 (22条)
[编号69-90，每条≤20字，可执行的手段]

### 五、避坑指南 (10条)
[编号91-100，每条≤20字，血泪教训]

---

## Core Objects (14个)

- **[Object 1]**: [一句话定义]
  - *本质*: [一句话本质]
  - *关联*: [关联对象]
[共14个Object]

---

## Core Morphisms (14个)

- **[Morphism 1]**: [一句话定义]
  - *涉及*: [涉及对象]
  - *动态*: [动态描述]
[共14个Morphism]

---

## Theorems / Patterns (18个)

### 1. [定理名称]
**内容**: [定理详细描述]

**Applicable_Structure**: [适用结构描述]

**Mapping_Hint**: [具体可操作："当Domain A面临[具体情境]时，识别[具体结构]，通过[具体方法]实现[具体目标]"]

**Case_Study**: [案例研究]

---
[共18个Theorem]

## Tags

- [标签1]
- [标签2]
```

## 质量标准

1. **100条每条必须有力**，引发深层思考，不是常识
2. **导语必须点破核心矛盾**，不是介绍背景
3. **Mapping_Hint必须具体可操作**，不能泛泛而谈
4. **保留 V2 结构完整性**：100基石 + 14O + 14M + 18T
5. **宗师口吻**，冷峻简练，无废话

请生成完整的领域知识文件内容。
"""

        # 保存生成提示词到临时文件（供 Team Lead 使用）
        prompt_file = output_file.parent / f".{domain}_generation_prompt.txt"
        prompt_file.parent.mkdir(parents=True, exist_ok=True)
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(generation_prompt)

        # 返回提示词和输出路径
        return False, str(output_file)

    def create_domain_from_content(
        self,
        domain: str,
        content: str,
        output_file: Optional[Path] = None
    ) -> str:
        """
        将生成的内容保存为领域文件

        Args:
            domain: 领域名称
            content: LLM 生成的完整内容
            output_file: 输出文件路径（可选）

        Returns:
            保存的文件路径
        """
        if output_file is None:
            output_file = self.references_dir / "custom" / f"{domain}_v2.md"

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        # 删除临时提示词文件
        prompt_file = output_file.parent / f".{domain}_generation_prompt.txt"
        if prompt_file.exists():
            prompt_file.unlink()

        return str(output_file)

    def generate_batch(
        self,
        domains: List[str],
        category_skeleton: Dict[str, Any],
        auto_create: bool = False,
        domain_sources: Optional[Dict[str, str]] = None
    ) -> Dict[str, str]:
        """
        批量生成多个领域的 Prompt

        Args:
            domains: 领域名称列表
            category_skeleton: 范畴骨架
            auto_create: 是否自动创建缺失的领域
            domain_sources: 领域来源描述字典 {domain: source_description}

        Returns:
            Dict[domain_name, full_prompt]
        """
        prompts = {}
        for domain in domains:
            try:
                # 检查/创建领域
                exists, path_or_prompt = self.check_and_create_domain(
                    domain,
                    domain_sources.get(domain) if domain_sources else None,
                    auto_create
                )

                if not exists and auto_create:
                    # 读取生成提示词
                    prompt_file = Path(path_or_prompt).parent / f".{domain}_generation_prompt.txt"
                    if prompt_file.exists():
                        with open(prompt_file, 'r', encoding='utf-8') as f:
                            generation_prompt = f.read()
                    else:
                        generation_prompt = "生成提示词未找到"

                    # 返回给 Lead Agent 的指令
                    prompts[domain] = {
                        "action": "CREATE_DOMAIN",
                        "domain": domain,
                        "generation_prompt": generation_prompt,
                        "output_path": path_or_prompt,
                        "instruction": f"""
【领域 {domain} 需要补盲生成】

该领域在 references/ 中不存在，需要动态创建。

**执行步骤**：
1. 使用 generation_prompt 调用 LLM 生成完整领域知识
2. 调用 create_domain_from_content(domain, content) 保存文件
3. 重新调用 generate_batch 获取完整的 Domain Agent Prompt

**注意**：这是一个阻塞步骤，必须完成领域创建后才能启动 Domain Agent。
"""
                    }
                    continue

                prompts[domain] = self.generate_full_prompt(domain, category_skeleton)

            except FileNotFoundError as e:
                print(f"Warning: 跳过 {domain} - {e}")
                continue
            except Exception as e:
                print(f"Error: 处理 {domain} 时出错 - {e}")
                continue

        return prompts

    def generate_and_save(
        self,
        domains: List[str],
        category_skeleton: Dict[str, Any],
        output_dir: Optional[str] = None
    ) -> List[str]:
        """
        生成并保存 Prompt 到文件

        Returns:
            生成的文件路径列表
        """
        if output_dir is None:
            script_dir = Path(__file__).parent
            output_path = script_dir / "generated_prompts"
        else:
            output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 清理旧文件（session 临时数据）
        for old_file in output_path.glob("*_agent_prompt.md"):
            old_file.unlink()

        prompts = self.generate_batch(domains, category_skeleton)
        saved_files = []

        for domain, prompt in prompts.items():
            file_path = output_path / f"{domain}_agent_prompt.md"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(prompt)
            saved_files.append(str(file_path))
            print(f"✓ 生成: {file_path}")

        return saved_files


def main():
    """CLI 入口"""
    import sys
    import json

    generator = DynamicAgentGenerator()

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # 演示模式
        print("=" * 60)
        print("Dynamic Agent Generator v4.7 - Demo")
        print("=" * 60)

        # 示例范畴骨架
        skeleton = {
            "objects": [
                {"name": "美国", "attributes": "全球霸权, 域外执法"},
                {"name": "马杜罗", "attributes": "国家元首, 反美象征"},
            ],
            "morphisms": [
                {"from": "美国", "to": "马杜罗", "dynamics": "单边制裁"},
            ],
            "核心问题": "美国抓捕马杜罗的影响"
        }

        # 生成 game_theory 的完整 prompt
        print("\n生成 game_theory 的 full_prompt...")
        prompt = generator.generate_full_prompt('game_theory', skeleton)
        print(f"Prompt 长度: {len(prompt)} 字符")
        print(f"\n前1000字符:\n{prompt[:1000]}...")

    elif len(sys.argv) > 1 and sys.argv[1] == "--batch":
        # 批量生成模式
        domains = sys.argv[2].split(',') if len(sys.argv) > 2 else ['game_theory']

        skeleton = {
            "objects": [
                {"name": "美国", "attributes": "全球霸权"},
                {"name": "马杜罗", "attributes": "国家元首"},
            ],
            "morphisms": [
                {"from": "美国", "to": "马杜罗", "dynamics": "单边制裁"},
            ],
            "核心问题": "测试"
        }

        print(f"批量生成: {domains}")
        files = generator.generate_and_save(domains, skeleton)
        print(f"\n生成文件: {files}")

    else:
        print("Dynamic Agent Generator v4.7")
        print()
        print("用法:")
        print("  python dynamic_agent_generator.py --demo      演示模式")
        print("  python dynamic_agent_generator.py --batch domain1,domain2  批量生成")
        print()
        print("Python API:")
        print("  from dynamic_agent_generator import DynamicAgentGenerator")
        print("  generator = DynamicAgentGenerator()")
        print("  base_prompt = generator.generate_base_prompt('game_theory')")
        print("  full_prompt = generator.generate_full_prompt('game_theory', skeleton)")


if __name__ == "__main__":
    main()
