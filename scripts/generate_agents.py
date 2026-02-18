#!/usr/bin/env python3
import os
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from dynamic_agent_generator import DynamicAgentGenerator


def resolve_prompt_output_dir() -> Path:
    """
    统一写入探索目录，避免使用 /tmp 或项目目录。
    """
    configured = os.environ.get("MORPHISM_EXPLORATION_PATH")
    if configured:
        exploration_path = Path(configured).expanduser().resolve()
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        exploration_path = (
            Path.home() / ".morphism_mapper" / "explorations" / f"{timestamp}_generate_agents"
        ).resolve()
        os.environ["MORPHISM_EXPLORATION_PATH"] = str(exploration_path)
        os.environ["MORPHISM_PERSISTENCE_MODE"] = "production"

    output_dir = exploration_path / "artifacts" / "generated_prompts"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

# 范畴骨架
category_skeleton = {
    "objects": [
        {"name": "中国", "attributes": "主体A, 全球制造业中心"},
        {"name": "美国", "attributes": "主体B, 全球消费市场"},
        {"name": "特朗普", "attributes": "关键决策者, 不可预测性"},
        {"name": "2026中期选举", "attributes": "时间触发器, 政治转折点"},
        {"name": "贸易战", "attributes": "博弈场域, 双边对抗"},
        {"name": "关税政策", "attributes": "核心工具, 经济武器"},
        {"name": "全球产业链", "attributes": "博弈标的, 供应链网络"}
    ],
    "morphisms": [
        {"from": "选举结果", "to": "政策转向", "dynamics": "时间延迟效应"},
        {"from": "中期选举", "to": "权力结构变化", "dynamics": "国会控制权争夺"},
        {"from": "关税战", "to": "经济博弈", "dynamics": "成本转嫁与反馈调节"},
        {"from": "特朗普决策", "to": "全球供应链扰动", "dynamics": "不确定性与预测应对"},
        {"from": "政治周期", "to": "贸易策略调整", "dynamics": "时间窗口与演化发展"},
        {"from": "选民压力", "to": "政策承诺兑现", "dynamics": "政治约束与博弈竞争"}
    ],
    "核心问题": "特朗普通过2026中期选举后，中美贸易战将如何演变？"
}

# 选择更适合的领域（基于地缘政治博弈特征）
selected_domains = ['game_theory', 'thermodynamics', 'control_systems']

print("=== 生成 Domain Agents ===")
print(f"选中领域: {selected_domains}")
output_dir = resolve_prompt_output_dir()

# 初始化生成器
generator = DynamicAgentGenerator()

# 批量生成 prompts
prompts = generator.generate_batch(
    domains=selected_domains,
    category_skeleton=category_skeleton,
    auto_create=True
)

print(f"\n生成结果:")
for domain, prompt in prompts.items():
    if isinstance(prompt, dict) and prompt.get('action') == 'CREATE_DOMAIN':
        print(f"  {domain}: 需要补盲生成")
    else:
        # 保存 prompt 到文件
        prompt_file = output_dir / f"{domain}_agent_prompt.txt"
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"  {domain}: Prompt 已生成 ({len(prompt)} 字符) -> {prompt_file}")
