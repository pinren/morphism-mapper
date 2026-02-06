#!/usr/bin/env python3
"""
Enhanced Morphism Tag Annotator
增强版Morphism标签标注器

Usage:
    python enhance_annotations.py
"""

import json
import re
from pathlib import Path

# 扩展的关键词映射（包含更多同义词和相关词）
TAG_KEYWORDS = {
    "feedback_regulation": {
        "primary": ["反馈", "调节", "纠正", "控制", "阻尼", "修正", "调整"],
        "secondary": ["回流", "比较", "响应", "补偿", "抑制", "衰减", "稳定"],
        "weight": 1.0
    },
    "feedforward_anticipation": {
        "primary": ["前馈", "预见", "预测", "提前", "前瞻"],
        "secondary": ["趋势", "外推", "干预", "预防", "预备", "预先"],
        "weight": 1.0
    },
    "learning_adaptation": {
        "primary": ["学习", "适应", "习得", "改进", "经验"],
        "secondary": ["积累", "可塑性", "调整", "优化", "进化", "成长", "成熟"],
        "weight": 1.0
    },
    "evolution_development": {
        "primary": ["演化", "发展", "演替", "进化", "变革"],
        "secondary": ["成长", "成熟", "转变", "进程", "阶段", "历程"],
        "weight": 1.0
    },
    "competition_selection": {
        "primary": ["竞争", "选择", "淘汰", "斗争", "对抗", "博弈"],
        "secondary": ["筛选", "冲突", "争夺", "比拼", "较量", "竞赛"],
        "weight": 1.0
    },
    "cooperation_symbiosis": {
        "primary": ["合作", "共生", "互惠", "协同", "互利"],
        "secondary": ["团结", "协作", "联盟", "整合", "协调", "配合"],
        "weight": 1.0
    },
    "information_processing": {
        "primary": ["信息", "信号", "编码", "解码", "处理"],
        "secondary": ["传递", "流动", "沟通", "认知", "感知", "识别"],
        "weight": 1.0
    },
    "stabilization_equilibrium": {
        "primary": ["稳定", "均衡", "平衡", "收敛", "恢复"],
        "secondary": ["维持", "稳态", "守恒", "持久", "恒定", "固定"],
        "weight": 1.0
    },
    "flow_exchange": {
        "primary": ["流动", "交换", "传递", "循环", "转移"],
        "secondary": ["输送", "传输", "流通", "迁移", "扩散", "传播"],
        "weight": 1.0
    },
    "structural_organization": {
        "primary": ["组织", "结构", "构建", "形成", "整合"],
        "secondary": ["配置", "安排", "系统", "秩序", "建构", "组建"],
        "weight": 1.0
    },
    "optimization_search": {
        "primary": ["优化", "搜索", "求解", "寻找", "改进"],
        "secondary": ["提升", "最大化", "最小化", "效率", "最佳", "最优"],
        "weight": 1.0
    },
    "diffusion_propagation": {
        "primary": ["扩散", "传播", "传染", "级联", "蔓延"],
        "secondary": ["扩展", "散布", "推广", "普及", "传导", "传递"],
        "weight": 1.0
    },
    "transformation_conversion": {
        "primary": ["转化", "转变", "转换", "变化", "转型"],
        "secondary": ["重构", "改变", "质变", "变革", "变易", "转化"],
        "weight": 1.0
    },
    "emergence_generation": {
        "primary": ["涌现", "生成", "产生", "创造", "形成"],
        "secondary": ["出现", "诞生", "创新", "发明", "产生", "发生"],
        "weight": 1.0
    },
    "exploration_exploitation": {
        "primary": ["探索", "利用", "尝试", "试验", "发现"],
        "secondary": ["开拓", "开发", "试错", "实验", "探究", "搜寻"],
        "weight": 1.0
    },
    "oscillation_fluctuation": {
        "primary": ["振荡", "波动", "周期", "涨落", "起伏"],
        "secondary": ["震动", "摆动", "循环", "节奏", "脉动", "震荡"],
        "weight": 1.0
    }
}

def calculate_tag_score(dynamics, tag_config):
    """计算标签匹配分数"""
    score = 0
    
    # Primary keywords: +2分
    for kw in tag_config["primary"]:
        if kw in dynamics:
            score += 2
    
    # Secondary keywords: +1分
    for kw in tag_config["secondary"]:
        if kw in dynamics:
            score += 1
    
    return score * tag_config["weight"]

def extract_tags_enhanced(dynamics, name=""):
    """增强版标签提取"""
    scores = {}
    
    # 从动态描述中提取
    for tag, config in TAG_KEYWORDS.items():
        score = calculate_tag_score(dynamics, config)
        if score > 0:
            scores[tag] = score
    
    # 从Morphism名称中提取（权重较低）
    for tag, config in TAG_KEYWORDS.items():
        score = calculate_tag_score(name, config) * 0.5
        if score > 0:
            scores[tag] = scores.get(tag, 0) + score
    
    # 按分数排序，取前3个
    sorted_tags = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [tag for tag, score in sorted_tags[:3] if score >= 2]

def enhance_database():
    """增强数据库标注"""
    db_path = Path(__file__).parent.parent / "data" / "morphism_tags.json"
    
    with open(db_path, 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    # 统计信息
    total = 0
    annotated = 0
    improved = 0
    
    for domain_name, domain_data in db['domains'].items():
        for morphism in domain_data.get('morphisms', []):
            total += 1
            
            # 如果已有标签且是manual标注，跳过
            if morphism.get('tags') and morphism.get('annotation_method') == 'manual':
                annotated += 1
                continue
            
            # 提取新标签
            dynamics = morphism.get('dynamics', '')
            name = morphism.get('name', '')
            new_tags = extract_tags_enhanced(dynamics, name)
            
            if new_tags:
                old_tags = morphism.get('tags', [])
                if set(new_tags) != set(old_tags):
                    improved += 1
                morphism['tags'] = new_tags
                morphism['annotation_method'] = 'auto'
                annotated += 1
    
    # 保存
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 增强完成!")
    print(f"   总Morphism: {total}")
    print(f"   已标注: {annotated} ({annotated/total*100:.1f}%)")
    print(f"   改进数量: {improved}")

if __name__ == "__main__":
    enhance_database()
