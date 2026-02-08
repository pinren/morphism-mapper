#!/usr/bin/env python3
"""
Cluster Detector - 同构簇识别模块 (v4.0)
将相似的 Domain Agent 映射聚类为同构簇
支持簇强度计算和核心结构提取
"""

import json
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict
import itertools


@dataclass
class HomographyCluster:
    """同构簇"""
    cluster_id: str
    members: List[str]
    shared_structure: str
    confidence: float
    strength: float
    core_formal_structure: str
    core_signature: str
    verification_proofs: List[Dict[str, Any]]


@dataclass
class ClusterRelationship:
    """簇间关系"""
    cluster_a: str
    cluster_b: str
    relationship_type: str  # "overlapping", "complementary", "conflicting"
    strength: float


class ClusterDetector:
    """同构簇检测器"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化检测器

        Args:
            config_path: 配置文件路径
        """
        from pathlib import Path

        if config_path is None:
            config_path = (
                Path(__file__).parent.parent.parent /
                "agents" / "config" / "swarm_protocol.json"
            )

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.min_similarity = self.config.get("clustering", {}).get(
            "min_similarity", 0.6
        )
        self.min_cluster_size = self.config.get("clustering", {}).get(
            "min_cluster_size", 2
        )

    def detect_clusters(
        self,
        agent_results: List[Dict[str, Any]],
        homography_matches: Optional[List] = None
    ) -> List[HomographyCluster]:
        """
        检测同构簇

        Args:
            agent_results: Agent 结果列表
            homography_matches: 可选的同构配对列表

        Returns:
            同构簇列表
        """
        # 如果没有提供 homography_matches，先计算
        if homography_matches is None:
            from modules.homography_detector import find_all_homographies
            homography_matches = find_all_homographies(agent_results)

        # 按相似度过滤
        filtered_matches = [
            m for m in homography_matches
            if m.similarity_score >= self.min_similarity
        ]

        # 形成簇
        clusters = self._form_clusters(filtered_matches)

        # 计算簇强度
        for cluster in clusters:
            cluster.strength = self.calculate_cluster_strength(cluster)

        # 按强度排序
        clusters.sort(key=lambda c: c.strength, reverse=True)

        return clusters

    def _form_clusters(
        self,
        homography_matches: List
    ) -> List[HomographyCluster]:
        """
        形成同构簇

        使用基于连通性的聚类算法

        Args:
            homography_matches: 同构配对列表

        Returns:
            同构簇列表
        """
        # 构建代理间的相似图
        graph = defaultdict(set)
        similarities = {}  # (agent_a, agent_b) -> similarity

        for match in homography_matches:
            agent_a = match.agent_a
            agent_b = match.agent_b
            graph[agent_a].add(agent_b)
            graph[agent_b].add(agent_a)
            similarities[(agent_a, agent_b)] = match.similarity_score
            similarities[(agent_b, agent_a)] = match.similarity_score

        # 使用连通分量形成簇
        visited = set()
        clusters = []

        for agent in graph:
            if agent not in visited:
                # BFS 找到连通分量
                cluster_members = self._bfs_find_component(graph, agent, visited)

                # 只保留满足最小大小的簇
                if len(cluster_members) >= self.min_cluster_size:
                    cluster = self._create_cluster_from_members(
                        cluster_members,
                        homography_matches
                    )
                    clusters.append(cluster)

        return clusters

    def _bfs_find_component(
        self,
        graph: Dict[str, Set[str]],
        start: str,
        visited: Set[str]
    ) -> List[str]:
        """BFS 找到连通分量"""
        component = []
        queue = [start]
        visited.add(start)

        while queue:
            node = queue.pop(0)
            component.append(node)

            for neighbor in graph.get(node, set()):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return component

    def _create_cluster_from_members(
        self,
        members: List[str],
        homography_matches: List
    ) -> HomographyCluster:
        """从成员列表创建簇"""
        # 找到涉及这些成员的所有匹配
        relevant_matches = [
            m for m in homography_matches
            if m.agent_a in members and m.agent_b in members
        ]

        # 计算平均置信度
        avg_confidence = sum(m.confidence for m in relevant_matches) / len(relevant_matches)

        # 提取共享结构
        shared_structure = self._extract_shared_structure(relevant_matches)

        # 提取核心签名
        core_signature = self._extract_core_signature(relevant_matches)

        # 收集 verification_proofs
        proofs = []
        for m in relevant_matches:
            if m.verification_proof:
                proofs.append(m.verification_proof)

        # 生成簇ID
        cluster_id = f"cluster_{'_'.join(sorted(members)[:2])}"

        return HomographyCluster(
            cluster_id=cluster_id,
            members=sorted(members),
            shared_structure=shared_structure,
            confidence=avg_confidence,
            strength=0.0,  # 稍后计算
            core_formal_structure=shared_structure,
            core_signature=core_signature,
            verification_proofs=proofs
        )

    def _extract_shared_structure(
        self,
        matches: List
    ) -> str:
        """提取共享结构描述"""
        if not matches:
            return ""

        # 收集所有 formal_structure
        structures = [m.formal_structure for m in matches]

        # 如果只有一个，直接返回
        if len(structures) == 1:
            return structures[0]

        # 如果有多个，找共同部分
        # 简化版本：取第一个作为代表
        return structures[0]

    def _extract_core_signature(
        self,
        matches: List
    ) -> str:
        """提取核心签名"""
        if not matches:
            return ""

        # 收集所有签名
        signatures = [m.formal_structure_signature for m in matches if m.formal_structure_signature]

        if not signatures:
            return ""

        # 简化版本：返回最常见的签名
        from collections import Counter
        counter = Counter(signatures)
        return counter.most_common(1)[0][0]

    def calculate_cluster_strength(
        self,
        cluster: HomographyCluster
    ) -> float:
        """
        计算簇强度

        簇强度 = (成员数权重 × 置信度权重 × 紧密度权重)

        Args:
            cluster: 同构簇

        Returns:
            强度分数 (0-1)
        """
        # 1. 成员数权重 (2-3个成员最优)
        member_count = len(cluster.members)
        if member_count == 2:
            member_weight = 0.8
        elif member_count == 3:
            member_weight = 1.0
        elif member_count == 4:
            member_weight = 0.9
        else:
            member_weight = 0.7

        # 2. 置信度权重
        confidence_weight = cluster.confidence

        # 3. 紧密度权重（基于验证证明数量）
        proof_count = len(cluster.verification_proofs)
        if proof_count >= len(cluster.members):
            tightness_weight = 1.0
        elif proof_count >= len(cluster.members) / 2:
            tightness_weight = 0.8
        else:
            tightness_weight = 0.6

        # 综合计算
        strength = (
            member_weight * 0.3 +
            confidence_weight * 0.5 +
            tightness_weight * 0.2
        )

        return strength

    def find_cluster_core_structure(
        self,
        cluster: HomographyCluster
    ) -> Dict[str, Any]:
        """
        找到簇的核心结构

        Args:
            cluster: 同构簇

        Returns:
            核心结构字典
        """
        # 分析所有 verification_proofs
        if_thens = []
        for proof in cluster.verification_proofs:
            if_then = proof.get("if_then_logic", "")
            if if_then:
                if_thens.append(if_then)

        # 提取共同元素
        common_elements = self._extract_common_elements(if_thens)

        return {
            "cluster_id": cluster.cluster_id,
            "members": cluster.members,
            "core_structure": cluster.core_formal_structure,
            "core_signature": cluster.core_signature,
            "common_elements": common_elements,
            "strength": cluster.strength,
            "confidence": cluster.confidence
        }

    def _extract_common_elements(
        self,
        texts: List[str]
    ) -> List[str]:
        """提取多个文本的共同元素"""
        if not texts:
            return []

        # 简化版本：提取所有文本中都出现的关键词
        import re
        from collections import Counter

        all_words = []
        for text in texts:
            words = re.findall(r'[\w]+', text.lower())
            all_words.append(set(words))

        # 找交集
        if all_words:
            common = set.intersection(*all_words)
            return list(common)[:10]  # 最多返回10个

        return []

    def detect_cluster_relationships(
        self,
        clusters: List[HomographyCluster]
    ) -> List[ClusterRelationship]:
        """
        检测簇间关系

        Args:
            clusters: 同构簇列表

        Returns:
            簇间关系列表
        """
        relationships = []

        for i, cluster_a in enumerate(clusters):
            for cluster_b in clusters[i+1:]:
                # 检查成员重叠
                overlap = set(cluster_a.members) & set(cluster_b.members)

                if overlap:
                    # 重叠关系
                    relationships.append(ClusterRelationship(
                        cluster_a=cluster_a.cluster_id,
                        cluster_b=cluster_b.cluster_id,
                        relationship_type="overlapping",
                        strength=len(overlap) / min(len(cluster_a.members), len(cluster_b.members))
                    ))

                # 检查签名互补
                elif self._are_complementary(cluster_a, cluster_b):
                    relationships.append(ClusterRelationship(
                        cluster_a=cluster_a.cluster_id,
                        cluster_b=cluster_b.cluster_id,
                        relationship_type="complementary",
                        strength=0.7
                    ))

                # 检查冲突
                elif self._are_conflicting(cluster_a, cluster_b):
                    relationships.append(ClusterRelationship(
                        cluster_a=cluster_a.cluster_id,
                        cluster_b=cluster_b.cluster_id,
                        relationship_type="conflicting",
                        strength=0.5
                    ))

        return relationships

    def _are_complementary(
        self,
        cluster_a: HomographyCluster,
        cluster_b: HomographyCluster
    ) -> bool:
        """判断两个簇是否互补"""
        # 检查签名是否互补
        # 简化版本：检查是否有共同的元素但不同的视角
        sig_a = set(cluster_a.core_signature.replace('_', ' ').split())
        sig_b = set(cluster_b.core_signature.replace('_', ' ').split())

        # 有一定重叠但不完全相同
        overlap = sig_a & sig_b
        union = sig_a | sig_b

        return 0.2 < len(overlap) / len(union) < 0.8 if union else False

    def _are_conflicting(
        self,
        cluster_a: HomographyCluster,
        cluster_b: HomographyCluster
    ) -> bool:
        """判断两个簇是否冲突"""
        # 检查是否有对立的元素
        conflict_keywords = [
            ("平衡", "失衡"),
            ("稳定", "变化"),
            ("开放", "封闭"),
            ("增长", "衰退")
        ]

        text_a = cluster_a.shared_structure.lower()
        text_b = cluster_b.shared_structure.lower()

        for kw_a, kw_b in conflict_keywords:
            if kw_a in text_a and kw_b in text_b:
                return True
            if kw_b in text_a and kw_a in text_b:
                return True

        return False

    def filter_weak_clusters(
        self,
        clusters: List[HomographyCluster],
        min_strength: float = 0.6
    ) -> List[HomographyCluster]:
        """过滤弱簇"""
        return [c for c in clusters if c.strength >= min_strength]


# ============================================================================
# 辅助函数
# ============================================================================

def create_clusters_from_agent_results(
    agent_results: List[Dict[str, Any]]
) -> List[HomographyCluster]:
    """
    从 Agent 结果直接创建簇

    Args:
        agent_results: Agent 结果列表

    Returns:
        同构簇列表
    """
    detector = ClusterDetector()
    return detector.detect_clusters(agent_results)


def merge_overlapping_clusters(
    clusters: List[HomographyCluster]
) -> List[HomographyCluster]:
    """
    合并重叠的簇

    Args:
        clusters: 同构簇列表

    Returns:
        合并后的簇列表
    """
    if not clusters:
        return []

    # 按强度排序
    sorted_clusters = sorted(clusters, key=lambda c: c.strength, reverse=True)

    merged = []
    used = set()

    for cluster in sorted_clusters:
        if cluster.cluster_id in used:
            continue

        # 找到所有重叠的簇
        overlapping = [cluster]
        used.add(cluster.cluster_id)

        for other in sorted_clusters:
            if other.cluster_id in used:
                continue

            # 检查重叠
            if set(cluster.members) & set(other.members):
                overlapping.append(other)
                used.add(other.cluster_id)

        # 合并成员
        all_members = set()
        all_proofs = []
        all_confidence = []

        for c in overlapping:
            all_members.update(c.members)
            all_proofs.extend(c.verification_proofs)
            all_confidence.append(c.confidence)

        # 创建合并后的簇
        from modules.homography_detector import find_all_homographies

        merged_cluster = HomographyCluster(
            cluster_id=f"merged_{'_'.join(sorted(all_members)[:2])}",
            members=sorted(all_members),
            shared_structure=cluster.shared_structure,  # 使用最强簇的结构
            confidence=sum(all_confidence) / len(all_confidence),
            strength=cluster.strength,  # 使用最强簇的强度
            core_formal_structure=cluster.core_formal_structure,
            core_signature=cluster.core_signature,
            verification_proofs=all_proofs
        )

        merged.append(merged_cluster)

    return merged


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """主函数"""
    print("=" * 60)
    print("Cluster Detector v4.0 - 同构簇检测演示")
    print("=" * 60)
    print()

    # 模拟 Agent 结果
    agent_results = [
        {
            "agent": "thermodynamics",
            "confidence": 0.85,
            "homography_candidates": [
                {
                    "domain_a_element": "熵增",
                    "domain_b_element": "noise_increase",
                    "formal_structure": "dS/dt > 0",
                    "formal_structure_signature": "dS/dt > 0 (Entropy Increase)"
                }
            ]
        },
        {
            "agent": "information_theory",
            "confidence": 0.82,
            "homography_candidates": [
                {
                    "domain_a_element": "信息熵",
                    "domain_b_element": "entropy",
                    "formal_structure": "H(X|Y) increases",
                    "formal_structure_signature": "H(X|Y) > 0 (Conditional Entropy)"
                }
            ]
        },
        {
            "agent": "control_systems",
            "confidence": 0.78,
            "homography_candidates": [
                {
                    "domain_a_element": "反馈调节",
                    "domain_b_element": "regulation",
                    "formal_structure": "negative feedback loop",
                    "formal_structure_signature": "Feedback → Regulation"
                }
            ]
        }
    ]

    # 模拟同构配对
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from homography_detector import HomographyMatch, HomographyDetector

    detector = ClusterDetector()

    # 创建模拟的同构匹配
    mock_matches = [
        HomographyMatch(
            agent_a="thermodynamics",
            agent_b="information_theory",
            agent_a_element="熵增",
            agent_b_element="信息熵",
            formal_structure="不可逆增长",
            formal_structure_signature="Irreversible Growth",
            similarity_score=0.85,
            confidence=0.84,
            reasoning="熵增与信息熵都是不可逆的增长过程",
            verification_proof={
                "if_then_logic": "如果熵增(dS/dt>0)，那么信息噪声增加",
                "examples": [{"verification": "两者都是不可逆过程"}]
            }
        ),
        HomographyMatch(
            agent_a="thermodynamics",
            agent_b="control_systems",
            agent_a_element="熵增",
            agent_b_element="反馈调节",
            formal_structure="系统调节",
            formal_structure_signature="System Regulation",
            similarity_score=0.65,
            confidence=0.72,
            reasoning="熵增需要反馈调节来对抗",
            verification_proof={
                "if_then_logic": "如果系统熵增，那么需要负反馈调节",
                "examples": []
            }
        )
    ]

    # 检测簇
    clusters = detector.detect_clusters(agent_results, mock_matches)

    print(f"【检测到 {len(clusters)} 个同构簇】")
    print()

    for i, cluster in enumerate(clusters, 1):
        print(f"簇 {i}: {cluster.cluster_id}")
        print(f"  成员: {', '.join(cluster.members)}")
        print(f"  共享结构: {cluster.shared_structure}")
        print(f"  核心签名: {cluster.core_signature}")
        print(f"  置信度: {cluster.confidence:.2f}")
        print(f"  强度: {cluster.strength:.2f}")
        print()

    # 检测簇间关系
    relationships = detector.detect_cluster_relationships(clusters)
    if relationships:
        print(f"【簇间关系 ({len(relationships)})】")
        for rel in relationships:
            print(f"  {rel.cluster_a} ↔ {rel.cluster_b}: {rel.relationship_type} (强度: {rel.strength:.2f})")


if __name__ == "__main__":
    main()
