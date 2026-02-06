# /morphism-config 命令

## 用途
配置和扩展 Morphism Mapper，包括添加自定义领域、验证格式等。

## 子命令

### list
列出所有可用领域（内置 + 自定义）。

```
/morphism-config list
```

**输出示例**:
```
内置领域 (9):
- zhuangzi          庄子哲学（变化、尺度、相对性）
- evolutionary_biology  进化生物学（选择、适应）
- thermodynamics    热力学（能量、熵）
- network_theory    网络理论（节点、传播）
- control_systems   控制系统（反馈、调节）
- linguistics       语言学（符号、意义）
- mythology         神话学（原型、仪式）
- ecology           生态学（种群、共生）
- game_theory       博弈论（策略、均衡）

自定义领域 (0):
暂无自定义领域

添加自定义领域:
1. 复制 references/_template.md 到 references/custom/your_domain.md
2. 按模板填写内容
3. 运行 /morphism-config validate 验证格式
```

### add-domain <name>
创建新的自定义领域文件。

```
/morphism-config add-domain quantum_physics
```

此命令会：
1. 创建 references/custom/quantum_physics.md
2. 从 _template.md 复制模板内容
3. 提示用户编辑文件

### validate
验证所有自定义领域文件的格式。

```
/morphism-config validate
```

**验证内容**:
- 必需的 frontmatter 字段（Domain, Source, Structural_Primitives）
- Core Objects 部分是否存在
- Core Morphisms 部分是否存在
- Theorems 部分是否存在且格式正确
- Tags 部分是否存在

**输出示例**:
```
验证结果:
✓ custom/quantum_physics.md - 格式正确
✗ custom/my_domain.md - 缺少 Core Morphisms 部分

修复建议:
- 在 my_domain.md 中添加 ## Core Morphisms 章节
- 参考 _template.md 的格式
```

## 自定义领域最佳实践

1. **选择硬核领域**: 优先选择有深厚理论基础的领域
2. **结构清晰**: 严格遵循模板格式
3. **定理具体**: 每个定理都要有 Applicable_Structure 和 Mapping_Hint
4. **标签准确**: Tags 帮助系统匹配最合适的 Domain B
5. **案例丰富**: 提供领域内的经典案例，帮助理解定理

## 文件位置

- 内置领域: `references/*.md`
- 自定义领域: `references/custom/*.md`
- 模板: `references/_template.md`

自定义领域会覆盖同名的内置领域（如果存在）。
