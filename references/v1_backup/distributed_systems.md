# Domain: Distributed Systems
# Source: Leslie Lamport, Eric Brewer, Jim Gray, Barbara Liskov
# Structural_Primitives: consensus, consistency, partition_tolerance, replication, fault_tolerance

## Core Objects
- **Node**: 分布式系统中的独立计算单元，具有本地存储和处理能力
- **Message**: 节点间通信的载体，可能丢失、延迟或乱序到达
- **Consensus**: 多个节点对某一值达成一致的协议状态
- **Clock**: 时间测量机制，分布式系统中不存在全局统一时钟
- **Partition**: 网络故障导致节点间通信中断形成的隔离区域

## Core Morphisms
- **Replication**: 数据/状态在多个节点间复制，提高可用性和容错性
- **Consensus Protocol**: 节点间交换消息 → 达成一致决策（Paxos, Raft）
- **Transaction**: 原子性的操作序列，满足ACID或BASE特性
- **Failure Detection**: 监控节点健康状态，识别崩溃或网络分区
- **Leader Election**: 在节点中选出协调者，处理单点决策需求

## Theorems / Patterns

### 1. CAP Theorem
**内容**: 分布式系统不可能同时满足一致性(Consistency)、可用性(Availability)、分区容错性(Partition Tolerance)，最多只能同时满足其中两项

**Applicable_Structure**: 需要权衡数据一致性与系统可用性的分布式架构设计

**Mapping_Hint**: 映射到"组织集中管控vs区域自治"、"产品标准化vs本地化"、"信息同步的时效性取舍"

**Case_Study**: 分区发生时，银行系统选择CP（保证账户余额一致性，可能拒绝交易），而社交网络选择AP（保证服务可用，允许短暂数据不一致）

### 2. FLP Impossibility
**内容**: 在异步系统中（消息延迟无上界），即使只有一个进程可能故障，也不存在确定性的共识算法

**Applicable_Structure**: 需要达成共识但无法保证时限的分布式决策场景

**Mapping_Hint**: 映射到"跨部门协作的决策困境"、"多方利益协调的固有难度"、"完全共识的不可能性"

**Case_Study**: 区块链系统通过引入随机性和经济激励（而非纯算法）绕过FLP限制，实现概率性共识

### 3. Two Generals Problem
**内容**: 在不可靠信道上，两个将军无法通过有限次消息交换确保达成共识（进攻或撤退）

**Applicable_Structure**: 通信不可靠时的协调难题

**Mapping_Hint**: 映射到"远程团队协作的信任建立"、"供应链上下游的协调困境"、"跨国业务的沟通成本"

**Case_Study**: TCP三次握手只能建立大概率可信的连接，无法绝对保证双方同时准备好通信

### 4. Backpressure
**内容**: 当系统组件处理能力不足时，向上游传递压力信号，实现流量自适应调节而非崩溃

**Applicable_Structure**: 具有多级处理环节的流水线系统

**Mapping_Hint**: 映射到"供应链需求信号传递"、"组织架构的压力传导"、"产品迭代的节奏控制"

**Case_Study**: Netflix的RxJava使用背压机制，当消费者处理速度低于生产者时自动调节生产速率

### 5. Eventual Consistency
**内容**: 系统保证在没有新更新的情况下，最终所有副本将达到一致状态，允许暂时不一致

**Applicable_Structure**: 高可用优先、可容忍短暂不一致的系统

**Mapping_Hint**: 映射到"品牌全球传播的时间差"、"分公司与总部的信息同步"、"产品多版本共存的策略"

**Case_Study**: DNS系统是全球最终一致的，域名解析变更可能需要数小时才能在全球所有服务器同步

## Tags
- distributed_systems
- cap_theorem
- consensus
- replication
- fault_tolerance
- consistency
- partition
- scalability
- microservices
- byzantine_fault
