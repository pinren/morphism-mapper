#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Team 集成辅助函数
用于 Agent Team Leader 调用 Python 模块
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict

# Skill 基础路径
SKILL_BASE = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_BASE / "scripts"
ASSETS_DIR = SKILL_BASE / "assets"
REFERENCES_DIR = SKILL_BASE / "references"
KNOWLEDGE_DIR = SKILL_BASE / "knowledge"

# 临时文件路径
TEMP_DIR = Path("/tmp")
MORPHISM_TEMP = TEMP_DIR / "morphism_swarm"


# ============================================================================
# Blind Protocol: 防止互相抄作业的结构指纹系统 (Phase 4.1 第一道防线)
# ============================================================================

@dataclass
class StructuralFingerprint:
    """
    结构指纹 - 4维布尔值用于聚类同构 Domain Agents

    设计哲学：只有指纹匹配的 Domain Agents 才被允许进行"自然变换"通信
    这防止了 Agents 互相抄袭，强制独立思考
    """
    is_cyclic: bool           # 是否存在循环因果?
    is_deterministic: bool    # 是否确定性系统? (vs 概率性/随机性)
    has_agent_agency: bool    # 个体是否有自由意志? (vs 完全决定论)
    is_zero_sum: bool         # 是否零和博弈? (vs 正和)

    def to_tuple(self) -> Tuple[bool, bool, bool, bool]:
        """转换为元组，用于聚类比较"""
        return (self.is_cyclic, self.is_deterministic, self.has_agent_agency, self.is_zero_sum)

    def __str__(self) -> str:
        """友好字符串表示"""
        return f"Cyclic:{self.is_cyclic}|Deterministic:{self.is_deterministic}|Agency:{self.has_agent_agency}|ZeroSum:{self.is_zero_sum}"

    @classmethod
    def from_dict(cls, data: Dict[str, bool]) -> 'StructuralFingerprint':
        """从字典创建"""
        return cls(
            is_cyclic=data.get("is_cyclic", False),
            is_deterministic=data.get("is_deterministic", False),
            has_agent_agency=data.get("has_agent_agency", False),
            is_zero_sum=data.get("is_zero_sum", False)
        )


def generate_structural_fingerprint_from_morphisms(
    objects: List[str],
    morphisms: List[Dict[str, str]]
) -> StructuralFingerprint:
    """
    从范畴骨架自动推断结构指纹

    Args:
        objects: Objects 列表
        morphisms: Morphisms 列表

    Returns:
        推断的结构指纹
    """
    # 启发式规则：从态射描述中推断结构特征

    # 1. 检测循环性
    cyclic_keywords = ["循环", "反馈", "迭代", "自指", "递归", "回路", "周期", "oscillat", "cycle", "feedback", "loop"]
    is_cyclic = any(
        any(kw in m.get("dynamics", "").lower() for kw in cyclic_keywords)
        for m in morphisms
    )

    # 2. 检测确定性
    deterministic_keywords = ["必然", "确定", "法则", "定律", "方程", "formula", "law", "deterministic"]
    probabilistic_keywords = ["随机", "概率", "可能", "不确定", "概率", "random", "probabilistic", "stochastic"]
    has_deterministic = any(kw in str(morphisms).lower() for kw in deterministic_keywords)
    has_probabilistic = any(kw in str(morphisms).lower() for kw in probabilistic_keywords)
    is_deterministic = has_deterministic and not has_probabilistic

    # 3. 检测自由意志
    agency_keywords = ["决策", "选择", "意志", "主观", "意识", "choice", "decision", "will", "agency"]
    has_agency = any(
        any(kw in m.get("dynamics", "").lower() or kw in obj.lower() for kw in agency_keywords)
        for m in morphisms
        for obj in objects
    )

    # 4. 检测零和
    zero_sum_keywords = ["零和", "输赢", "胜负", "竞争", "zero-sum", "win-lose", "rivalry"]
    positive_sum_keywords = ["共赢", "互利", "合作", "正和", "win-win", "cooperation"]
    has_zero_sum = any(kw in str(morphisms).lower() for kw in zero_sum_keywords)
    has_positive_sum = any(kw in str(morphisms).lower() for kw in positive_sum_keywords)
    is_zero_sum = has_zero_sum and not has_positive_sum

    return StructuralFingerprint(
        is_cyclic=is_cyclic,
        is_deterministic=is_deterministic,
        has_agent_agency=has_agency,
        is_zero_sum=is_zero_sum
    )


def cluster_by_fingerprint(
    agent_fingerprints: Dict[str, StructuralFingerprint]
) -> List[Dict[str, Any]]:
    """
    根据结构指纹聚类 Domain Agents

    Args:
        agent_fingerprints: {agent_name: StructuralFingerprint}

    Returns:
        聚类结果列表，每个簇包含:
        {
            "cluster_id": str,
            "fingerprint": StructuralFingerprint,
            "members": List[str],
            "size": int
        }
    """
    # 按指纹分组
    fingerprint_groups = defaultdict(list)
    for agent_name, fingerprint in agent_fingerprints.items():
        key = fingerprint.to_tuple()
        fingerprint_groups[key].append(agent_name)

    # 构建聚类结果
    clusters = []
    for i, (fingerprint_tuple, members) in enumerate(fingerprint_groups.items()):
        clusters.append({
            "cluster_id": f"cluster_{i+1}",
            "fingerprint": StructuralFingerprint(*fingerprint_tuple),
            "members": members,
            "size": len(members)
        })

    # 按 size 降序排序
    clusters.sort(key=lambda x: x["size"], reverse=True)

    return clusters


def validate_fingerprint_cluster_for_natural_transformation(
    cluster: Dict[str, Any]
) -> Tuple[bool, str]:
    """
    验证聚类是否可以启动"自然变换"通信

    规则：
    - 只有 size >= 2 的簇才允许通信（避免孤狼）
    - 单人簇被标记为"独特视角"，等待后续整合

    Args:
        cluster: 聚类结果字典

    Returns:
        (is_valid, reason) 元组
    """
    if cluster["size"] >= 2:
        return True, f"✅ 簇 {cluster['cluster_id']} 有 {cluster['size']} 个成员，可以启动自然变换通信"
    else:
        return False, f"⚠️ 簇 {cluster['cluster_id']} 仅有 1 个成员 ({cluster['members'][0]})，标记为独特视角，等待整合"


def save_fingerprint_clusters(
    clusters: List[Dict[str, Any]],
    exploration_id: str
) -> Path:
    """
    保存指纹聚类结果到文件

    Args:
        clusters: 聚类结果列表
        exploration_id: 探索 ID

    Returns:
        保存的文件路径
    """
    MORPHISM_TEMP.mkdir(exist_ok=True)
    (MORPHISM_TEMP / "fingerprints").mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cluster_file = MORPHISM_TEMP / "fingerprints" / f"{exploration_id}_{timestamp}.json"

    # 序列化（将 dataclass 转为 dict）
    serializable_clusters = []
    for cluster in clusters:
        cluster_copy = cluster.copy()
        cluster_copy["fingerprint"] = cluster["fingerprint"].__dict__
        serializable_clusters.append(cluster_copy)

    with open(cluster_file, "w", encoding="utf-8") as f:
        json.dump({
            "exploration_id": exploration_id,
            "timestamp": timestamp,
            "clusters": serializable_clusters,
            "total_clusters": len(clusters),
            "valid_clusters": sum(1 for c in clusters if c["size"] >= 2)
        }, f, ensure_ascii=False, indent=2)

    return cluster_file


# ============================================================================
# 原有辅助函数
# ============================================================================

def call_domain_selector(
    objects: List[str],
    morphisms: List[Dict[str, str]],
    user_profile: Optional[Dict[str, Any]] = None,
    top_k: int = 5
) -> Dict[str, Any]:
    """
    调用 domain_selector.py 进行领域选择

    Args:
        objects: Phase 1 提取的 Objects
        morphisms: Phase 1 提取的 Morphisms
        user_profile: 用户画像 (可选)
        top_k: 返回前 K 个推荐领域

    Returns:
        {
            "top_domains": [
                {
                    "domain": "thermodynamics",
                    "score": 0.85,
                    "best_matches": [...],
                    "reasoning": "..."
                }
            ],
            "user_tags": [...],
            "complexity_level": "simple"
        }
    """
    # 导入 DomainSelector 类
    sys.path.insert(0, str(SCRIPTS_DIR))
    from domain_selector import DomainSelector

    # 创建 selector 实例
    selector = DomainSelector()

    # 转换 user_profile 格式
    profile_type = None
    if user_profile and "identity" in user_profile:
        identity = user_profile["identity"]
        # 映射用户类型到 domain_selector 预期的格式
        profile_map = {
            "高管": "tech_executive",
            "创业者": "entrepreneur",
            "产品经理": "product_manager",
            "投资者": "investor",
            "学生": "student",
            "独立开发者": "indie_developer"
        }
        profile_type = profile_map.get(identity, identity)

    # 调用 select_domains
    result = selector.select_domains(
        objects=objects,
        morphisms=morphisms,
        user_profile=profile_type,
        top_n=top_k
    )

    return result


def create_broadcast_message(
    user_query: str,
    objects: List[str],
    morphisms: List[Dict[str, str]],
    user_profile: Dict[str, Any]
) -> Dict[str, Any]:
    """
    创建广播消息 (Phase 3 输入)

    Args:
        user_query: 用户问题
        objects: Objects 列表
        morphisms: Morphisms 列表
        user_profile: 用户画像

    Returns:
        广播消息字典
    """
    return {
        "user_query": user_query,
        "category_skeleton": {
            "objects": objects,
            "morphisms": morphisms
        },
        "user_profile": user_profile,
        "timestamp": datetime.now().isoformat()
    }


def save_broadcast_message(broadcast: Dict[str, Any]) -> Path:
    """
    保存广播消息到文件

    Args:
        broadcast: 广播消息字典

    Returns:
        保存的文件路径
    """
    MORPHISM_TEMP.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    broadcast_file = MORPHISM_TEMP / f"broadcast_{timestamp}.json"

    with open(broadcast_file, "w", encoding="utf-8") as f:
        json.dump(broadcast, f, ensure_ascii=False, indent=2)

    return broadcast_file


def load_domain_agent_results(domain: str) -> Optional[Dict[str, Any]]:
    """
    加载 Domain Agent 的结果

    Args:
        domain: 领域名称

    Returns:
        Domain Agent 结果字典，如果文件不存在返回 None
    """
    result_file = MORPHISM_TEMP / f"results" / f"{domain}.json"

    if not result_file.exists():
        return None

    with open(result_file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_all_domain_results(domains: List[str]) -> Dict[str, Dict[str, Any]]:
    """
    加载所有 Domain Agent 的结果

    Args:
        domains: 领域列表

    Returns:
        {domain: result} 字典
    """
    results = {}
    for domain in domains:
        result = load_domain_agent_results(domain)
        if result:
            results[domain] = result

    return results


def create_exploration_report(
    exploration_id: str,
    user_query: str,
    user_profile: Dict[str, Any],
    objects: List[str],
    morphisms: List[Dict[str, str]],
    participating_agents: List[str],
    _domain_results: Dict[str, Dict[str, Any]],  # 保留用于未来扩展
    synthesis: Dict[str, Any],
    exploration_duration: float
) -> str:
    """
    创建探索报告 Markdown 文档

    Args:
        exploration_id: 探索 ID
        user_query: 用户问题
        user_profile: 用户画像
        objects: Objects 列表
        morphisms: Morphisms 列表
        participating_agents: 参与的 Agent 列表
        _domain_results: 领域结果字典 (预留用于未来扩展)
        synthesis: 合成结果
        exploration_duration: 探索时长（秒）

    Returns:
        报告文件路径
    """
    # 确保目录存在
    KNOWLEDGE_DIR.mkdir(exist_ok=True)
    (KNOWLEDGE_DIR / "exploration_history").mkdir(exist_ok=True)

    # 生成文件名
    today = datetime.now().strftime("%Y%m%d")
    report_file = KNOWLEDGE_DIR / "exploration_history" / f"{today}-exploration.md"

    # 构建 Markdown 报告
    report_lines = [
        f"# Morphism Swarm 探索报告",
        f"**探索ID**: {exploration_id}",
        f"**时间**: {datetime.now().isoformat()}",
        "",
        "## 用户问题",
        f"> {user_query}",
        "",
        "## 用户画像",
        f"- **身份**: {user_profile.get('identity', '未知')}",
        f"- **资源**: {', '.join(user_profile.get('resources', []))}",
        f"- **约束**: {', '.join(user_profile.get('constraints', []))}",
        "",
        "## 范畴骨架",
        f"**Objects**: {', '.join(objects)}",
        "",
        "**Morphisms**:",
    ]

    for m in morphisms:
        report_lines.append(f"- {m.get('from', '?')} → {m.get('to', '?')}: {m.get('dynamics', '')}")

    report_lines.extend([
        "",
        "## 参与 Agents",
        f"**领域数量**: {len(participating_agents)}",
        f"**领域列表**: {', '.join(participating_agents)}",
        f"**探索时长**: {exploration_duration:.1f}秒",
        "",
    ])

    # 同构簇
    if synthesis.get("homography_clusters"):
        report_lines.append("## 同构簇发现")
        for cluster in synthesis["homography_clusters"]:
            report_lines.append(f"### 簇 {cluster['cluster_id']}")
            report_lines.append(f"- **成员**: {', '.join(cluster['members'])}")
            report_lines.append(f"- **置信度**: {cluster.get('confidence', 0):.2f}")
            report_lines.append("")

    # Limit
    report_lines.extend([
        "## Limit（跨域共识）",
        "### 核心洞察",
        synthesis.get("limit", {}).get("insight", "无"),
        "",
        "### 结构描述",
        "```",
        synthesis.get("limit", {}).get("structure", ""),
        "```",
        "",
        "### 形式化映射",
        synthesis.get("limit", {}).get("mapping", ""),
        "",
        f"**稳定性评分**: {synthesis.get('limit', {}).get('stability', 0)}/5",
        "",
    ])

    # Colimit
    unique_contributions = synthesis.get("colimit", {}).get("unique_contributions", {})
    report_lines.extend([
        "## Colimit（互补整合）",
        "### 独特贡献",
    ])

    for domain, contribution in unique_contributions.items():
        report_lines.append(f"- **{domain}**: {contribution}")

    report_lines.extend([
        "",
        "### 整合策略",
        synthesis.get("colimit", {}).get("integration_strategy", "无"),
        "",
    ])

    # 质量指标
    metrics = synthesis.get("quality_metrics", {})
    report_lines.extend([
        "## 质量指标",
        f"- **Limit 质量**: {metrics.get('limit_quality', 0):.2f}",
        f"- **Colimit 质量**: {metrics.get('colimit_quality', 0):.2f}",
        f"- **整体成功**: {metrics.get('overall_success', 0):.2f}",
        f"- **Dissensus Metric**: {metrics.get('dissensus_metric', 0)}/100",
        f"- **Trivial Limit 通过**: {metrics.get('trivial_limit_passed', False)}",
        "",
        "\n" + "=" * 80 + "\n"
    ])

    # 追加到文件
    with open(report_file, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    return str(report_file)


def apply_tier_balance(
    top_domains: List[Dict[str, Any]],
    tier_config: Optional[Dict[str, int]] = None
) -> List[str]:
    """
    应用 Tier Balance 策略选择领域

    Args:
        top_domains: domain_selector 返回的 Top K 领域
        tier_config: 层级配置 {tier: count}

    Returns:
        选中的领域列表
    """
    # 加载领域配置
    config_file = ASSETS_DIR / "agents" / "config" / "domain_agents.json"
    with open(config_file, "r", encoding="utf-8") as f:
        domain_config = json.load(f)

    # 默认层级配置
    if tier_config is None:
        tier_config = {
            "tier_1": 2,  # 公理化领域
            "tier_2": 2,  # 应用领域
            "tier_3": 1,  # 实践领域
        }

    # 按层级分组
    tier_groups = {
        "tier_1": [],
        "tier_2": [],
        "tier_3": [],
        "tier_4": []
    }

    for domain_info in top_domains:
        domain = domain_info["domain"]
        tier = domain_config["domains"].get(domain, {}).get("complexity_tier", "tier_2")
        if tier in tier_groups:
            tier_groups[tier].append(domain)

    # 选择领域
    selected = []
    for tier, count in tier_config.items():
        if tier in tier_groups:
            selected.extend(tier_groups[tier][:count])

    return selected


def select_wildcard_domain(seeded_domains: List[str]) -> str:
    """
    选择 Wildcard 领域

    Args:
        seeded_domains: 已选中的领域列表

    Returns:
        Wildcard 领域名称
    """
    # 加载 wildcard 候选
    config_file = ASSETS_DIR / "agents" / "config" / "domain_agents.json"
    with open(config_file, "r", encoding="utf-8") as f:
        domain_config = json.load(f)

    # 获取 wildcard_candidates
    all_wildcards = []
    for domain, config in domain_config["domains"].items():
        if domain not in seeded_domains:
            all_wildcards.extend(config.get("wildcard_candidates", []))

    # 去重并排除已选中
    wildcard_pool = list(set(all_wildcards) - set(seeded_domains))

    if not wildcard_pool:
        # Fallback: 随机选择一个非 seeded 领域
        all_domains = list(domain_config["domains"].keys())
        wildcard_pool = list(set(all_domains) - set(seeded_domains))

    import random
    return random.choice(wildcard_pool)


# CLI 接口
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Agent Team 集成辅助函数")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # domain-selector 命令
    ds_parser = subparsers.add_parser("domain-selector", help="调用领域选择器")
    ds_parser.add_argument("--input", required=True, help="输入 JSON 文件路径")
    ds_parser.add_argument("--top-k", type=int, default=5, help="返回 Top K 领域")

    # tier-balance 命令
    tb_parser = subparsers.add_parser("tier-balance", help="应用 Tier Balance 策略")
    tb_parser.add_argument("--domains", required=True, help="领域列表 (逗号分隔)")

    # wildcard 命令
    wc_parser = subparsers.add_parser("wildcard", help="选择 Wildcard 领域")
    wc_parser.add_argument("--seeded", required=True, help="已选中领域 (逗号分隔)")

    # fingerprint 命令 (NEW - Blind Protocol)
    fp_parser = subparsers.add_parser("fingerprint", help="从范畴骨架生成结构指纹")
    fp_parser.add_argument("--input", required=True, help="输入 JSON 文件路径 (包含 objects 和 morphisms)")

    # cluster-fingerprints 命令 (NEW - Blind Protocol)
    cf_parser = subparsers.add_parser("cluster-fingerprints", help="根据结构指纹聚类 Domain Agents")
    cf_parser.add_argument("--input", required=True, help="输入 JSON 文件路径 (包含 agent_fingerprints)")

    args = parser.parse_args()

    if args.command == "domain-selector":
        with open(args.input, "r", encoding="utf-8") as f:
            input_data = json.load(f)

        result = call_domain_selector(
            objects=input_data.get("objects", []),
            morphisms=input_data.get("morphisms", []),
            user_profile=input_data.get("user_profile"),
            top_k=args.top_k
        )

        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "tier-balance":
        domains = args.domains.split(",")
        top_domains = [{"domain": d, "score": 1.0} for d in domains]
        selected = apply_tier_balance(top_domains)
        print(",".join(selected))

    elif args.command == "wildcard":
        seeded = args.seeded.split(",")
        wildcard = select_wildcard_domain(seeded)
        print(wildcard)

    elif args.command == "fingerprint":
        # 从范畴骨架生成结构指纹
        with open(args.input, "r", encoding="utf-8") as f:
            input_data = json.load(f)

        fingerprint = generate_structural_fingerprint_from_morphisms(
            objects=input_data.get("objects", []),
            morphisms=input_data.get("morphisms", [])
        )

        result = {
            "structural_fingerprint": fingerprint.__dict__,
            "description": str(fingerprint),
            "interpretation": {
                "is_cyclic": "系统存在循环因果或反馈回路" if fingerprint.is_cyclic else "系统为非循环线性结构",
                "is_deterministic": "系统为确定性系统" if fingerprint.is_deterministic else "系统包含随机性或概率性因素",
                "has_agent_agency": "系统中的个体具有自由意志和决策能力" if fingerprint.has_agent_agency else "系统为完全决定论，无自由意志",
                "is_zero_sum": "系统为零和博弈（此消彼长）" if fingerprint.is_zero_sum else "系统存在正和可能（共赢）"
            }
        }

        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "cluster-fingerprints":
        # 根据结构指纹聚类 Domain Agents
        with open(args.input, "r", encoding="utf-8") as f:
            input_data = json.load(f)

        # 转换为 StructuralFingerprint 对象
        agent_fingerprints = {}
        for agent_name, fp_dict in input_data.get("agent_fingerprints", {}).items():
            agent_fingerprints[agent_name] = StructuralFingerprint.from_dict(fp_dict)

        # 聚类
        clusters = cluster_by_fingerprint(agent_fingerprints)

        # 验证每个簇
        result = {
            "total_agents": len(agent_fingerprints),
            "total_clusters": len(clusters),
            "valid_clusters": sum(1 for c in clusters if c["size"] >= 2),
            "unique_perspectives": sum(1 for c in clusters if c["size"] == 1),
            "clusters": []
        }

        for cluster in clusters:
            is_valid, reason = validate_fingerprint_cluster_for_natural_transformation(cluster)
            result["clusters"].append({
                "cluster_id": cluster["cluster_id"],
                "fingerprint": cluster["fingerprint"].__dict__,
                "description": str(cluster["fingerprint"]),
                "members": cluster["members"],
                "size": cluster["size"],
                "can_communicate": is_valid,
                "reason": reason
            })

        print(json.dumps(result, ensure_ascii=False, indent=2))
