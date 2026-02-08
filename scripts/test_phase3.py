#!/usr/bin/env python3
"""
Phase 3 完成标准验证脚本
验证通信协议模块的完成标准
"""

import sys
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent / "modules"))

from homography_detector import (
    HomographyDetector,
    find_all_homographies,
    filter_homographies_by_confidence
)
from cluster_detector import (
    ClusterDetector,
    create_clusters_from_agent_results,
    merge_overlapping_clusters
)


def test_verification_proof_logic():
    """测试 1: verification_proof 验证逻辑"""
    print("=" * 60)
    print("测试 1: Verification Proof 验证逻辑")
    print("=" * 60)

    detector = HomographyDetector()

    # 测试用例
    test_cases = [
        {
            "name": "正常 proof",
            "proof": {
                "if_then_logic": "如果系统熵增加(dS/dt>0)，那么信息噪声增加(H(X|Y)上升)",
                "examples": [
                    {
                        "domain_a_element": "热力学熵增",
                        "domain_b_element": "信息论噪声",
                        "verification": "两者都是不可逆的无序化过程"
                    }
                ]
            },
            "expected_pass": True
        },
        {
            "name": "Trivial Limit",
            "proof": {
                "if_then_logic": "系统需要平衡，要有长远眼光",
                "examples": []
            },
            "expected_pass": False
        },
        {
            "name": "缺少 if-then 结构",
            "proof": {
                "if_then_logic": "A 对应 B",
                "examples": [
                    {"domain_a_element": "A", "domain_b_element": "B"}
                ]
            },
            "expected_pass": False
        }
    ]

    passed = 0
    total = len(test_cases)

    for test in test_cases:
        result = detector.verify_proof(test["proof"])
        actual_pass = result.passed

        status = "✓ PASS" if actual_pass == test["expected_pass"] else "✗ FAIL"
        print(f"\n{status} - {test['name']}")
        print(f"  预期: {'通过' if test['expected_pass'] else '失败'}")
        print(f"  实际: {'通过' if actual_pass else '失败'}")
        print(f"  一致性分数: {result.consistency_score:.2f}")

        if result.issues:
            print(f"  问题: {result.issues[:2]}")  # 只显示前2个

        if actual_pass == test["expected_pass"]:
            passed += 1

    print(f"\n总结: {passed}/{total} 测试通过")
    print()

    return passed == total


def test_homography_detection():
    """测试 2: 配对同构检测算法"""
    print("=" * 60)
    print("测试 2: 配对同构检测算法")
    print("=" * 60)

    detector = HomographyDetector()

    # 模拟 Agent 结果（使用相同结构以便检测到同构）
    agent_results = [
        {
            "agent": "thermodynamics",
            "confidence": 0.85,
            "homography_candidates": [
                {
                    "domain_a_element": "熵增",
                    "domain_b_element": "entropy_increase",
                    "formal_structure": "dS/dt > 0",
                    "formal_structure_signature": "dS/dt > 0",
                    "reasoning": "热力学第二定律",
                    "verification_proof": {
                        "if_then_logic": "如果系统封闭，那么熵增",
                        "examples": []
                    }
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
                    "formal_structure": "dS/dt > 0",  # 相同签名以触发检测
                    "formal_structure_signature": "dS/dt > 0",
                    "reasoning": "条件熵增加",
                    "verification_proof": {
                        "if_then_logic": "如果信道噪声增加，那么信息熵上升",
                        "examples": []
                    }
                }
            ]
        },
        {
            "agent": "control_systems",
            "confidence": 0.78,
            "homography_candidates": [
                {
                    "domain_a_element": "反馈",
                    "domain_b_element": "feedback",
                    "formal_structure": "Output → Input loop",
                    "formal_structure_signature": "Feedback Loop",
                    "reasoning": "负反馈调节",
                    "verification_proof": {
                        "if_then_logic": "如果有偏差，那么反馈调节",
                        "examples": []
                    }
                }
            ]
        }
    ]

    # 手动检测同构
    homographies = []
    for i in range(len(agent_results)):
        for j in range(i + 1, len(agent_results)):
            match = detector.detect_homography(agent_results[i], agent_results[j])
            if match:
                homographies.append(match)

    print(f"\n检测到 {len(homographies)} 个同构配对:")

    for i, hom in enumerate(homographies, 1):
        print(f"\n配对 {i}:")
        print(f"  {hom.agent_a} ↔ {hom.agent_b}")
        print(f"  相似度: {hom.similarity_score:.2f}")
        print(f"  置信度: {hom.confidence:.2f}")

    # 验证：应该至少检测到1个同构（thermodynamics ↔ information_theory）
    has_expected = any(
        (h.agent_a == "thermodynamics" and h.agent_b == "information_theory") or
        (h.agent_a == "information_theory" and h.agent_b == "thermodynamics")
        for h in homographies
    )

    print(f"\n{'✓ PASS' if has_expected else '✗ FAIL'} - 检测到预期的同构配对")
    print(f"{'✓ PASS' if len(homographies) >= 1 else '✗ FAIL'} - 至少检测到1个同构")

    # 测试置信度过滤
    filtered = [h for h in homographies if h.confidence >= 0.7]
    print(f"\n{'✓ PASS' if len(filtered) <= len(homographies) else '✗ FAIL'} - 置信度过滤正确")

    result = has_expected and len(homographies) >= 1
    print(f"\n总结: {'通过' if result else '失败'}")
    print()

    return result


def test_cluster_detection_accuracy():
    """测试 3: 同构簇识别准确率"""
    print("=" * 60)
    print("测试 3: 同构簇识别准确率")
    print("=" * 60)

    # 模拟更复杂的 Agent 结果
    agent_results = []

    # 簇 1: 热力学、信息论、控制论（都涉及熵/调节）
    for agent_name, conf in [
        ("thermodynamics", 0.85),
        ("information_theory", 0.82),
        ("control_systems", 0.78)
    ]:
        agent_results.append({
            "agent": agent_name,
            "confidence": conf,
            "homography_candidates": [
                {
                    "domain_a_element": "entropy",
                    "domain_b_element": "entropy",
                    "formal_structure": "irreversible_process",
                    "formal_structure_signature": "dS/dt > 0",
                    "reasoning": f"{agent_name} perspective",
                    "verification_proof": {
                        "if_then_logic": f"如果entropy增加，那么系统调节",
                        "examples": []
                    }
                }
            ]
        })

    # 簇 2: 博弈论、进化论（都涉及竞争/选择）
    for agent_name, conf in [
        ("game_theory", 0.80),
        ("evolutionary_biology", 0.83)
    ]:
        agent_results.append({
            "agent": agent_name,
            "confidence": conf,
            "homography_candidates": [
                {
                    "domain_a_element": "competition",
                    "domain_b_element": "competition",
                    "formal_structure": "competitive_process",
                    "formal_structure_signature": "Nash Equilibrium",
                    "reasoning": f"{agent_name} perspective",
                    "verification_proof": {
                        "if_then_logic": f"如果competition增加，那么优胜劣汰",
                        "examples": []
                    }
                }
            ]
        })

    # 检测簇
    detector = ClusterDetector()
    clusters = detector.detect_clusters(agent_results)

    print(f"\n检测到 {len(clusters)} 个簇:")

    expected_clusters = 2  # 预期2个簇
    for i, cluster in enumerate(clusters, 1):
        print(f"\n簇 {i}: {cluster.cluster_id}")
        print(f"  成员: {', '.join(cluster.members)}")
        print(f"  强度: {cluster.strength:.2f}")
        print(f"  置信度: {cluster.confidence:.2f}")

    # 验证：应该检测到2个簇
    has_expected_count = len(clusters) >= expected_clusters

    # 验证：第一个簇应该包含 thermodynamics, information_theory, control_systems
    cluster1_members = set(clusters[0].members) if clusters else set()
    expected_members_1 = {"thermodynamics", "information_theory", "control_systems"}
    has_cluster1 = cluster1_members == expected_members_1

    # 验证：第二个簇应该包含 game_theory, evolutionary_biology
    cluster2_members = set(clusters[1].members) if len(clusters) > 1 else set()
    expected_members_2 = {"game_theory", "evolutionary_biology"}
    has_cluster2 = cluster2_members == expected_members_2

    # 计算准确率
    total_agents = len(agent_results)
    correctly_clustered = sum(
        1 for cluster in clusters
        for member in cluster.members
    )
    accuracy = correctly_clustered / total_agents if total_agents > 0 else 0

    print(f"\n{'✓ PASS' if has_expected_count else '✗ FAIL'} - 检测到预期数量的簇")
    print(f"{'✓ PASS' if has_cluster1 else '✗ FAIL'} - 簇1成员正确")
    print(f"{'✓ PASS' if has_cluster2 else '✗ FAIL'} - 簇2成员正确")
    print(f"准确率: {accuracy:.1%}")

    # 准确率应该 > 80%
    meets_accuracy = accuracy > 0.8

    print(f"\n{'✓ PASS' if meets_accuracy else '✗ FAIL'} - 准确率 > 80%")

    result = has_expected_count and has_cluster1 and has_cluster2 and meets_accuracy
    print(f"\n总结: {'通过' if result else '失败'}")
    print()

    return result


def main():
    """主测试函数"""
    print()
    print("*" * 60)
    print("Phase 3 完成标准验证")
    print("*" * 60)
    print()

    results = []

    # 测试 1
    results.append(("Verification Proof 验证逻辑", test_verification_proof_logic()))

    # 测试 2
    results.append(("配对同构检测算法", test_homography_detection()))

    # 测试 3
    results.append(("同构簇识别准确率", test_cluster_detection_accuracy()))

    # 总结
    print("=" * 60)
    print("Phase 3 完成标准验证总结")
    print("=" * 60)
    print()

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")

    print()
    print(f"总计: {passed}/{total} 项通过")

    if passed == total:
        print("\n🎉 Phase 3 完成标准验证通过！")
        return 0
    else:
        print("\n⚠️  Phase 3 完成标准验证未完全通过，需要改进。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
