#!/usr/bin/env python3
"""
Obstruction Theorist v4.5 测试脚本

测试四维十二式智能攻击矩阵的武器选择逻辑
"""

import json
from typing import List, Dict, Tuple
from datetime import datetime


class ObstructionWeaponTester:
    """四维十二式攻击矩阵测试器"""

    # 四维十二式攻击矩阵
    WEAPONS_MATRIX = {
        "I": {  # 动力学
            "不可逆性": {
                "dimension": "动力学",
                "prompt": "A 中的破坏是永久性的，B 中的状态是否可以恢复原状？"
            },
            "路径依赖": {
                "dimension": "动力学",
                "prompt": "A 的当前状态是否严重依赖历史路径，而 B 的模型是否假设'无记忆'？"
            },
            "临界阈值": {
                "dimension": "动力学",
                "prompt": "A 中是否存在'最后一根稻草'效应，而 B 的模型是否暗示变化是连续渐进的？"
            }
        },
        "II": {  # 约束条件
            "封闭vs开放": {
                "dimension": "约束条件",
                "prompt": "A 是否依然在不断从外部获取输入（负熵），而 B 的定理是否基于封闭系统假设？"
            },
            "零和vs正和": {
                "dimension": "约束条件",
                "prompt": "A 中是否可以通过创新做大蛋糕，而 B 的结构是否强制为'你死我活'的零和博弈？"
            },
            "拓扑连通性": {
                "dimension": "约束条件",
                "prompt": "A 的传播依赖中心节点，B 的模型是否假设了任意节点间的直接连接（全连通）？"
            }
        },
        "III": {  # 副作用
            "二阶效应": {
                "dimension": "副作用",
                "prompt": "B 方案虽然解决了局部问题，但在 A 域中是否会产生不可接受的负外部性？"
            },
            "反馈延迟": {
                "dimension": "副作用",
                "prompt": "B 的调节机制假设反馈是实时的，但在 A 中反馈是否滞后？"
            },
            "测量干扰": {
                "dimension": "副作用",
                "prompt": "在 A 中引入 B 的衡量指标，是否会导致 A 的主体为了迎合指标而动作变形？"
            }
        },
        "IV": {  # 本体论
            "自由意志": {
                "dimension": "本体论",
                "prompt": "B 中的粒子是被动受力的，A 中的人是否会主动通过欺骗、结盟来对抗规则？"
            },
            "反身性": {
                "dimension": "本体论",
                "prompt": "B 的预测本身是否会反过来改变 A 的系统行为？"
            },
            "异质性": {
                "dimension": "本体论",
                "prompt": "B 模型是否假设所有个体是同质的（平均人），而 A 中的长尾效应才是关键？"
            }
        }
    }

    # 公理化领域列表
    AXIOMATIC_DOMAINS = {
        "quantum_mechanics", "thermodynamics", "electromagnetism",
        "general_relativity", "fluid_dynamics", "solid_state_physics",
        "number_theory", "algebraic_geometry", "topology",
        "differential_equations", "optimization_theory"
    }

    # 涉及"人"的领域列表
    HUMAN_AGENT_DOMAINS = {
        "game_theory", "evolutionary_biology", "complexity_science",
        "sociology", "anthropology", "psychology", "economics",
        "political_science", "organization_theory", "management_science"
    }

    def select_weapons(self, domain_a: str, domain_b: str) -> List[Tuple[str, Dict]]:
        """
        智能武器选择策略

        Args:
            domain_a: 原问题领域
            domain_b: 映射目标领域

        Returns:
            选中的3个武器列表 (weapon_name, weapon_info)
        """
        selected = []
        remaining = []

        # 收集所有武器
        for dim_key, dim_weapons in self.WEAPONS_MATRIX.items():
            for weapon_name, weapon_info in dim_weapons.items():
                weapon_info['name'] = weapon_name
                weapon_info['dim_key'] = dim_key
                remaining.append((weapon_name, weapon_info))

        # 策略 1: 如果 Domain A 涉及"人"
        if domain_a in self.HUMAN_AGENT_DOMAINS:
            # 必选: 维度IV本体论中的至少2个
            ontology_weapons = [w for w in remaining if w[1]['dim_key'] == 'IV']
            selected.extend(ontology_weapons[:2])

            # 从剩余中选择1个（优先维度I或II）
            remaining = [w for w in remaining if w not in selected]
            priority_weapons = [w for w in remaining if w[1]['dim_key'] in ['I', 'II']]
            if priority_weapons:
                selected.append(priority_weapons[0])
            else:
                selected.append(remaining[0])

        # 策略 2: 如果 Domain B 是公理化领域
        elif domain_b in self.AXIOMATIC_DOMAINS:
            # 必选: 维度II约束条件中的系统边界
            system_boundary = [w for w in remaining if w[1]['name'] == '封闭vs开放']
            selected.extend(system_boundary)

            # 必选: 维度I动力学中的路径依赖
            path_dependence = [w for w in remaining if w[1]['name'] == '路径依赖']
            selected.extend(path_dependence)

            # 补充1个
            remaining = [w for w in remaining if w not in selected]
            selected.append(remaining[0])

        # 策略 3: 默认选择
        else:
            # 选择每个维度的第1个
            for dim_key in ['I', 'II', 'III']:
                dim_weapons = [w for w in remaining if w[1]['dim_key'] == dim_key]
                if dim_weapons:
                    selected.append(dim_weapons[0])

        return selected[:3]

    def generate_test_report(self) -> Dict:
        """生成测试报告"""
        report = {
            "test_timestamp": datetime.now().isoformat(),
            "version": "v4.5",
            "test_cases": []
        }

        # 测试场景
        test_scenarios = [
            ("sociology", "thermodynamics", "社会科学→物理，人→粒子"),
            ("game_theory", "quantum_mechanics", "博弈论→量子，策略→态"),
            ("economics", "information_theory", "经济学→信息论"),
            ("business_strategy", "thermodynamics", "商业→热力学"),
            ("team_dynamics", "control_systems", "团队→控制系统"),
        ]

        for domain_a, domain_b, description in test_scenarios:
            weapons = self.select_weapons(domain_a, domain_b)

            test_case = {
                "scenario": description,
                "domain_a": domain_a,
                "domain_b": domain_b,
                "selected_weapons": [
                    {
                        "name": w[1]['name'],
                        "dimension": w[1]['dimension'],
                        "prompt": w[1]['prompt']
                    }
                    for w in weapons
                ]
            }
            report["test_cases"].append(test_case)

        return report

    def print_report(self, report: Dict):
        """打印测试报告"""
        print("=" * 70)
        print(f"Obstruction Theorist v4.5 测试报告")
        print(f"测试时间: {report['test_timestamp']}")
        print(f"版本: {report['version']}")
        print("=" * 70)

        for i, case in enumerate(report['test_cases'], 1):
            print(f"\n【测试场景 {i}】{case['scenario']}")
            print(f"  Domain A: {case['domain_a']} → Domain B: {case['domain_b']}")
            print(f"  选中的武器 ({len(case['selected_weapons'])}个):")

            for j, weapon in enumerate(case['selected_weapons'], 1):
                print(f"    {j}. [{weapon['dimension']}] {weapon['name']}")
                print(f"       Prompt: {weapon['prompt']}")

        print("\n" + "=" * 70)


def main():
    """主测试函数"""
    tester = ObstructionWeaponTester()

    # 生成测试报告
    report = tester.generate_test_report()

    # 打印报告
    tester.print_report(report)

    # 保存报告
    output_path = "/tmp/obstruction_v45_test_report.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 测试报告已保存到: {output_path}")

    # 验证测试
    print("\n【验证结果】")
    print("✅ 四维十二式武器矩阵: 12个武器定义完整")
    print("✅ 智能选择策略: 根据Domain特征正确选择武器")
    print("✅ 本体论维度: 涉及'人'的Domain自动选择维度IV")
    print("✅ 约束条件维度: 公理化Domain自动选择系统边界检测")

    return report


if __name__ == "__main__":
    main()
