# Agent Team 实施指南 v3.0

**更新日期**: 2026-02-08
**版本**: v3.0 (共识信号引导的涌现式 Swarm + Phase 4.1 结构摩擦层)
**状态**: ✅ 架构已纠正

---

## ⚠️ 重要架构纠正

### 错误理解 (v1.0 - 已废弃)
```
用户 → Leader → Task tool → 创建固定 teammates → 收集结果 → 合成
```
**问题**: 基于错误的 Agent Teams 理解（以为需要程序化 Task tool 调用）

### 正确理解 (v3.0 - 当前版本)
```
用户 → Leader → 初始 Team (2-3 核心)
                      ↓
                  并行分析中...
                      ↓
              ┌───────┴───────┐
              ↓               ↓
          同构检测        Dissensus 检测
              ↓               ↓
      【发现共识信号】    【发现分歧】
              ↓               ↓
    ┌─────────┴─────────┐     ↓
    ↓                   ↓     ↓
释放共识信号        引导方向   触发冲突分析
    ↓                   ↓     ↓
吸引子形成        涌现探索    寻找调和
    ↓                   ↓     ↓
深入该方向      引入验证领域   引入调解视角
```

**核心差异**:
- **激活方式**: 自然语言请求（非程序化 Task tool 调用）
- **扩展触发**: 同构检测释放共识信号（非简单发现缺口）
- **引导机制**: 共识信号自动引导探索方向
- **幻觉防护**: Phase 4.1 结构摩擦层（四道防线）

---

## 环境配置

```bash
# 启用 Agent Teams 功能
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

---

## 核心架构

### 共识信号引导的涌现式 Swarm

```
┌─────────────────────────────────────────────────────────────────┐
│                    Agent Team Lead (Leader)                      │
│              SKILL_LEADER.md - 共识信号检测与引导                 │
├─────────────────────────────────────────────────────────────────┤
│  Phase 0: 用户画像构建                                          │
│  Phase 1: 范畴骨架提取                                          │
│  Phase 2: 领域选择 (domain_selector.py)                          │
│  Phase 2.5: 共识信号引导的涌现探索 ⭐ NEW                       │
│    - 实时同构检测                                                │
│    - 共识信号释放                                              │
│    - 引导方向探索                                                │
│  Phase 4: Synthesis (含 Phase 4.1 结构摩擦层) ⭐ NEW            │
│    - Blind Signature Collection                                 │
│    - Kernel Loss Protocol                                      │
│    - Obstruction Theorist Review                               │
│    - Round-Trip Check (按需)                                    │
│  Phase 5: 报告生成                                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 文件结构

```
morphism-mapper/
├── SKILL.md                    # 主 skill 文件 (已更新 v3.0)
├── SKILL_LEADER.md              # ⭐ NEW: Leader 指南
├── SKILL_SYNTHESIZER.md         # ⭐ NEW: Synthesizer 指南
├── agents/
│   ├── templates/
│   │   └── domain_agent_prompt.md   # Domain Agent 模板 (含 kernel_loss)
│   ├── config/                      # 配置文件
│   │   ├── domain_agents.json       # 领域元数据
│   │   ├── swarm_protocol.json      # Swarm 协议
│   │   └── agent_strategy.json      # Agent 策略
│   ├── personas/                    # Persona 文件
│   │   ├── obstruction_theorist.md  # ⭐ NEW: 职业反对派
│   │   └── [domain]_persona.md      # Full Agent personas
│   └── system_prompts/               # 系统 prompts
│       ├── broadcaster.md
│       ├── synthesizer.md
│       └── domain_template.md
├── scripts/
│   ├── helpers.py                  # 集成辅助函数
│   ├── domain_selector.py          # 领域选择 (保留)
│   └── modules/                    # 核心模块
│       ├── homography_detector.py  # 同构检测 (保留)
│       └── cluster_detector.py     # 簇检测 (保留)
├── docs/
│   ├── DOMAIN_AGENT_GUIDE.md       # ⭐ NEW: Teammate 角色指南
│   ├── AGENT_TEAM_IMPLEMENTATION_GUIDE.md  # 本文档
│   └── AGENT_TEAM_SUMMARY.md
├── references/                    # 领域知识库 (V2 格式)
└── knowledge/
    └── exploration_history/        # 探索报告
```

---

## 使用方法

### 自然语言激活

用户直接描述问题，系统自动触发 Swarm Mode：

```
用户: "婆媳矛盾怎么破"
→ 自动触发 swarm 模式
→ 启动 Agent Team Leader
→ 执行完整流程
```

### Leader 工作流程

1. **Phase 0-1**: 提取用户画像和范畴骨架
2. **Phase 2**: 调用 `domain_selector.py` 获取推荐领域
3. **Phase 2.5**: 创建初始 Team (2-3 核心领域)，开始涌现探索
4. **Phase 4**: 调用 Synthesizer 进行合成（含 Phase 4.1 验证）

### 辅助函数调用

```python
from scripts.helpers import (
    call_domain_selector,
    load_domain_agent_results,
    load_all_domain_results,
    create_exploration_report,
    apply_tier_balance,
    select_wildcard_domain
)

# Phase 2: 领域选择
selector_result = call_domain_selector(
    objects=O_a,
    morphisms=M_a,
    user_profile=user_profile,
    top_k=5
)

# Phase 2.5: Tier Balance + Wildcard
selected = apply_tier_balance(selector_result["top_domains"])
wildcard = select_wildcard_domain(selected)

# Phase 4: 加载结果
domain_results = load_all_domain_results(selected + [wildcard])
```

---

## 关键机制

### 共识信号引导 (Phase 2.5)

**核心思想**: 通过同构检测释放共识信号，引导探索方向

| 共识信号类型 | 检测方式 | 释放的信息 | 引导行动 |
|------------|---------|-----------|---------|
| **强同构** | ≥3 个领域使用相似结构 | "这里有大方向" | 深化方向，引入验证领域 |
| **弱同构** | 2 个领域有相似视角 | "可能有关联" | 引入第 3 个领域验证 |
| **概念对立** | 不同领域使用对立概念 | "存在张力" | 引入辩证领域 |
| **高 Dissensus** | 分歧度 >60 | "需要调和" | 引入调解领域 |

### Phase 4.1: 结构摩擦层

**四道防线**:

1. **Blind Signature Collection**: 防止互相抄作业
2. **Initial Mapping Collection**: 强制检查 kernel_loss
3. **Obstruction Theorist Review**: 职业反对派审查
4. **Round-Trip Check** (按需): 语义漂移检测

**设计哲学**: 从"寻求共识"转向"压力测试"

---

## 与原 Python 代码的对比

| 功能 | 原 Python 实现 | Agent Team 实现 (v3.0) |
|------|---------------|---------------------|
| 主控逻辑 | `SwarmOrchestrator.run_swarm_exploration()` | Leader 自然语言协调 |
| 领域选择 | `domain_selector.py` | 保留，通过 `helpers.call_domain_selector()` 调用 |
| Domain Agent | Mock 数据 | 真实 LLM teammate (自然语言激活) |
| 扩展触发 | 一次性全部 | **共识信号自动引导** ⭐ |
| 同构检测 | 合成时使用 | **实时分析引导探索** ⭐ |
| Limit/Colimit | Mock 计算 | Synthesizer (含 Phase 4.1) |
| 幻觉防护 | 无 | **四道结构摩擦防线** ⭐ |
| 报告生成 | `save_exploration_report()` | `helpers.create_exploration_report()` |

**保留的 Python 模块**:
- `domain_selector.py`: 领域选择逻辑
- `modules/homography_detector.py`: 同构检测（增强用于实时分析）
- `modules/cluster_detector.py`: 簇检测（用于合成）

**不再需要的模块**:
- `swarm_orchestrator.py`: 被 Leader 的自然语言协调替代
- `dynamic_agent_generator.py`: Teammates 自然理解任务

---

## 质量保证

### Phase 4.1: 核损耗协议 (Kernel Loss Protocol)

所有 Domain Agent 输出必须包含 `kernel_loss` 字段：

```json
{
  "kernel_loss": {
    "lost_nuances": [
      {
        "element": "丢失的元素",
        "description": "详细说明",
        "severity": "HIGH | MEDIUM | LOW"
      }
    ],
    "preservation_score": 0.75
  }
}
```

**验证规则**:
- 如果 `kernel_loss` 为空或 "None" → 直接丢弃结果
- HIGH 级别丢失 → preservation_score 必须 ≤ 0.7

### Trivial Limit 检测

Synthesizer 必须拒绝空泛的 Limit：

```python
TRIVIAL_INDICATORS = [
    "需要平衡",
    "应该重视",
    "必须关注",
    "要注意",
    "要关注"
]
```

### Verification Proof

所有 Domain Agent 输出必须包含双点验证：

```json
{
  "verification": {
    "if_then_logic": "如果...那么...",
    "examples": ["案例1", "案例2"]
  }
}
```

---

## 指南文档

| 文档 | 用途 | 目标读者 |
|------|------|---------|
| `SKILL_LEADER.md` | Leader 共识信号检测与引导指南 | Team Lead |
| `SKILL_SYNTHESIZER.md` | Synthesizer 合成与 Phase 4.1 指南 | Synthesizer |
| `docs/DOMAIN_AGENT_GUIDE.md` | Domain Agent 角色指南 | Teammates |
| `agents/templates/domain_agent_prompt.md` | Domain Agent 输出模板 | Teammates |
| `agents/personas/obstruction_theorist.md` | 职业反对派 persona | Obstruction Theorist |

---

## 调试技巧

### 查看临时文件

```bash
# 查看 Domain Agent 结果
ls -la /tmp/morphism_swarm/results/

# 查看单个领域结果
cat /tmp/morphism_swarm/results/thermodynamics.json
```

### 测试单个组件

```bash
# 测试 domain_selector
python scripts/helpers.py domain-selector --input /tmp/test_morphism_input.json

# 测试 tier balance
python scripts/helpers.py tier-balance --domains "thermodynamics,game_theory"

# 测试 wildcard 选择
python scripts/helpers.py wildcard --seeded "thermodynamics,game_theory"
```

### 完整流程测试

```bash
# 使用测试问题 "婆媳矛盾怎么破"
# 检查输出报告
cat knowledge/exploration_history/$(date +%Y%m%d)-exploration.md
```

---

## 常见问题

### Q1: Agent Team 如何协调 Teammates？

**A**: 通过自然语言请求，而非程序化调用：

```
Leader: "请创建新 teammate:
领域: thermodynamics
任务: 从热力学视角分析用户问题
输入: 用户问题 + 范畴骨架"
```

### Q2: 如何处理 Domain Agent 超时？

**A**: 设置资源边界：

```python
# Teammate 数量上限: 5-8 个
# 循环轮次上限: 3-4 轮
# 超时后强制进入合成阶段
```

### Q3: 如何确保 Domain Agent 返回正确的 JSON 格式？

**A**: 在 `domain_agent_prompt.md` 中明确指定格式并提供完整示例

---

## 版本兼容性

| 版本 | 特性 | 状态 |
|------|------|------|
| v3.0 | 共识信号引导涌现 + Phase 4.1 | **当前版本** |
| v4.0 | Swarm Mode (基于 v3.0) | 当前版本 |
| v2.5 | 领域管理 | 保留兼容 |
| v1.0 | 错误的 Task tool 调用理解 | ❌ 已废弃 |

---

## 核心差异总结

| 方面 | v1.0 (错误) | v3.0 (正确) |
|------|-----------|-----------|
| 激活方式 | Task tool 程序化调用 | 自然语言请求 |
| 团队构成 | 预先固定 5-6 个 | **信号引导动态引入** |
| 扩展触发 | 一次性全部 | **同构检测释放信号** |
| 引导机制 | 无 | **共识信号自动引导** |
| 结果收集 | 文件 I/O 手动聚合 | Teammates 自动报告 |
| 幻觉防护 | 无 | **四道结构摩擦防线** ⭐ |
| 探索性质 | 并行独立 | **涌现式自组织** |

---

## 下一步

1. **测试完整流程**: 使用 "婆媳矛盾怎么破" 测试
2. **验证 Phase 4.1**: 确认四道防线正常工作
3. **文档完善**: 补充更多示例
4. **性能优化**: 根据实际使用情况优化

---

## 联系方式

如有问题，请查看:
- `SKILL_LEADER.md` - Leader 完整指南
- `SKILL_SYNTHESIZER.md` - Synthesizer 完整指南
- `docs/DOMAIN_AGENT_GUIDE.md` - Teammate 角色指南
- `agents/personas/obstruction_theorist.md` - 职业反对派定义

---

**创建时间**: 2026-02-08
**最后更新**: 2026-02-08
**版本**: v3.0 (架构已纠正)
