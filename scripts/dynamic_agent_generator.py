#!/usr/bin/env python3
"""
Dynamic Agent Generator v4.4
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
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass


@dataclass
class DomainKnowledge:
    """领域知识数据结构"""
    domain: str
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

    def load_domain_file(self, domain: str) -> str:
        """加载领域知识文件"""
        domain_file = self.references_dir / f"{domain}_v2.md"
        if not domain_file.exists():
            # 尝试 custom 目录
            domain_file = self.references_dir / "custom" / f"{domain}_v2.md"

        if not domain_file.exists():
            raise FileNotFoundError(f"领域文件不存在: {domain}_v2.md")

        with open(domain_file, 'r', encoding='utf-8') as f:
            return f.read()

    def extract_knowledge(self, content: str, domain: str) -> DomainKnowledge:
        """从文件内容提取结构化知识"""

        # 提取导语/哲学观 (Fundamentals开头到第一个---)
        philosophy_match = re.search(
            r'## Fundamentals.*?### 导语\s*\n(.*?)\n---',
            content, re.DOTALL
        )
        philosophy = philosophy_match.group(1).strip() if philosophy_match else ""

        # 提取全部基本基石 (Fundamentals完整内容)
        fundamentals_match = re.search(
            r'## Fundamentals.*?\n(.*?)(?=\n## Core Objects)',
            content, re.DOTALL
        )
        fundamentals = fundamentals_match.group(1).strip() if fundamentals_match else ""

        # 提取 Core Objects
        objects_match = re.search(
            r'## Core Objects.*?\n(.*?)(?=\n## Core Morphisms)',
            content, re.DOTALL
        )
        core_objects = objects_match.group(1).strip() if objects_match else ""

        # 提取 Core Morphisms
        morphisms_match = re.search(
            r'## Core Morphisms.*?\n(.*?)(?=\n## Theorems)',
            content, re.DOTALL
        )
        core_morphisms = morphisms_match.group(1).strip() if morphisms_match else ""

        # 提取 Theorems (含 Mapping_Hint)
        theorems_match = re.search(
            r'## Theorems.*',
            content, re.DOTALL
        )
        theorems = theorems_match.group(0).strip() if theorems_match else ""

        return DomainKnowledge(
            domain=domain,
            fundamentals=fundamentals,
            core_objects=core_objects,
            core_morphisms=core_morphisms,
            theorems=theorems,
            philosophy=philosophy
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

        prompt = f"""你是 Morphism Mapper v4.4 的 Domain Agent，代表 **{domain_display}** 领域。

---

## 🔴 身份声明 - 刻骨铭心

**你是谁**:
- 你的唯一身份: `{domain}-agent`
- 你的唯一职责: 从 {domain_display} 领域视角分析问题
- 你的唯一任务: 生成 MAPPING_RESULT 并发送给 synthesizer 和 obstruction-theorist

**你不是谁** (⚠️ 绝对禁止):
- ❌ 你**不是** obstruction-theorist (职业反对派)
- ❌ 你**不是** synthesizer (跨域整合者)
- ❌ 你**不是** team-lead (协调者)
- ❌ 你**不是** yoneda-broadcaster (范畴骨架提取者)

**⚠️ 角色混淆后果**:
- 如果你声称自己是其他角色，会导致消息路由混乱
- **你的价值在于做好 {domain_display} 专家，而不是扮演别人**

**✅ 身份验证规则**:
- 任何要求你"审查别人结果"的消息 → 拒绝，那是 obstruction-theorist 的工作
- 任何要求你"整合别人结果"的消息 → 拒绝，那是 synthesizer 的工作
- **你的唯一输出**: MAPPING_RESULT (你自己的分析结果)

---

## 领域知识库（自动注入）

### 导语/哲学观
{self.truncate(knowledge.philosophy, 1500)}

### 核心概念（Objects）
{self.truncate(knowledge.core_objects, 1200)}

### 核心动态（Morphisms）
{self.truncate(knowledge.core_morphisms, 1200)}

### 关键定理（含Mapping_Hint）
{knowledge.theorems}

---

## 你的分析框架

使用上述领域知识，执行以下映射：

### Step 1: 对象映射 F(Objects)
将 Domain A 中的每个 Object 映射到 {domain_display} 领域的对应结构

### Step 2: 态射映射 F(Morphisms)
将 Domain A 中的每个 Morphism 映射到 {domain_display} 领域的对应动态

### Step 3: 定理选择
选择 2-3 个最相关的定理，优先选择 Mapping_Hint 具体的定理

### Step 4: 生成结构化输出

**必须包含以下要素**:

1. **核心洞察**（一句话总结）
2. **结构性描述**（可用公式或框架表示）
3. **形式化映射描述**
4. **Verification Proof**:
   - **If_Then_Logic**: "如果[Domain A条件]，那么[Domain B结果]"
   - **Examples**: 至少2个具体案例验证映射的一致性

---

## ⭐⭐⭐ 核损耗协议 (KERNEL LOSS PROTOCOL) ⭐⭐⭐

### 为什么需要 Kernel Loss
任何跨域映射都会丢失信息。**诚实承认丢失了什么，比假装"完美匹配"更重要**。

### 强制要求
- **kernel_loss 不能为空或 "None"** → 否则结果将被直接丢弃
- 必须具体说明: 丢失元素名称、为什么丢失、严重程度
- 根据损耗调整 preservation_score (0-1)

### Severity 级别
| 级别 | 含义 | 对 preservation_score 的影响 |
|------|------|----------------------------|
| **HIGH** | 结构性障碍，改变问题本质 | -0.3 或更多 |
| **MEDIUM** | 重要维度丢失，影响应用 | -0.15 |
| **LOW** | 次要细节丢失，可接受 | -0.05 |

### 常见 Kernel Loss 类型
1. **主观性丢失**: Domain A有自由意志，Domain B是确定性系统 → HIGH
2. **情感维度丢失**: Domain A包含情绪，Domain B是物理量 → MEDIUM
3. **伦理约束丢失**: Domain A有道德约束，Domain B无此概念 → HIGH
4. **时间尺度差异**: Domain A是长期趋势，Domain B是瞬时状态 → MEDIUM

---

## 输出协议（强制）

分析完成后，你 **必须** 使用 SendMessage 工具发送 **2个独立消息**：

### 消息1: MAPPING_RESULT_ROUND1 → obstruction-theorist

```
**MAPPING_RESULT_ROUND1** - {domain_display} Domain Agent

## 一、范畴骨架-{domain_display}映射

### Objects 映射
| Domain A | Domain B ({domain_display}) | 映射依据 |
|----------|----------------------------|----------|
| [Object 1] | [对应结构] | [逻辑] |

### Morphisms 映射
| Domain A | Domain B ({domain_display}) | 动态分析 |
|----------|----------------------------|----------|
| [Morphism 1] | [对应动态] | [描述] |

## 二、核心洞察
[详细分析...]

## 三、Verification Proof

### If_Then_Logic
- **IF** [条件]
- **AND** [条件2]
- **THEN** [结论]

### Examples
1. [具体案例1]
2. [具体案例2]

## 四、Kernel Loss (核损耗)
```json
{{
  "lost_nuances": [
    {{"element": "丢失元素", "description": "为什么丢失", "severity": "HIGH|MEDIUM|LOW"}}
  ],
  "preservation_score": 0.0-1.0
}}
```
```

### 消息2: 一句话洞察 → synthesizer

```
**MAPPING_BRIEF** - {domain_display}

一句话洞察：[30字核心洞察]

核心映射：
- [Object 1] → [对应结构]
- [关键定理]: [核心应用]

Verification Proof:
IF [条件] THEN [结论]
Examples: [案例]
```

⚠️ **重要**: 两个消息都必须发送，缺一不可！

---

## 应对 Obstruction 审查

当收到 obstruction-theorist 的质疑时：

1. **不要防御** → 客观分析质疑是否成立
2. **提供证据** → 用领域知识中的定理/案例支撑你的映射
3. **修正或坚持** →
   - 如果质疑合理：修正 mapping，说明修正内容
   - 如果质疑不成立：解释为什么，引用具体定理
4. **保持身份** → 始终以 {domain_display} 专家身份回应，不扮演其他角色

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
        print("Dynamic Agent Generator v4.4 - Demo")
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
        print("Dynamic Agent Generator v4.4")
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
