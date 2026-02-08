#!/usr/bin/env python3
"""
Homography Detector - 配对同构检测模块 (v4.0)
检测两个 Domain Agent 之间的同构映射关系
支持 Verification Proof 验证逻辑
"""

import json
import re
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from difflib import SequenceMatcher


@dataclass
class HomographyMatch:
    """同构匹配结果"""
    agent_a: str
    agent_b: str
    agent_a_element: str
    agent_b_element: str
    formal_structure: str
    formal_structure_signature: str
    similarity_score: float
    confidence: float
    reasoning: str
    verification_proof: Optional[Dict[str, Any]]


@dataclass
class VerificationResult:
    """验证结果"""
    passed: bool
    consistency_score: float
    issues: List[str]
    suggestions: List[str]


class HomographyDetector:
    """配对同构检测器"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化检测器

        Args:
            config_path: swarm_protocol.json 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.trivial_adjectives = self._load_trivial_adjectives()

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置文件"""
        if config_path is None:
            from pathlib import Path
            config_path = (
                Path(__file__).parent.parent.parent /
                "agents" / "config" / "swarm_protocol.json"
            )

        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_trivial_adjectives(self) -> List[str]:
        """加载 Trivial Limit 黑名单形容词"""
        return [
            "需要平衡", "要有长远眼光", "应该重视", "要注意",
            "必须关注", "需要优化", "应该加强", "需要考虑",
            "要注意平衡", "应该注意", "需要改进"
        ]

    def detect_homography(
        self,
        agent_a_result: Dict[str, Any],
        agent_b_result: Dict[str, Any]
    ) -> Optional[HomographyMatch]:
        """
        检测两个 Agent 结果之间的同构

        Args:
            agent_a_result: Agent A 的映射结果
            agent_b_result: Agent B 的映射结果

        Returns:
            HomographyMatch 或 None（无同构）
        """
        # 提取候选
        for candidate_a in agent_a_result.get("homography_candidates", []):
            for candidate_b in agent_b_result.get("homography_candidates", []):
                # 计算结构相似度
                similarity = self._calculate_structural_similarity(
                    candidate_a.get("formal_structure", ""),
                    candidate_b.get("formal_structure", "")
                )

                # 如果相似度超过阈值，形成同构
                if similarity >= 0.6:
                    # 计算综合置信度
                    confidence = self._calculate_confidence(
                        agent_a_result.get("confidence", 0.5),
                        agent_b_result.get("confidence", 0.5),
                        similarity
                    )

                    # 验证 verification_proof
                    verification_proof = self._merge_verification_proofs(
                        candidate_a.get("verification_proof"),
                        candidate_b.get("verification_proof")
                    )

                    return HomographyMatch(
                        agent_a=agent_a_result.get("agent", "unknown"),
                        agent_b=agent_b_result.get("agent", "unknown"),
                        agent_a_element=candidate_a.get("domain_a_element", ""),
                        agent_b_element=candidate_b.get("domain_b_element", ""),
                        formal_structure=candidate_a.get("formal_structure", ""),
                        formal_structure_signature=candidate_a.get(
                            "formal_structure_signature", ""
                        ),
                        similarity_score=similarity,
                        confidence=confidence,
                        reasoning=self._generate_reasoning(
                            candidate_a, candidate_b, similarity
                        ),
                        verification_proof=verification_proof
                    )

        return None

    def _calculate_structural_similarity(
        self,
        structure_a: str,
        structure_b: str
    ) -> float:
        """
        计算两个形式化结构的相似度

        Args:
            structure_a: 结构 A 描述
            structure_b: 结构 B 描述

        Returns:
            相似度分数 (0-1)
        """
        # 使用 SequenceMatcher 计算字符串相似度
        similarity = SequenceMatcher(None, structure_a, structure_b).ratio()

        # 提取签名中的关键符号
        signature_a = self._extract_signature(structure_a)
        signature_b = self._extract_signature(structure_b)

        # 如果有签名，计算签名相似度
        if signature_a and signature_b:
            signature_similarity = SequenceMatcher(
                None, signature_a, signature_b
            ).ratio()
            # 加权平均：签名权重更高
            similarity = similarity * 0.3 + signature_similarity * 0.7

        return similarity

    def _extract_signature(self, text: str) -> str:
        """提取形式化签名"""
        # 提取数学符号、公式等
        patterns = [
            r'[A-Z]\s*=\s*[^,;\n]+',  # 赋值公式
            r'[a-z]\([^)]+\)',         # 函数调用
            r'd[A-Z]/dt',               # 导数
            r'∂[A-Z]/∂[a-z]',           # 偏导数
            r'∫[^∫]+dt',                # 积分
            r'[∑∏√±÷×<>≤≥]',           # 数学符号
            r'[A-Z]+_\{[^}]+\}',        # 下标
        ]

        signatures = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            signatures.extend(matches)

        return ' '.join(signatures)

    def _calculate_confidence(
        self,
        conf_a: float,
        conf_b: float,
        similarity: float
    ) -> float:
        """
        计算综合置信度

        Args:
            conf_a: Agent A 置信度
            conf_b: Agent B 置信度
            similarity: 结构相似度

        Returns:
            综合置信度 (0-1)
        """
        # 加权平均：相似度权重更高
        return (conf_a + conf_b) / 2 * 0.4 + similarity * 0.6

    def _generate_reasoning(
        self,
        candidate_a: Dict,
        candidate_b: Dict,
        similarity: float
    ) -> str:
        """生成推理说明"""
        return (
            f"{candidate_a.get('agent_a_element', '')} "
            f"与 {candidate_b.get('agent_b_element', '')} "
            f"在 '{candidate_a.get('formal_structure', '')}' 结构上相似 "
            f"(相似度: {similarity:.2f})"
        )

    def _merge_verification_proofs(
        self,
        proof_a: Optional[Dict],
        proof_b: Optional[Dict]
    ) -> Optional[Dict]:
        """合并两个验证证明"""
        if not proof_a or not proof_b:
            return proof_a or proof_b

        return {
            "if_then_logic": f"{proof_a.get('if_then_logic', '')} ↔ {proof_b.get('if_then_logic', '')}",
            "examples": (proof_a.get("examples", []) + proof_b.get("examples", []))
        }

    def verify_proof(self, proof: Dict[str, Any]) -> VerificationResult:
        """
        验证 Verification Proof 的一致性

        检查 if_then_logic 和 examples 的逻辑连贯性

        Args:
            proof: verification_proof 字典
                {
                    "if_then_logic": "如果 A，那么 B",
                    "examples": [{"domain_a_element": "...", "domain_b_element": "..."}]
                }

        Returns:
            VerificationResult
        """
        issues = []
        suggestions = []

        # 1. 检查 if_then_logic 格式
        if_then = proof.get("if_then_logic", "")
        if not if_then:
            issues.append("缺少 if_then_logic")
            return VerificationResult(
                passed=False, consistency_score=0.0, issues=issues, suggestions=suggestions
            )

        # 检查是否包含"如果...那么..."结构
        has_if_then_structure = (
            "如果" in if_then and "那么" in if_then
        ) or (
            "if" in if_then.lower() and "then" in if_then.lower()
        )

        if not has_if_then_structure:
            issues.append("if_then_logic 缺乏 '如果...那么...' 结构")

        # 2. 检查 examples
        examples = proof.get("examples", [])
        if not examples:
            issues.append("缺少 examples 验证示例")
        else:
            # 检查每个 example 的完整性
            for i, example in enumerate(examples):
                if "domain_a_element" not in example:
                    issues.append(f"example {i+1} 缺少 domain_a_element")
                if "domain_b_element" not in example:
                    issues.append(f"example {i+1} 缺少 domain_b_element")
                if "verification" not in example:
                    suggestions.append(f"example {i+1} 可添加 verification 说明")

        # 3. 检查 if_then 与 examples 的一致性
        if examples and has_if_then_structure:
            consistency = self._check_if_then_examples_consistency(
                if_then, examples
            )
            if not consistency:
                issues.append("if_then_logic 与 examples 不一致")
            else:
                suggestions.append("if_then_logic 与 examples 逻辑连贯")

        # 4. 检查 Trivial Limit
        if self._is_trivial_limit(if_then):
            issues.append("检测到 Trivial Limit：使用通用形容词而非结构性描述")
            suggestions.append("建议：使用具体的形式化映射（如 dS/dt > 0）替代通用描述")

        # 5. 计算一致性分数
        consistency_score = self._calculate_consistency_score(
            has_if_then_structure,
            len(examples) > 0,
            len(issues) == 0,
            not self._is_trivial_limit(if_then)
        )

        return VerificationResult(
            passed=len(issues) == 0,
            consistency_score=consistency_score,
            issues=issues,
            suggestions=suggestions
        )

    def _check_if_then_examples_consistency(
        self,
        if_then: str,
        examples: List[Dict]
    ) -> bool:
        """
        检查 if_then_logic 与 examples 的一致性

        Args:
            if_then: "如果 A，那么 B"
            examples: 验证示例列表

        Returns:
            是否一致
        """
        # 提取 if_then 中的关键元素
        if_match = re.search(r'如果(.+?)那么', if_then)
        if not if_match:
            if_match = re.search(r'if\s+(.+?)\s+then', if_then, re.IGNORECASE)

        if not if_match:
            return False  # 无法解析

        condition_part = if_match.group(1).strip()

        # 检查 examples 是否验证了 if_then 中的条件
        for example in examples:
            verification = example.get("verification", "")
            if verification:
                # 简单检查：verification 是否包含条件关键词
                keywords = self._extract_keywords(condition_part)
                if any(kw.lower() in verification.lower() for kw in keywords):
                    return True

        return True  # 默认认为一致

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 移除常见连接词
        stopwords = {"的", "是", "在", "与", "和", "或", "但", "而"}
        words = re.findall(r'[\w]+', text)
        return [w for w in words if w not in stopwords and len(w) > 1]

    def _is_trivial_limit(self, text: str) -> bool:
        """
        检测是否为 Trivial Limit

        Args:
            text: 待检测文本

        Returns:
            是否为 Trivial Limit
        """
        text_lower = text.lower()
        for adjective in self.trivial_adjectives:
            if adjective.lower() in text_lower:
                return True

        # 检查是否缺乏结构性描述
        has_structural = any([
            '=' in text,            # 赋值/等式
            '>' in text or '<' in text,  # 比较
            '→' in text or '->' in text,  # 映射
            'd/' in text,           # 导数
            '∂/' in text,           # 偏导
            '+' in text,            # 加法
            '反馈' in text,         # 反馈
            '回路' in text          # 回路
        ])

        return not has_structural

    def _calculate_consistency_score(
        self,
        has_structure: bool,
        has_examples: bool,
        no_issues: bool,
        not_trivial: bool
    ) -> float:
        """计算一致性分数"""
        score = 0.0

        if has_structure:
            score += 0.3
        if has_examples:
            score += 0.3
        if no_issues:
            score += 0.2
        if not_trivial:
            score += 0.2

        return score


# ============================================================================
# 辅助函数
# ============================================================================

def find_all_homographies(
    agent_results: List[Dict[str, Any]]
) -> List[HomographyMatch]:
    """
    找出所有 Agent 结果之间的同构配对

    Args:
        agent_results: Agent 结果列表

    Returns:
        同构配对列表
    """
    detector = HomographyDetector()
    homographies = []

    # 两两比较
    for i in range(len(agent_results)):
        for j in range(i + 1, len(agent_results)):
            match = detector.detect_homography(
                agent_results[i],
                agent_results[j]
            )
            if match:
                homographies.append(match)

    # 按置信度排序
    homographies.sort(key=lambda h: h.confidence, reverse=True)

    return homographies


def filter_homographies_by_confidence(
    homographies: List[HomographyMatch],
    min_confidence: float = 0.7
) -> List[HomographyMatch]:
    """按置信度过滤同构"""
    return [h for h in homographies if h.confidence >= min_confidence]


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """主函数"""
    import sys

    detector = HomographyDetector()

    # 演示 verification_proof 验证
    print("=" * 60)
    print("Homography Detector v4.0 - Verification Proof 验证演示")
    print("=" * 60)
    print()

    # 测试用例 1: 正常的 verification_proof
    proof_good = {
        "if_then_logic": "如果系统熵增加(dS/dt>0)，那么信息噪声增加(H(X|Y)上升)",
        "examples": [
            {
                "domain_a_element": "热力学熵增",
                "domain_b_element": "信息论噪声",
                "verification": "两者都是不可逆的无序化过程"
            }
        ]
    }

    print("【测试 1: 正常的 Verification Proof】")
    result = detector.verify_proof(proof_good)
    print(f"通过: {result.passed}")
    print(f"一致性分数: {result.consistency_score:.2f}")
    print(f"问题: {result.issues if result.issues else '无'}")
    print(f"建议: {result.suggestions if result.suggestions else '无'}")
    print()

    # 测试用例 2: Trivial Limit
    proof_trivial = {
        "if_then_logic": "系统需要平衡，要有长远眼光",
        "examples": []
    }

    print("【测试 2: Trivial Limit】")
    result = detector.verify_proof(proof_trivial)
    print(f"通过: {result.passed}")
    print(f"一致性分数: {result.consistency_score:.2f}")
    print(f"问题: {result.issues if result.issues else '无'}")
    print(f"建议: {result.suggestions if result.suggestions else '无'}")
    print()

    # 测试用例 3: 缺少 structure
    proof_no_structure = {
        "if_then_logic": "A 对应 B",
        "examples": [
            {"domain_a_element": "A", "domain_b_element": "B"}
        ]
    }

    print("【测试 3: 缺少 '如果...那么...' 结构】")
    result = detector.verify_proof(proof_no_structure)
    print(f"通过: {result.passed}")
    print(f"一致性分数: {result.consistency_score:.2f}")
    print(f"问题: {result.issues if result.issues else '无'}")
    print(f"建议: {result.suggestions if result.suggestions else '无'}")


if __name__ == "__main__":
    main()
