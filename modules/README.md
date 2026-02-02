# Morphism Mapper 高级模块系统

## 概述

基于高级范畴论概念（自然变换、米田引理、伴随函子、极限/余极限）的按需挂载分析模块，用于解决基础映射无法覆盖的复杂场景。

## 模块列表

| 模块文件 | 版本 | 数学概念 | 核心功能 | 强制执行 |
|----------|------|----------|----------|----------|
| `adjoint_balancer.md` | V4 | 伴随函子 | 可行性平衡 | **是** |
| `yoneda_probe.md` | V3 | 米田引理 | 信息补全 | 否 |
| `natural_transformation.md` | V2 | 自然变换 | 策略演化 | 否 |
| `limits_colimits.md` | V5 | 极限/余极限 | 元逻辑提取 | 否 |

## 触发映射速查

| 用户话术关键词 | 潜在困境 | 挂载模块 |
|----------------|----------|----------|
| "环境变了"、"风向调了" | 结构性失效 | Natural Transformation |
| "看不穿"、"查不到"、"黑盒" | 信息不对称 | Yoneda Probe |
| "太难了"、"没资源"、"怎么落地" | 复杂度超载 | Adjoint Balancer |
| "这几个领域有什么共同点？" | 缺乏通用底层 | Limits/Colimits |

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

## 扩展计划

- **Kan Extensions**: 域扩展保持结构
- **Functor Categories**: 反事实推理
- **Higher Category Theory**: 多层结构处理
