#!/usr/bin/env python3
"""
Swarm Orchestrator - 蜂群模式协调器 (v4.0)
协调 Domain Agents 进行并行探索，合成 Limit/Colimit 输出
"""

import json
import asyncio
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime

# 导入 DomainSelector
from domain_selector import DomainSelector, TierBalanceResult


@dataclass
class CategorySkeleton:
    """范畴骨架"""
    objects: List[str]
    morphisms: List[Dict[str, str]]
    identity_composition: List[str]


@dataclass
class UserProfile:
    """用户画像"""
    identity: str
    resources: List[str]
    constraints: List[str]


@dataclass
class BroadcastMessage:
    """广播消息"""
    timestamp: str
    category_skeleton: CategorySkeleton
    user_profile: UserProfile
    seed_strategy: Dict[str, Any]


@dataclass
class MappingResult:
    """领域映射结果"""
    agent: str
    confidence: float
    homography_candidates: List[Dict[str, Any]]
    verification_proof: Optional[Dict[str, Any]]


@dataclass
class HomographyCluster:
    """同构簇"""
    cluster_id: str
    members: List[str]
    shared_structure: str
    confidence: float


@dataclass
class SynthesisResult:
    """综合结果"""
    limit: Dict[str, Any]
    colimit: Dict[str, Any]
    dissensus_metric: float
    trivial_limit_passed: bool
    quality_rating: str


@dataclass
class ExplorationReport:
    """探索报告"""
    timestamp: str
    user_query: str
    user_profile: Dict[str, Any]
    participating_agents: List[str]
    exploration_duration: float
    homography_clusters: List[HomographyCluster]
    synthesis: SynthesisResult
    tier_distribution: Dict[str, List[str]]
    wildcard_agent: Optional[str]


class SwarmOrchestrator:
    """蜂群模式协调器 v4.0"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化协调器

        Args:
            config_path: 配置文件路径，默认为 agents/config/domain_agents.json
        """
        script_dir = Path(__file__).parent.parent

        # 初始化 DomainSelector
        self.domain_selector = DomainSelector()

        # 加载配置
        if config_path is None:
            config_path = str(script_dir / "agents" / "config" / "domain_agents.json")
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.domain_info = self.config.get("domains", {})
        self.swarm_protocol = self._load_swarm_protocol()
        self.synthesizer_config = self._load_synthesizer_config()

    def _load_swarm_protocol(self) -> Dict:
        """加载蜂群协议配置"""
        protocol_path = (
            Path(__file__).parent.parent /
            "agents" / "config" / "swarm_protocol.json"
        )
        with open(protocol_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_synthesizer_config(self) -> Dict:
        """加载 Synthesizer 配置"""
        config_path = (
            Path(__file__).parent.parent /
            "agents" / "config" / "synthesizer.json"
        )
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def extract_category_skeleton(
        self,
        user_query: str,
        user_profile_input: Optional[Dict[str, Any]] = None
    ) -> tuple[CategorySkeleton, UserProfile]:
        """
        提取范畴骨架

        Args:
            user_query: 用户问题
            user_profile_input: 用户画像输入

        Returns:
            (CategorySkeleton, UserProfile)
        """
        # TODO: 实现实际的 NLP 提取逻辑
        # 当前使用简化版本

        # 简化的 Objects 提取（基于关键词）
        objects = self._extract_objects(user_query)

        # 简化的 Morphisms 提取
        morphisms = self._extract_morphisms(user_query)

        # Identity & Composition
        identity_composition = self._extract_identity_composition(user_query)

        category_skeleton = CategorySkeleton(
            objects=objects,
            morphisms=morphisms,
            identity_composition=identity_composition
        )

        # 用户画像
        if user_profile_input:
            user_profile = UserProfile(
                identity=user_profile_input.get("identity", "未知"),
                resources=user_profile_input.get("resources", []),
                constraints=user_profile_input.get("constraints", [])
            )
        else:
            user_profile = UserProfile(
                identity="未知",
                resources=[],
                constraints=[]
            )

        return category_skeleton, user_profile

    def _extract_objects(self, query: str) -> List[str]:
        """提取核心实体（简化版）"""
        # TODO: 使用 NLP 模型提取
        # 当前使用关键词匹配
        keywords = {
            "产品": ["产品", "服务", "软件", "平台", "系统"],
            "用户": ["用户", "客户", "消费者", "市场"],
            "团队": ["团队", "组织", "公司", "企业"],
            "增长": ["增长", "发展", "扩张", "规模化"],
            "竞争": ["竞争", "对手", "市场", "行业"]
        }

        objects = []
        for obj, patterns in keywords.items():
            if any(p in query for p in patterns):
                objects.append(obj)

        return objects if objects else ["问题", "解决方案"]

    def _extract_morphisms(self, query: str) -> List[Dict[str, str]]:
        """提取动态关系（简化版）"""
        # TODO: 使用 NLP 模型提取
        # 当前返回默认关系
        return [
            {"from": "问题", "to": "解决方案", "dynamics": "需要解决"}
        ]

    def _extract_identity_composition(self, query: str) -> List[str]:
        """提取稳态机制（简化版）"""
        # TODO: 使用 NLP 模型提取
        return ["当前状态维持"]

    def should_trigger_swarm_mode(
        self,
        fast_result: Dict[str, Any],
        user_request: Optional[str] = None
    ) -> bool:
        """
        判断是否触发 Swarm Mode

        Args:
            fast_result: Fast Mode 结果
            user_request: 用户明确请求

        Returns:
            是否触发 Swarm Mode
        """
        # 用户明确请求
        if user_request and any(kw in user_request.lower() for kw in
           ["swarm", "蜂群", "多领域", "探索", "深度分析"]):
            return True

        # 置信度 < 70%
        if fast_result.get("confidence", 100) < 70:
            return True

        # 关键词触发
        # TODO: 从 user_query 中检测

        return False

    async def run_swarm_exploration(
        self,
        user_query: str,
        user_profile_input: Optional[Dict[str, Any]] = None,
        user_request: Optional[str] = None
    ) -> ExplorationReport:
        """
        执行蜂群探索

        Args:
            user_query: 用户问题
            user_profile_input: 用户画像
            user_request: 用户明确请求

        Returns:
            ExplorationReport
        """
        start_time = time.time()

        # Phase 1: 提取范畴骨架
        category_skeleton, user_profile = self.extract_category_skeleton(
            user_query, user_profile_input
        )

        # Phase 2: Fast Mode 预筛选
        fast_result = self.domain_selector.select_domains(
            objects=category_skeleton.objects,
            morphisms=category_skeleton.morphisms,
            user_profile=user_profile.identity
        )

        # 判断是否需要 Swarm Mode
        if not self.should_trigger_swarm_mode(fast_result, user_request):
            # 返回 Fast Mode 结果
            return self._create_fast_mode_report(
                user_query, user_profile, fast_result, time.time() - start_time
            )

        # Phase 3: Tier Balance 种子选择
        tier_result = self.domain_selector.tier_balance_selection(
            fast_result["top_domains"]
        )

        # Phase 4: 广播给 Domain Agents
        broadcast_msg = self._create_broadcast_message(
            category_skeleton, user_profile, tier_result
        )

        # Phase 5: 收集 Domain Agents 结果
        mapping_results = await self._collect_domain_agent_results(
            tier_result.selected_domains,
            broadcast_msg
        )

        # 添加 Wildcard Agent
        if tier_result.wildcard_domain:
            wildcard_result = await self._collect_single_agent_result(
                tier_result.wildcard_domain, broadcast_msg
            )
            if wildcard_result:
                mapping_results.append(wildcard_result)

        # Phase 6: 发现同构簇
        homography_clusters = self._discover_homography_clusters(mapping_results)

        # Phase 7: Synthesizer 计算 Limit/Colimit
        synthesis = self._synthesize_results(
            homography_clusters,
            mapping_results,
            category_skeleton,
            user_profile
        )

        # Phase 8: 更新知识图谱
        self._update_knowledge_graph(
            mapping_results,
            homography_clusters,
            synthesis
        )

        # 生成报告
        participating_agents = tier_result.selected_domains.copy()
        if tier_result.wildcard_domain:
            participating_agents.append(tier_result.wildcard_domain)

        report = ExplorationReport(
            timestamp=datetime.now().isoformat(),
            user_query=user_query,
            user_profile={
                "identity": user_profile.identity,
                "resources": user_profile.resources,
                "constraints": user_profile.constraints
            },
            participating_agents=participating_agents,
            exploration_duration=time.time() - start_time,
            homography_clusters=homography_clusters,
            synthesis=synthesis,
            tier_distribution=tier_result.tier_distribution,
            wildcard_agent=tier_result.wildcard_domain
        )

        # Phase 9: 保存探索日志
        self._save_exploration_log(report)

        return report

    def _create_broadcast_message(
        self,
        category_skeleton: CategorySkeleton,
        user_profile: UserProfile,
        tier_result: TierBalanceResult
    ) -> BroadcastMessage:
        """创建广播消息"""
        return BroadcastMessage(
            timestamp=datetime.now().isoformat(),
            category_skeleton=category_skeleton,
            user_profile=user_profile,
            seed_strategy={
                "method": "tier_balance",
                "tiers_selected": tier_result.tier_distribution,
                "wildcard": tier_result.wildcard_domain
            }
        )

    async def _collect_domain_agent_results(
        self,
        domains: List[str],
        broadcast_msg: BroadcastMessage
    ) -> List[MappingResult]:
        """收集 Domain Agents 结果"""
        # TODO: 实现实际的 Agent Team 调用
        # 当前使用模拟结果

        results = []

        for domain in domains:
            result = await self._collect_single_agent_result(domain, broadcast_msg)
            if result:
                results.append(result)

        return results

    async def _collect_single_agent_result(
        self,
        domain: str,
        broadcast_msg: BroadcastMessage
    ) -> Optional[MappingResult]:
        """收集单个 Agent 结果（模拟）"""
        # TODO: 调用实际的 Domain Agent
        # 当前返回模拟数据

        domain_data = self.domain_info.get(domain, {})
        persona_file = domain_data.get("persona", "")

        # 模拟映射结果
        return MappingResult(
            agent=domain,
            confidence=0.75 + (hash(domain) % 20) / 100,  # 0.75-0.95
            homography_candidates=[
                {
                    "domain_a_element": "问题",
                    "domain_b_element": f"{domain}_concept",
                    "formal_structure": f"{domain}_structure",
                    "formal_structure_signature": f"{domain}_signature",
                    "reasoning": f"基于{domain}的分析"
                }
            ],
            verification_proof={
                "if_then_logic": f"如果{domain}条件成立，那么...",
                "examples": []
            }
        )

    def _discover_homography_clusters(
        self,
        mapping_results: List[MappingResult]
    ) -> List[HomographyCluster]:
        """发现同构簇"""
        # TODO: 实现实际的聚类算法
        # 当前返回模拟数据

        if len(mapping_results) < 2:
            return []

        return [
            HomographyCluster(
                cluster_id="cluster_1",
                members=[r.agent for r in mapping_results[:2]],
                shared_structure="模拟共享结构",
                confidence=0.8
            )
        ]

    def _synthesize_results(
        self,
        homography_clusters: List[HomographyCluster],
        mapping_results: List[MappingResult],
        category_skeleton: CategorySkeleton,
        user_profile: UserProfile
    ) -> SynthesisResult:
        """综合结果"""
        # TODO: 实现实际的 Limit/Colimit 计算
        # 当前返回模拟数据

        return SynthesisResult(
            limit={
                "core_insight": "模拟 Limit 洞察",
                "structural_description": "模拟结构性描述",
                "formal_mapping": "模拟形式化映射",
                "stability_rating": 4
            },
            colimit={
                "unique_contributions": [],
                "integration_strategy": "模拟整合策略"
            },
            dissensus_metric=35.0,
            trivial_limit_passed=True,
            quality_rating="ACCEPTABLE"
        )

    def _update_knowledge_graph(
        self,
        mapping_results: List[MappingResult],
        homography_clusters: List[HomographyCluster],
        synthesis: SynthesisResult
    ) -> None:
        """更新知识图谱"""
        # TODO: 实现 homography_graph.json 更新
        pass

    def _save_exploration_log(self, report: ExplorationReport) -> None:
        """保存探索日志"""
        log_dir = Path(__file__).parent.parent / "knowledge" / "exploration_history"
        log_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_file = log_dir / f"{timestamp}-exploration.md"

        # 生成 Markdown 报告
        report_md = self._format_report_as_markdown(report)

        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(report_md)

    def _format_report_as_markdown(self, report: ExplorationReport) -> str:
        """格式化报告为 Markdown"""
        # TODO: 实现完整的 Markdown 格式化
        return f"""# Morphism Swarm 探索报告

## 探索概览

**用户问题**: {report.user_query}
**用户画像**: {report.user_profile.get('identity', '未知')}
**参与 Agents**: {', '.join(report.participating_agents)}
**探索时长**: {report.exploration_duration:.2f}秒

## Tier 分布

{json.dumps(report.tier_distribution, ensure_ascii=False, indent=2)}

**Wildcard Agent**: {report.wildcard_agent or '无'}

## 同构簇发现

{len(report.homography_clusters)} 个同构簇

## 综合结果

### Limit（跨域共识）

{report.synthesis.limit.get('core_insight', '无')}

### Colimit（互补整合）

{report.synthesis.colimit.get('integration_strategy', '无')}

## 质量评估

- **Dissensus Metric**: {report.synthesis.dissensus_metric:.0f}/100
- **Trivial Limit**: {'通过' if report.synthesis.trivial_limit_passed else '未通过'}
- **整体质量**: {report.synthesis.quality_rating}

---
*生成时间: {report.timestamp}*
"""

    def _create_fast_mode_report(
        self,
        user_query: str,
        user_profile: UserProfile,
        fast_result: Dict[str, Any],
        duration: float
    ) -> ExplorationReport:
        """创建 Fast Mode 报告"""
        top_domain = fast_result["top_domains"][0] if fast_result["top_domains"] else None

        return ExplorationReport(
            timestamp=datetime.now().isoformat(),
            user_query=user_query,
            user_profile={
                "identity": user_profile.identity,
                "resources": user_profile.resources,
                "constraints": user_profile.constraints
            },
            participating_agents=[top_domain["domain"]] if top_domain else [],
            exploration_duration=duration,
            homography_clusters=[],
            synthesis=SynthesisResult(
                limit={"core_insight": f"Fast Mode: {top_domain['domain']}" if top_domain else "无匹配"},
                colimit={"integration_strategy": "Fast Mode 不生成 Colimit"},
                dissensus_metric=0.0,
                trivial_limit_passed=True,
                quality_rating="FAST_MODE"
            ),
            tier_distribution={},
            wildcard_agent=None
        )


# ============================================================================
# CLI Interface
# ============================================================================

async def main():
    """主函数"""
    import sys

    orchestrator = SwarmOrchestrator()

    if len(sys.argv) > 1:
        if sys.argv[1] == "--demo":
            # 演示模式
            print("=" * 60)
            print("Swarm Orchestrator Demo (v4.0)")
            print("=" * 60)
            print()

            # 模拟用户查询
            query = "我的 SaaS 产品增长停滞了，需要突破"
            print(f"用户查询: {query}\n")

            report = await orchestrator.run_swarm_exploration(query)

            # 输出报告摘要
            print(f"\n【探索完成】")
            print(f"参与 Agents: {', '.join(report.participating_agents)}")
            print(f"探索时长: {report.exploration_duration:.2f}秒")
            print(f"Dissensus Metric: {report.synthesis.dissensus_metric:.0f}/100")
            print(f"质量评级: {report.synthesis.quality_rating}")

        else:
            print("用法:")
            print("  python swarm_orchestrator.py --demo    运行演示")
    else:
        print("Swarm Orchestrator v4.0")
        print()
        print("用法:")
        print("  python swarm_orchestrator.py --demo    运行演示")


if __name__ == "__main__":
    asyncio.run(main())
