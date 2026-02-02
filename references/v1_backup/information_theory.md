# Domain: Information Theory
# Source: Claude Shannon, Warren Weaver, Leon Brillouin
# Structural_Primitives: entropy, channel_capacity, noise, redundancy, compression

## Core Objects
- **Information Source**: 产生消息或符号序列的源头，具有特定的概率分布
- **Channel**: 传输信息的媒介，具有有限的带宽和特定的噪声特性
- **Receiver**: 解码接收到的信号并还原消息的终端
- **Entropy (H)**: 信息源的不确定性度量，H = -Σp(x)log₂p(x)，单位比特
- **Code**: 将消息映射为可传输符号的编码系统

## Core Morphisms
- **Encoding**: 消息 → 信号，增加冗余以对抗噪声
- **Transmission**: 信号通过信道，可能受到噪声干扰
- **Decoding**: 接收信号 → 还原消息，利用冗余纠错
- **Compression**: 消除统计冗余，降低传输成本
- **Encryption**: 信息变换为只有授权方可解读的形式

## Theorems / Patterns

### 1. Shannon's Source Coding Theorem
**内容**: 无损压缩的极限是信息熵，不可能将数据压缩到熵以下而不丢失信息

**Applicable_Structure**: 任何需要精简表达而保留核心含义的场景

**Mapping_Hint**: 映射到"品牌核心信息提炼"、" elevator pitch 设计"、"产品功能精简"

**Case_Study**: ZIP压缩算法利用统计冗余，通常将文本文件压缩至原大小的30-40%

### 2. Shannon's Channel Capacity Theorem
**内容**: 信道容量C = B·log₂(1+S/N)，带宽和信噪比决定最大无误传输速率

**Applicable_Structure**: 信息传递系统的设计与优化

**Mapping_Hint**: 映射到"营销渠道容量规划"、"组织沟通带宽优化"、"知识管理效率"

**Case_Study**: 4G LTE通过MIMO技术增加等效带宽，配合编码增益实现高速数据传输

### 3. The Data Processing Inequality
**内容**: 对数据进行处理不会增加关于源的信息量，X→Y→Z形成马尔可夫链则I(X;Y)≥I(X;Z)

**Applicable_Structure**: 信息在传递和处理过程中的必然损耗

**Mapping_Hint**: 映射到"中层管理导致的信息过滤"、"市场研究数据的失真累积"、"直接沟通的价值"

**Case_Study**: 企业层级结构中，CEO的意图经过多层传递后严重失真

### 4. Rate-Distortion Theory
**内容**: 允许一定失真D时，压缩率可低于熵，R(D)给出最优权衡曲线

**Applicable_Structure**: 需要在信息保真度和效率之间取舍的场景

**Mapping_Hint**: 映射到"产品简化与功能保留的权衡"、"报告摘要的失真容忍度"、"快速原型vs精细设计"

**Case_Study**: MP3音频压缩利用人耳听觉掩蔽效应，在可接受的音质损失下实现10:1压缩比

### 5. Mutual Information
**内容**: I(X;Y) = H(X) - H(X|Y)，表示Y关于X的信息量，即知道Y后X不确定性的减少

**Applicable_Structure**: 衡量两个变量之间的依赖关系强度

**Mapping_Hint**: 映射到"客户行为数据的价值评估"、"供应链可见性的ROI"、"市场调研的信息增益"

**Case_Study**: 推荐系统通过最大化用户-物品交互的互信息提升推荐准确度

## Tags
- information
- entropy
- channel
- noise
- compression
- bandwidth
- communication
- coding
- redundancy
- mutual_information
