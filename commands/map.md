# /morphism-map 命令

## 用途
执行从 Domain A 到指定 Domain B 的函子映射。

## 用法
```
/morphism-map <domain_name>
```

## 参数
- `domain_name`: 目标领域名称，对应 references/ 下的文件名（不含 .md）

## 可用领域
- `zhuangzi` - 庄子哲学
- `evolutionary_biology` - 进化生物学
- `thermodynamics` - 热力学
- `network_theory` - 网络理论
- `control_systems` - 控制系统
- `linguistics` - 语言学/符号学
- `mythology` - 神话学/原型
- `ecology` - 生态学
- `game_theory` - 博弈论

## 示例
```
/morphism-map ecology
```

## 输出格式
```markdown
### 【映射矩阵】Domain A → Domain B (ecology)

| Domain A | 映射关系 | Domain B | 同构性验证 |
|----------|----------|----------|------------|
| 用户 | ≅ | 种群 | 都是系统的基本单元，有增长/流失动态 |
| 竞品 | ≅ | 竞争者/捕食者 | 争夺相同资源的异种生物 |
| 市场 | ≅ | 生态系统 | 包含多种相互作用的实体 |
| 使用 | → | 定植/栖息 | 在特定环境中建立存在 |
| 流失 | → | 迁移/死亡 | 离开当前栖息地 |
| 抢夺 | → | 竞争/捕食 | 争夺有限资源的行为 |
| 注意力有限 | → | 承载力 | 环境支持能力的上限 |
| 转换成本 | → | 迁移成本 | 改变栖息地的能量代价 |

**结构同构性**: 用户留存问题与种群生态具有高度结构相似性
- 都是开放系统，与外部环境有物质/能量/信息交换
- 都存在竞争和选择压力
- 都有承载力限制
```

## 执行步骤

1. 读取指定 Domain B 的 references 文件
2. 建立 Objects 的对应关系
3. 建立 Morphisms 的对应关系
4. 验证结构同构性
5. 识别适用的 Theorems

## 注意事项
- 映射必须基于结构而非表面相似
- 每个映射都需要同构性验证
- 如果结构不匹配，应提示用户选择其他 Domain B
