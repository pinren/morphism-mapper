# Morphism Mapper 高级模块系统

## 概述

基于高级范畴论概念（自然变换、米田引理、伴随函子、极限/余极限）的按需挂载分析模块，用于解决基础映射无法覆盖的复杂场景。

## 模块列表

| 模块文件 | 版本 | 数学概念 | 核心功能 | 强制执行 |
|----------|------|----------|----------|----------|
| `adjoint_balancer.md` | V4 | 伴随函子 | 可行性平衡 | **是** |
| `yoneda_probe.md` | V3 | 米田引理 | 信息补全 | 否 |
| `natural_transformation.md` | **V3** | 自然变换 | 视角对齐/颗粒度缩放/策略演化 | 否 |
| `limits_colimits.md` | V5 | 极限/余极限 | 元逻辑提取 | 否 |
| `kan_extension.md` | V1 | 坎扩展 (Kan Extension) | 局部成功全局复制 (激进/保守) | 否 (called by Adjoint Balancer) |
| `koan_break.md` | V1 | 初始对象 | 问题重构 | 否 |

## 触发映射速查

| 用户话术关键词 | 潜在困境 | 挂载模块 |
|----------------|----------|----------|
| "环境变了"、"风向调了" | 结构性失效 | Natural Transformation (Mode C) |
| "技术和业务打架"、"KPI不一致" | 视角冲突 | Natural Transformation (Mode A) |
| "战略宏大落地零碎"、"动作变形" | 颗粒度断裂 | Natural Transformation (Mode B) |
| "看不穿"、"查不到"、"黑盒" | 信息不对称 | Yoneda Probe |
| "太难了"、"没资源"、"怎么落地" | 复杂度超载 | Adjoint Balancer |
| "复制到XX市场"、"如何规模化"、"下沉市场" | 局部成功到全局复制 | Kan Extension |
| "这几个领域有什么共同点？" | 缺乏通用底层 | Limits/Colimits |
| "圆的方"、"万能的石头"、"无解" | 逻辑悖论/范畴错误 | Koan Break |
| 遍历所有 Domain B 均无法映射 | 结构不匹配 | Koan Break |
| 连续多次验证失败 | 问题本身需重构 | Koan Break |

## 模块接口标准

每个模块必须包含以下章节：

```markdown
---
module: [模块标识]
version: [版本号]
name: [中文名称]
description: [一句话描述]
---

## Mathematical Foundation
[数学原理及商业映射]

## Trigger
[自动触发条件 + 手动触发命令]

## Logic
[Step-by-step 执行逻辑]

## Input/Output
[输入要求 + 输出格式模板]

## Integration
[挂载点 + 与主流程的整合方式]
```

## 模块开发指南

1. 复制 `_template.md` 创建新模块
2. 遵循接口标准填写各章节
3. 在 README.md 中更新模块列表
4. 在 SKILL.md 中更新触发映射

## 模块链式调用

默认优先级：
```
yoneda_probe → natural_transformation → limits_colimits → adjoint_balancer
```

特殊情况（逻辑僵局时）：
```
koan_break → [用户重构问题后重新进入主流程]
```

## 扩展计划

- ✅ **Kan Extensions**: 域扩展保持结构 (已完成 v2.6)
- **Functor Categories**: 反事实推理
- **Higher Category Theory**: 多层结构处理
- **Koan Break Variants**: 针对不同类型悖论的专业重构模块（逻辑型、情感型、价值型）
