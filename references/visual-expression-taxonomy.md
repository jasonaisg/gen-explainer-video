# 科普视频视觉表达 Taxonomy

> 版本：0.1-draft  
> 状态：供讨论  
> 范围：科普类、知识类、解释类视频的视觉表达词典

## 1. 文档定位

本词典用于统一描述科普视频中的视觉表达，使同一类信息意图、视觉结构、画面组织、素材形态、画面容器、运动方式、视觉风格和运动气质具有稳定、可复用的名称。

本词典只回答三个问题：

1. 这个词条是什么；
2. 它适合表达什么；
3. 它与相近词条有什么区别。

本词典不规定具体视频如何切割，不包含数据处理步骤、选择算法、渲染代码、时长、坐标、颜色、字体或缓动参数。

## 2. 八个表达维度

| 维度 | 回答的问题 | ID 前缀 |
|---|---|---|
| 信息意图 | 为什么需要视觉化 | `intent.` |
| 视觉结构 | 信息之间是什么关系 | `structure.` |
| 画面组织 | 整个镜头如何布局 | `composition.` |
| 素材形态 | 用什么视觉对象表达 | `medium.` |
| 画面容器 | 信息被放在什么组件中 | `container.` |
| 运动方式 | 元素如何出现、变化和离开 | `motion.` |
| 视觉风格 | 画面采用什么美术语言 | `style.` |
| 运动气质 | 动起来给人什么感受 | `character.` |

词条 ID 使用英文小写命名空间。一个镜头可以同时使用多个词条，但应区分主要词条与辅助词条。

---

# 一、信息意图 Information Intent

信息意图描述“观众需要通过视觉更容易理解什么”，它是后续视觉选择的起点。

| ID | 中文名称 | 定义 | 典型内容 |
|---|---|---|---|
| `intent.key_point` | 核心观点 | 建立一个必须被记住的主要结论 | 核心判断、中心命题、段落结论 |
| `intent.emphasis` | 重点强调 | 提高某个词、数字或对象的注意优先级 | 关键词、关键数字、特别提醒 |
| `intent.definition` | 概念定义 | 说明一个术语、对象或概念是什么 | 名词解释、缩写展开、概念边界 |
| `intent.explanation` | 原理解释 | 解释某种现象、规则或机制为何成立 | 科学原理、工作原理、制度逻辑 |
| `intent.enumeration` | 并列列举 | 呈现若干地位相近的项目 | 三个特点、五种方法、多个因素 |
| `intent.classification` | 分类归纳 | 按共同属性将对象分组 | 类型划分、物种分类、用户分群 |
| `intent.comparison` | 对照比较 | 显示两个或多个对象的相同与不同 | A/B比较、方案比较、优缺点 |
| `intent.before_after` | 前后变化 | 比较同一对象在变化前后的状态 | 改造前后、治疗前后、政策前后 |
| `intent.sequence` | 先后顺序 | 说明离散事项的排列顺序 | 第一步到第三步、操作次序 |
| `intent.process` | 过程推进 | 说明事物如何从输入走向结果 | 工作流程、生产流程、审批流程 |
| `intent.branching` | 条件分支 | 说明不同条件会通向不同路径 | 如果……那么……、决策选择 |
| `intent.cycle` | 循环往复 | 说明过程会回到起点并重复 | 水循环、生命周期、反馈循环 |
| `intent.time_change` | 时间变化 | 说明事物如何随时间演变 | 历史变化、技术迭代、价格走势 |
| `intent.milestone` | 关键节点 | 强调时间过程中的重要事件 | 发明年份、项目里程碑、人生节点 |
| `intent.duration` | 持续时间 | 比较事件开始、结束与持续长度 | 项目工期、生命周期、并行任务 |
| `intent.cause_effect` | 因果关系 | 说明原因如何导致结果 | 诱因与后果、机制链条 |
| `intent.condition_result` | 条件与结果 | 说明结果成立所依赖的条件 | 触发条件、适用条件、边界条件 |
| `intent.feedback` | 反馈关系 | 说明结果如何反过来影响系统 | 正反馈、负反馈、闭环调节 |
| `intent.hierarchy` | 层级关系 | 说明上下级、包含或从属关系 | 组织结构、概念层级、权限层级 |
| `intent.part_whole` | 整体与部分 | 说明整体由哪些部分构成 | 人体系统、预算构成、产品组件 |
| `intent.relationship` | 关联关系 | 说明多个对象如何彼此连接 | 人际网络、知识图谱、生态关系 |
| `intent.flow` | 流动迁移 | 说明数量、资源或对象从哪里流向哪里 | 资金流、信息流、人口迁移 |
| `intent.location` | 空间位置 | 说明对象在哪里或如何分布 | 地理位置、器官位置、场地布局 |
| `intent.route` | 路径路线 | 说明对象如何穿过空间到达目的地 | 航线、传播路线、神经路径 |
| `intent.magnitude` | 数量规模 | 说明数值有多大或对象有多少 | 人数、金额、距离、体积 |
| `intent.proportion` | 比例构成 | 说明部分占整体的份额 | 百分比、市场份额、成分比例 |
| `intent.trend` | 趋势变化 | 说明数值上升、下降或波动趋势 | 增长曲线、温度变化、长期趋势 |
| `intent.ranking` | 排名顺序 | 说明对象在有序列表中的位置 | 排行榜、优先级、名次变化 |
| `intent.deviation` | 偏差基准 | 说明数值相对基准、目标或平均值的差异 | 超标、低于目标、正负偏差 |
| `intent.distribution` | 分布形态 | 说明数据如何集中、离散或偏斜 | 年龄分布、成绩分布、概率分布 |
| `intent.correlation` | 相关关系 | 说明两个或多个变量是否共同变化 | 收入与寿命、温度与能耗 |
| `intent.uncertainty` | 不确定性 | 表达概率、范围、预测或未知程度 | 预测区间、风险概率、多个情景 |
| `intent.mechanism` | 内部机制 | 说明物体或系统内部如何运作 | 发动机、细胞、算法内部机制 |
| `intent.transformation` | 状态转化 | 说明对象从一种形态变为另一种形态 | 相变、化学反应、能量转化 |
| `intent.scale` | 尺度关系 | 说明宏观、微观或不同数量级之间的关系 | 宇宙到地球、人体到细胞 |
| `intent.instruction` | 操作指导 | 告诉观众应该怎样做 | 安装步骤、使用方法、安全操作 |
| `intent.evidence` | 证据支持 | 用事实、数据或来源支撑一个判断 | 研究结果、文献、实验、原始记录 |
| `intent.reasoning` | 推理证明 | 展示从前提到结论的思考链条 | 论证、公式推导、排除过程 |
| `intent.misconception` | 误区纠正 | 对照常见误解与正确理解 | 谣言与事实、错误答案解析 |
| `intent.problem_solution` | 问题与方案 | 先呈现问题，再说明解决方式 | 痛点、诊断、改进方案 |
| `intent.scenario` | 情境案例 | 通过具体人物或事件帮助理解抽象内容 | 用户案例、生活情境、实验故事 |
| `intent.warning` | 风险警示 | 强调危险、限制、禁止或异常 | 安全警告、错误后果、红线条件 |
| `intent.summary` | 总结回顾 | 将前文信息压缩成可记忆的整体 | 本章总结、三点回顾、结论清单 |

---

# 二、视觉结构 Visual Structure

视觉结构描述信息关系在画面中的基本组织模型。它不规定具体美术风格，也不等同于画面容器。

## 2.1 观点、列表与分类

| ID | 中文名称 | 定义 | 适合表达 |
|---|---|---|---|
| `structure.single_focus` | 单中心结构 | 全画面围绕一个主要对象或结论 | 核心观点、关键数字、单一概念 |
| `structure.annotated_statement` | 注释式观点 | 主句周围附带解释、证据或标注 | 结论解释、术语拆解 |
| `structure.list.bullet` | 项目列表 | 使用项目符号排列并列信息 | 无先后关系的列举 |
| `structure.list.numbered` | 编号列表 | 使用数字表示项目次序 | 有顺序或优先级的列举 |
| `structure.list.checklist` | 检查清单 | 使用选框或勾选状态呈现项目 | 条件核对、完成状态 |
| `structure.list.icon` | 图标列表 | 每个项目由图标与短文字组成 | 特征、类别、简短要点 |
| `structure.classification.grouped` | 分组分类 | 将项目放入若干明确分组 | 类别划分、归纳总结 |
| `structure.classification.cluster` | 聚类分布 | 通过空间聚集表达相似性 | 自然分群、概念聚类 |
| `structure.classification.matrix` | 分类矩阵 | 使用行列两个维度同时分类 | 双条件分类、产品矩阵 |
| `structure.classification.quadrant` | 四象限 | 用两个坐标维度划分四个区域 | 风险收益、重要紧急 |
| `structure.classification.venn` | 维恩图 | 用重叠区域表达集合交集 | 共同点、交集、独有属性 |

## 2.2 比较与差异

| ID | 中文名称 | 定义 | 适合表达 |
|---|---|---|---|
| `structure.compare.split` | 左右对照 | 将两个对象并列放置形成直接比较 | A/B、旧/新、正/反 |
| `structure.compare.table` | 对比表 | 用统一行列比较多个对象与指标 | 参数、功能、方案比较 |
| `structure.compare.pros_cons` | 优缺点结构 | 将正面与负面信息成对呈现 | 利弊、机会风险 |
| `structure.compare.before_after` | 前后对照 | 对照同一对象两个时间状态 | 改造、变化、效果 |
| `structure.compare.balance` | 平衡结构 | 用天平或中心基准表达两方权衡 | 权衡、平衡、代价收益 |
| `structure.compare.overlay` | 重叠对照 | 将两个状态透明叠加以显示差异 | 轮廓变化、位置偏移 |
| `structure.compare.difference_map` | 差异标注图 | 在对象上直接标注变化区域 | 产品迭代、结构差异 |
| `structure.compare.small_multiples` | 小倍图 | 使用相同尺度的小图并列比较 | 多对象、多时间点比较 |

## 2.3 顺序、过程与决策

| ID | 中文名称 | 定义 | 适合表达 |
|---|---|---|---|
| `structure.process.step_sequence` | 步骤序列 | 将离散步骤按顺序排列 | 操作步骤、方法说明 |
| `structure.process.linear_flow` | 线性流程 | 使用节点和箭头表示单一路径 | 简单业务流程、生产流程 |
| `structure.process.branching_flow` | 分支流程 | 流程在条件节点分成多条路径 | 条件判断、异常处理 |
| `structure.process.swimlane` | 泳道流程 | 按角色或系统划分并行流程 | 跨部门、多人协作 |
| `structure.process.pipeline` | 管线结构 | 输入经过多个处理阶段形成输出 | 数据处理、生产加工 |
| `structure.process.funnel` | 漏斗结构 | 项目逐层筛选并减少 | 转化、过滤、淘汰 |
| `structure.process.conveyor` | 传送带结构 | 对象在连续工位间移动 | 制造、加工、自动化 |
| `structure.process.staircase` | 阶梯结构 | 用逐级上升表达能力或阶段提升 | 成长路径、成熟度 |
| `structure.process.roadmap` | 路线图 | 展示未来阶段、目标与方向 | 规划、发展路径 |
| `structure.process.decision_tree` | 决策树 | 通过问题与选项逐层得到结果 | 诊断、选择、分类判断 |
| `structure.process.state_machine` | 状态机 | 展示有限状态及状态间转换条件 | 系统状态、生命周期 |
| `structure.process.input_output` | 输入—处理—输出 | 将系统抽象为输入、处理和结果 | 算法、机器、组织运作 |

## 2.4 循环、反馈与因果

| ID | 中文名称 | 定义 | 适合表达 |
|---|---|---|---|
| `structure.cycle.circular` | 环形循环 | 多个阶段首尾相接形成闭环 | 生命周期、周期过程 |
| `structure.cycle.feedback_loop` | 反馈回路 | 结果返回并影响前序环节 | 正反馈、负反馈 |
| `structure.cycle.flywheel` | 飞轮结构 | 循环因素彼此增强并形成持续动力 | 增长飞轮、自强化机制 |
| `structure.cause.chain` | 因果链 | 原因按顺序引发一系列结果 | 连锁影响、机制路径 |
| `structure.cause.domino` | 骨牌结构 | 用连续触发隐喻因果传导 | 连锁反应、系统风险 |
| `structure.cause.fishbone` | 鱼骨图 | 从多个类别分析一个结果的原因 | 根因分析、问题诊断 |
| `structure.cause.causal_loop` | 因果回路 | 多个变量形成相互影响的闭环 | 系统动力学、复杂因果 |
| `structure.cause.argument_map` | 论证图 | 连接主张、理由、证据与反驳 | 逻辑论证、观点分析 |

## 2.5 时间与持续期

| ID | 中文名称 | 定义 | 适合表达 |
|---|---|---|---|
| `structure.timeline.horizontal` | 横向时间线 | 沿水平方向排列时间事件 | 少量历史事件、宽屏画面 |
| `structure.timeline.vertical` | 纵向时间线 | 沿垂直方向排列时间事件 | 事件较多、长标签 |
| `structure.timeline.milestone` | 里程碑时间线 | 只保留最关键的时间节点 | 发展史、关键突破 |
| `structure.timeline.period_band` | 时期区间带 | 用长度表达阶段起止与持续时间 | 朝代、生命周期、项目阶段 |
| `structure.timeline.parallel` | 并行时间线 | 同时展示多条时间进程 | 多国历史、多个项目 |
| `structure.timeline.calendar` | 日历结构 | 按日、周、月的自然周期组织事件 | 习惯、排期、季节规律 |
| `structure.timeline.gantt` | 甘特图 | 用任务条表示起止、持续与并行关系 | 项目计划、工期依赖 |
| `structure.timeline.clock` | 时钟结构 | 将事件映射到一天或一个周期 | 作息、昼夜变化 |

## 2.6 层级、整体与部分

| ID | 中文名称 | 定义 | 适合表达 |
|---|---|---|---|
| `structure.hierarchy.tree` | 层级树 | 从根节点逐层展开子节点 | 分类体系、组织结构 |
| `structure.hierarchy.pyramid` | 金字塔 | 用上下位置表达层级、基础或稀缺程度 | 需求层次、能力等级 |
| `structure.hierarchy.nested_boxes` | 嵌套框 | 用外框包含内框表达隶属关系 | 系统边界、集合包含 |
| `structure.hierarchy.concentric` | 同心层级 | 用中心到外围表达重要性或距离 | 核心与外围、影响范围 |
| `structure.part_whole.stacked` | 堆叠构成 | 将整体拆分成上下或左右堆叠部分 | 构成比例、层级材料 |
| `structure.part_whole.donut` | 环形构成 | 用圆环扇区表达少量部分占比 | 简单比例、完成度 |
| `structure.part_whole.treemap` | 矩形树图 | 用嵌套矩形面积表达层级占比 | 多层级构成、大量项目 |
| `structure.part_whole.sunburst` | 旭日图 | 用同心环表达层级与占比 | 多层分类构成 |
| `structure.part_whole.layers` | 分层结构 | 将对象表示为多个连续层 | 地层、皮肤、系统架构 |
| `structure.part_whole.exploded` | 爆炸分解结构 | 将零件沿空间分离并保留组装关系 | 机械、产品、器官结构 |

## 2.7 关系、网络与流动

| ID | 中文名称 | 定义 | 适合表达 |
|---|---|---|---|
| `structure.relation.hub_spoke` | 中心辐射 | 一个中心对象连接多个外围对象 | 核心能力、平台生态 |
| `structure.relation.node_link` | 节点连线 | 用节点和边表达一般关系 | 依赖、引用、关系网络 |
| `structure.relation.network` | 复杂网络 | 多个节点之间存在多对多连接 | 社交、交通、神经网络 |
| `structure.relation.ecosystem` | 生态关系图 | 展示角色、环境和资源的相互作用 | 行业生态、自然生态 |
| `structure.relation.concept_map` | 概念图 | 用带语义的连线组织概念 | 知识体系、概念解释 |
| `structure.relation.mind_map` | 思维导图 | 从中心主题向外发散分支 | 头脑风暴、内容总览 |
| `structure.flow.sankey` | 桑基图 | 用带宽表达流量从来源到去向的变化 | 能量、资金、用户流向 |
| `structure.flow.alluvial` | 冲积图 | 展示类别成员在多个阶段间的迁移 | 人群变化、状态迁移 |
| `structure.flow.chord` | 弦图 | 用圆周节点和内部连接表达双向关系 | 地区往来、互相流动 |
| `structure.flow.route` | 路径流动图 | 沿明确路径表达对象移动 | 运输、传播、数据包 |
| `structure.flow.stream` | 河流结构 | 用连续流带表达随时间变化的组成 | 主题演变、流量变化 |

## 2.8 数量、趋势与统计关系

| ID | 中文名称 | 定义 | 适合表达 |
|---|---|---|---|
| `structure.data.kpi` | 关键数字 | 以单个数字及单位作为视觉主体 | 总量、比例、关键指标 |
| `structure.data.counter` | 计数器 | 以可递增或递减的数值表达变化 | 实时数量、累计值 |
| `structure.data.progress_bar` | 进度条 | 用线性填充表达完成比例 | 完成度、目标进度 |
| `structure.data.progress_ring` | 进度环 | 用圆环填充表达单一比例 | 百分比、达成率 |
| `structure.data.gauge` | 仪表盘 | 用指针或弧度表达数值区间 | 速度、风险、健康度 |
| `structure.data.pictogram` | 象形图 | 用重复图标的数量表达整数或比例 | 人数、占比、直观规模 |
| `structure.data.bar` | 条形图 | 用水平长度比较类别数值 | 排名、长类别名称 |
| `structure.data.column` | 柱状图 | 用垂直高度比较类别或时间数值 | 类别比较、离散时间 |
| `structure.data.line` | 折线图 | 用连续线条表达随时间或顺序变化 | 趋势、波动 |
| `structure.data.area` | 面积图 | 用线下填充强调趋势与总量 | 总量变化、累积趋势 |
| `structure.data.slope` | 斜率图 | 连接两个时间点显示方向和幅度 | 前后排名、两期变化 |
| `structure.data.waterfall` | 瀑布图 | 展示多个正负因素如何形成最终总量 | 盈亏、增减构成 |
| `structure.data.scatter` | 散点图 | 用点的位置表达两个连续变量 | 相关性、异常点 |
| `structure.data.bubble` | 气泡图 | 在散点基础上用面积增加第三变量 | 多变量关系 |
| `structure.data.histogram` | 直方图 | 用连续区间显示频数分布 | 分布形状、集中程度 |
| `structure.data.boxplot` | 箱线图 | 概括中位数、范围和异常值 | 多组分布比较 |
| `structure.data.heatmap` | 热力图 | 用颜色强度编码二维数值 | 密度、时段规律、矩阵关系 |
| `structure.data.radar` | 雷达图 | 在多个径向维度上显示对象特征 | 多指标画像，非精细比较 |
| `structure.data.ranking` | 排行结构 | 按数值或优先级排列对象 | 名次、Top N、优先级 |
| `structure.data.uncertainty_band` | 不确定区间 | 用带状范围表示估计值的不确定性 | 预测、置信区间 |
| `structure.data.scenario_fan` | 情景扇形 | 从当前点向未来展开多个可能范围 | 长期预测、风险情景 |

## 2.9 空间、地图与位置

| ID | 中文名称 | 定义 | 适合表达 |
|---|---|---|---|
| `structure.spatial.locator_map` | 定位地图 | 说明地点在更大地理范围中的位置 | 城市、国家、事件地点 |
| `structure.spatial.choropleth` | 分级设色地图 | 用区域颜色表达比率或强度 | 人口率、风险率、投票率 |
| `structure.spatial.symbol_map` | 比例符号地图 | 用符号大小表达地点的绝对数量 | 城市人口、事件数量 |
| `structure.spatial.route_map` | 路线地图 | 在地图上绘制移动路线 | 迁徙、运输、旅行 |
| `structure.spatial.flow_map` | 流向地图 | 同时表达地理位置与流动方向或规模 | 贸易、人口、物流 |
| `structure.spatial.heat_map` | 空间热力图 | 用连续颜色表达空间密度 | 活动热点、温度、污染 |
| `structure.spatial.contour` | 等值线图 | 用等值线表达连续空间场 | 海拔、气压、温度 |
| `structure.spatial.floor_plan` | 平面布局图 | 用俯视图表达空间结构和位置 | 建筑、房间、设备布局 |
| `structure.spatial.section` | 空间剖面 | 切开空间以显示内部纵深关系 | 地层、建筑、人体 |

## 2.10 科学、结构与抽象推导

| ID | 中文名称 | 定义 | 适合表达 |
|---|---|---|---|
| `structure.science.annotated_object` | 对象标注图 | 在对象周围标注名称、属性或功能 | 器官、设备、产品介绍 |
| `structure.science.cutaway` | 局部剖切图 | 移除部分外壳并保留外部上下文 | 机械内部、建筑内部 |
| `structure.science.cross_section` | 完整截面图 | 沿平面切开对象显示截面结构 | 地质、人体、材料 |
| `structure.science.exploded_view` | 爆炸图 | 将零件分离显示组装顺序和关系 | 产品拆解、机械结构 |
| `structure.science.peel_layers` | 逐层剥离 | 逐层移除表层显示内部层次 | 皮肤、地球、复合材料 |
| `structure.science.scale_zoom` | 尺度下钻 | 在宏观和微观尺度间连续移动 | 宇宙、细胞、芯片 |
| `structure.science.particle_model` | 粒子模型 | 用粒子位置和运动解释微观现象 | 气体、扩散、统计运动 |
| `structure.science.force_vector` | 力与矢量图 | 用带方向和大小的箭头表达作用 | 力学、速度、电场 |
| `structure.science.wave` | 波形结构 | 用振幅、频率和传播方向表达波 | 声音、光、电信号 |
| `structure.science.orbit` | 轨道结构 | 用围绕中心的路径表达周期运动 | 行星、电子、卫星 |
| `structure.science.transformation` | 形态转化图 | 连续展示对象结构或状态变化 | 相变、化学反应、演化 |
| `structure.reasoning.formula_derivation` | 公式推导 | 按逻辑步骤展示公式变化 | 数学、物理推导 |
| `structure.reasoning.equation_balance` | 等式平衡 | 用两侧平衡表达等价关系 | 方程、守恒、收支 |
| `structure.reasoning.hypothesis_evidence` | 假设—证据结构 | 将假设与支持或反对证据对应 | 科学论证、调查分析 |
| `structure.reasoning.problem_solution` | 问题—方案结构 | 将问题、原因、方案和结果组织为链条 | 改进建议、产品解释 |
| `structure.reasoning.myth_fact` | 误区—事实结构 | 将错误认知和正确解释直接对照 | 辟谣、知识纠错 |

---

# 三、画面组织 Scene Composition

画面组织描述整个镜头的舞台和主要区域关系。它是镜头级结构，通常高于卡片、标签等组件。

| ID | 中文名称 | 定义 | 适合场景 |
|---|---|---|---|
| `composition.fullscreen_takeover` | 全屏接管 | 视觉内容完全占据画面 | 复杂图表、重要解释、章节重点 |
| `composition.presenter_overlay` | 人物加浮层 | 保留人物主体并在周围叠加图形 | 口播、轻量补充信息 |
| `composition.presenter_sidecar` | 人物侧挂信息区 | 人物与固定信息区并列 | 持续讲解、列表和图表 |
| `composition.split_horizontal` | 左右分屏 | 画面分为左右两个主要区域 | 人物与图形、A/B比较 |
| `composition.split_vertical` | 上下分屏 | 画面分为上下两个主要区域 | 原画面与字幕、过程与结果 |
| `composition.picture_in_picture` | 画中画 | 一个画面作为较小窗口嵌入主画面 | 案例视频、软件演示、来源引用 |
| `composition.center_stage` | 中心舞台 | 主对象居中，辅助信息围绕分布 | 产品、器官、核心概念 |
| `composition.dashboard` | 仪表盘 | 多个固定信息组件同时呈现 | 多指标状态、综合数据 |
| `composition.grid` | 网格画面 | 使用规则网格容纳多个并列对象 | 分类、案例、人物、产品 |
| `composition.panel_sequence` | 分格叙事 | 使用漫画式分格表达连续事件 | 情景故事、前因后果 |
| `composition.infinite_canvas` | 无限画布 | 镜头在连续大画布中移动 | 知识地图、长流程、复杂关系 |
| `composition.document_stage` | 文档舞台 | 以网页、论文或文件作为主要画面 | 证据、引用、解读原文 |
| `composition.map_stage` | 地图舞台 | 地图持续作为空间参照 | 地理、历史、迁移、战争 |
| `composition.object_stage` | 对象舞台 | 单一物体持续作为解释中心 | 产品拆解、人体、机械 |
| `composition.ui_stage` | 界面舞台 | 软件或设备界面作为主要画面 | 教程、产品功能、交互说明 |
| `composition.live_action_composite` | 实拍合成舞台 | 在实拍空间中放置跟踪图形或虚拟对象 | 人物互动、现场科普 |
| `composition.typography_stage` | 字体舞台 | 文字本身承担主要视觉叙事 | 金句、概念、情绪强化 |
| `composition.blank_field` | 留白舞台 | 使用大量留白突出少量信息 | 极简解释、关键结论 |

---

# 四、素材形态 Visual Medium

素材形态描述镜头实际使用的视觉对象。一个镜头通常可以组合多种素材形态。

| ID | 中文名称 | 定义 | 常见用途 |
|---|---|---|---|
| `medium.text` | 文字 | 标题、正文、标签、注释等文字对象 | 概念、结论、说明 |
| `medium.number` | 数字 | 数值、百分比、倍数、日期等数字对象 | 数据强调、计算、比较 |
| `medium.symbol` | 符号 | 箭头、运算符、货币符号、警告符号 | 关系、方向、逻辑 |
| `medium.icon` | 图标 | 高度简化的象征性图形 | 列表、分类、快速识别 |
| `medium.geometric_shape` | 几何图形 | 圆、线、矩形等抽象形状 | 结构、运动、抽象概念 |
| `medium.vector_illustration` | 矢量插画 | 可缩放的二维插画对象 | 人物、场景、产品、隐喻 |
| `medium.character` | 角色 | 具有人物或拟人身份的视觉对象 | 案例、情境、情绪 |
| `medium.pictogram` | 象形单位 | 可重复计数的简化对象 | 人数、比例、规模 |
| `medium.chart` | 图表 | 使用视觉编码呈现数据关系 | 趋势、比较、分布 |
| `medium.diagram` | 图解 | 使用节点、线条、区域解释关系 | 流程、层级、机制 |
| `medium.map` | 地图 | 表达地理或空间位置的底图 | 地点、路线、区域数据 |
| `medium.document` | 文档 | 论文、报告、合同、书页等文件图像 | 来源、证据、原文 |
| `medium.screenshot` | 截图 | 网页、应用或社交媒体的静态截图 | 引用、案例、界面说明 |
| `medium.ui` | 界面组件 | 按钮、菜单、输入框、窗口等界面对象 | 产品功能、操作演示 |
| `medium.code` | 代码 | 程序代码、终端命令、配置内容 | 编程科普、技术说明 |
| `medium.formula` | 公式 | 数学或科学符号表达式 | 推导、定量关系 |
| `medium.photo` | 照片 | 静态真实影像 | 人物、地点、历史、证据 |
| `medium.video` | 视频片段 | 连续真实或生成影像 | 案例、实验证明、现场 |
| `medium.archive` | 档案素材 | 历史照片、旧报纸、录像或手稿 | 历史、溯源、纪实 |
| `medium.texture` | 纹理 | 纸张、噪点、材质等表面元素 | 风格统一、空间层次 |
| `medium.particle` | 粒子 | 大量点、碎片或微小对象 | 微观、流动、能量、聚合 |
| `medium.wave` | 波形 | 连续振荡或信号曲线 | 声音、光、电信号 |
| `medium.2d_model` | 二维模型 | 可拆解或变形的二维结构模型 | 机制、结构、示意 |
| `medium.3d_model` | 三维模型 | 具有体积和空间关系的模型 | 产品、机械、人体、科学 |
| `medium.live_subject` | 实拍主体 | 原视频中的人物或真实物体 | 口播、现场演示 |
| `medium.generated_image` | 生成图像 | 通过生成模型得到的视觉素材 | 难以拍摄的情境、概念插图 |
| `medium.generated_video` | 生成视频 | 通过生成模型得到的连续影像 | 假设场景、历史重建、隐喻 |

---

# 五、画面容器 Visual Container

画面容器是承载信息的局部组件。容器可以不存在，此时信息直接存在于画面空间中。

| ID | 中文名称 | 定义 | 常见用途 |
|---|---|---|---|
| `container.none` | 无容器 | 对象直接存在于画面中 | 极简画面、自由构图 |
| `container.card.title` | 标题卡 | 承载标题、章节或主题 | 章节切换、主题引入 |
| `container.card.definition` | 定义卡 | 承载术语及简明定义 | 概念解释、缩写展开 |
| `container.card.metric` | 数字卡 | 承载关键数值、单位和说明 | KPI、比例、增长率 |
| `container.card.fact` | 事实卡 | 承载简短事实或知识点 | 冷知识、研究发现 |
| `container.card.quote` | 引语卡 | 承载直接引语及来源 | 专家观点、历史原话 |
| `container.card.person` | 人物卡 | 承载人物姓名、身份和信息 | 人物介绍、案例 |
| `container.card.step` | 步骤卡 | 承载流程中的单个步骤 | 操作、流程、阶段 |
| `container.card.pro_con` | 利弊卡 | 承载单项优点或缺点 | 方案评估、正反分析 |
| `container.card.warning` | 警告卡 | 承载风险、禁止或注意信息 | 安全提示、限制条件 |
| `container.card.summary` | 总结卡 | 承载结论或回顾信息 | 段落总结、结尾回收 |
| `container.panel` | 信息面板 | 可容纳多个相关元素的较大区域 | 图表、说明、仪表盘 |
| `container.label` | 标签 | 紧贴对象的短名称或状态 | 标注、分类、状态 |
| `container.badge` | 徽标 | 用小型高强调组件表示身份或状态 | 新增、重点、等级 |
| `container.chip` | 标签片 | 可并列排列的短词组件 | 分类、属性、关键词 |
| `container.callout` | 注释框 | 通过引线指向被解释对象 | 局部说明、结构标注 |
| `container.tooltip` | 悬浮信息框 | 临时显示对象的补充信息 | 数据点、界面说明 |
| `container.banner` | 横幅 | 横向占据较大宽度的信息条 | 结论、提醒、章节 |
| `container.lower_third` | 下三分之一字幕条 | 位于画面下方的人物或主题信息条 | 姓名、职务、来源 |
| `container.modal` | 弹窗 | 覆盖原内容的集中信息窗口 | 重要提示、详细解释 |
| `container.device_frame` | 设备框 | 用手机、平板或电脑外框承载界面 | 产品演示、应用教程 |
| `container.browser_frame` | 浏览器框 | 用浏览器窗口承载网页内容 | 网站、搜索、网页证据 |
| `container.document_frame` | 文档框 | 用纸张或文件边界承载原文 | 论文、报告、档案 |
| `container.photo_frame` | 图片框 | 用边框、拍立得或幻灯片承载照片 | 历史、人物、案例 |
| `container.code_window` | 代码窗口 | 用编辑器或终端窗口承载代码 | 编程、命令、技术演示 |
| `container.map_inset` | 地图嵌框 | 在主地图或主画面中嵌入局部地图 | 定位、局部放大 |
| `container.tab` | 标签页 | 在同一区域切换多组内容 | 多方案、多分类 |
| `container.carousel` | 轮播容器 | 让多个同类内容依次占据同一区域 | 案例、卡片、产品 |
| `container.stack` | 堆叠容器 | 将多个组件以层叠方式组织 | 历史记录、多层信息 |

---

# 六、运动方式 Motion Pattern

运动方式描述元素如何进入、构建、变化、强调、建立关系、转场和退出。一个镜头可以组合多种运动方式。

## 6.1 入场与揭示

| ID | 中文名称 | 定义 | 典型用途 |
|---|---|---|---|
| `motion.enter.fade` | 淡入 | 透明度从无到有 | 通用、克制入场 |
| `motion.enter.slide` | 滑入 | 元素从画面外或邻近位置移动进入 | 卡片、列表、方向关系 |
| `motion.enter.scale` | 缩放进入 | 元素从小到大或从大到正常尺寸 | 重点对象、数字 |
| `motion.enter.pop` | 弹出 | 快速缩放并略带回弹 | 图标、标签、轻松内容 |
| `motion.enter.flip` | 翻转进入 | 元素围绕轴翻转到正面 | 卡片、正反信息 |
| `motion.enter.mask_reveal` | 遮罩揭示 | 通过移动边界逐步显示对象 | 标题、图片、图表 |
| `motion.enter.wipe` | 擦入 | 画面被方向性擦拭揭示 | 前后变化、章节转场 |
| `motion.enter.blur_focus` | 模糊聚焦 | 从模糊逐渐变为清晰 | 焦点建立、记忆、发现 |
| `motion.enter.type_on` | 逐字出现 | 文字按字符、词或短语依次显示 | 引语、术语、代码 |
| `motion.enter.stroke_draw` | 线条绘制 | 轮廓或线条沿路径生成 | 图标、地图、公式、连接线 |
| `motion.enter.assemble` | 聚合组装 | 分散部分移动到正确位置形成整体 | 标志、组件、概念聚合 |
| `motion.enter.particle_form` | 粒子成形 | 粒子聚集形成文字或对象 | 微观、科技、能量 |

## 6.2 构建与推进

| ID | 中文名称 | 定义 | 典型用途 |
|---|---|---|---|
| `motion.build.sequential` | 逐项构建 | 按解释顺序一次加入一个元素 | 列表、步骤、图表 |
| `motion.build.stagger` | 错峰进入 | 同类元素按短时间间隔连续进入 | 卡片阵列、图标列表 |
| `motion.build.stack` | 堆叠 | 元素逐层叠加形成整体 | 构成、层级、累积 |
| `motion.build.group` | 聚类分组 | 分散元素移动并形成若干组 | 分类、归纳 |
| `motion.build.sort` | 排序 | 元素根据数值或类别重新排列 | 排名、分类、比较 |
| `motion.build.path_draw` | 路径生长 | 线或箭头沿方向逐步延伸 | 流程、时间线、路线 |
| `motion.build.connector_draw` | 连线生成 | 在已有节点之间建立连接 | 网络、因果、依赖 |
| `motion.build.node_activate` | 节点点亮 | 节点按顺序切换为激活状态 | 流程、时间线、网络 |
| `motion.build.chart_grow` | 图表增长 | 图形从基线增长到目标值 | 柱形、面积、进度 |
| `motion.build.line_trace` | 折线追踪 | 折线沿数据顺序绘制 | 趋势、轨迹、波形 |
| `motion.build.area_fill` | 区域填充 | 区域或比例从空白逐渐填满 | 地图、进度、构成 |
| `motion.build.count` | 数值计数 | 数字递增或递减到目标值 | KPI、比例、累计值 |
| `motion.build.progress` | 进度推进 | 游标或填充沿既定方向前进 | 时间、任务、教程 |

## 6.3 变形与状态变化

| ID | 中文名称 | 定义 | 典型用途 |
|---|---|---|---|
| `motion.transform.morph` | 形态变换 | 一个形状连续变成另一个形状 | 概念转换、对象演化 |
| `motion.transform.shared_element` | 共享元素转场 | 同一对象在两个布局间保持连续 | 卡片到详情、图标到实物 |
| `motion.transform.reflow` | 布局重排 | 元素平滑移动到新的布局位置 | 分类、排序、比较 |
| `motion.transform.expand` | 展开 | 容器或对象扩展以显示更多内容 | 卡片详情、局部放大 |
| `motion.transform.collapse` | 收拢 | 多个对象收回到更小的整体 | 总结、章节结束 |
| `motion.transform.assemble` | 组装 | 零件移动并连接为完整对象 | 产品、机械、整体构成 |
| `motion.transform.disassemble` | 拆解 | 完整对象分离为组成部分 | 结构解释、问题诊断 |
| `motion.transform.peel` | 剥离 | 移除表面层显示内部内容 | 人体、地球、材料 |
| `motion.transform.cutaway` | 剖切 | 通过切开或隐藏外壳显露内部 | 机械、建筑、器官 |
| `motion.transform.zoom_through` | 穿越缩放 | 镜头穿过对象进入更小或更大尺度 | 宏观到微观、空间层级 |
| `motion.transform.state_toggle` | 状态切换 | 在两个或多个离散状态间切换 | 开关、前后、正确错误 |

## 6.4 强调与注意力引导

| ID | 中文名称 | 定义 | 典型用途 |
|---|---|---|---|
| `motion.emphasis.color` | 颜色强调 | 改变目标对象颜色以建立焦点 | 关键词、数据点、路径 |
| `motion.emphasis.scale` | 尺寸强调 | 短暂放大或缩小目标对象 | 数字、节点、图标 |
| `motion.emphasis.pulse` | 脉冲 | 对象以一次或少量周期轻微缩放或发光 | 关键节点、提醒 |
| `motion.emphasis.halo` | 光晕 | 在对象周围出现柔和光圈 | 科技、定位、重点 |
| `motion.emphasis.underline` | 下划线 | 绘制线条强调文字片段 | 关键词、结论、引语 |
| `motion.emphasis.outline` | 框选描边 | 用边框或轮廓圈定目标 | 局部区域、界面元素 |
| `motion.emphasis.spotlight` | 聚光 | 压暗周围区域并保留目标明亮 | 复杂画面中的局部焦点 |
| `motion.emphasis.dim_others` | 弱化其他项 | 降低非目标对象的对比度 | 比较、列表、网络 |
| `motion.emphasis.magnify` | 放大镜 | 局部放大目标细节 | 文档、地图、微小结构 |
| `motion.emphasis.freeze` | 定格 | 暂停运动以便观察和标注 | 实验、体育、快速事件 |
| `motion.emphasis.shake` | 短促抖动 | 用短暂位移表达错误、危险或冲击 | 警告、失败、碰撞 |
| `motion.emphasis.cross_out` | 划除 | 用线条否定或淘汰内容 | 错误答案、排除项 |
| `motion.emphasis.check` | 勾选 | 出现勾号表示正确或完成 | 清单、确认、结论 |

## 6.5 关系、传播与模拟

| ID | 中文名称 | 定义 | 典型用途 |
|---|---|---|---|
| `motion.relation.particle_flow` | 粒子流动 | 粒子沿通道或路径运动 | 数据、能量、物质流动 |
| `motion.relation.packet_travel` | 数据包传递 | 离散对象从节点移动到节点 | 网络通信、信息传播 |
| `motion.relation.ripple` | 波纹扩散 | 影响从一点向周围传播 | 影响范围、触发、声波 |
| `motion.relation.domino` | 骨牌传导 | 对象按相邻关系依次触发 | 因果链、系统风险 |
| `motion.relation.cascade` | 级联触发 | 多个层级由上到下连续激活 | 层级传播、连锁事件 |
| `motion.relation.wave_propagation` | 波传播 | 振动沿介质或空间向前传播 | 声音、光、信号 |
| `motion.relation.orbit` | 轨道运动 | 对象沿中心轨道周期运行 | 天体、电子、系统循环 |
| `motion.relation.force_response` | 受力响应 | 对象根据矢量方向产生运动或形变 | 力学、磁场、碰撞 |
| `motion.relation.diffusion` | 扩散 | 对象从高密度区域向外随机分散 | 气体、热、信息扩散 |
| `motion.relation.filtering` | 过滤筛选 | 一部分对象通过条件，其他对象被阻挡 | 漏斗、筛选、规则 |

## 6.6 比较与切换

| ID | 中文名称 | 定义 | 典型用途 |
|---|---|---|---|
| `motion.compare.sync` | 同步对照 | 两侧对象以相同节奏同时变化 | A/B过程比较 |
| `motion.compare.wipe` | 擦除对比 | 用移动分界线显示两个状态 | 前后效果、地图变化 |
| `motion.compare.toggle` | 往返切换 | 在两个状态间交替显示 | 开关、旧新方案 |
| `motion.compare.overlay` | 透明叠加 | 重合两个状态并改变透明度 | 轮廓、位置、结构差异 |
| `motion.compare.difference_highlight` | 差异高亮 | 只强调发生变化的部分 | 对比表、产品迭代 |
| `motion.compare.rank_reorder` | 排名重排 | 项目根据数值变化交换位置 | 排名、竞速图 |
| `motion.compare.baseline_lock` | 基准锁定 | 保持统一基线，只让比较量变化 | 数值差异、偏差 |

## 6.7 镜头与空间运动

| ID | 中文名称 | 定义 | 典型用途 |
|---|---|---|---|
| `motion.camera.push_in` | 镜头推近 | 视野向目标靠近 | 建立重点、进入细节 |
| `motion.camera.pull_out` | 镜头拉远 | 视野离开目标并展示更大上下文 | 从局部到整体、总结 |
| `motion.camera.pan` | 平移浏览 | 镜头沿水平或垂直方向移动 | 时间线、长流程、地图 |
| `motion.camera.track` | 跟随 | 镜头跟随运动对象移动 | 路线、粒子、角色 |
| `motion.camera.orbit` | 环绕 | 镜头围绕三维对象旋转 | 产品、机械、器官 |
| `motion.camera.parallax` | 视差 | 不同深度层以不同速度移动 | 2.5D空间、照片、地图 |
| `motion.camera.rack_focus` | 焦点转移 | 清晰焦点从一个深度对象切换到另一个 | 前后关系、空间引导 |
| `motion.camera.whip_pan` | 甩镜 | 快速平移并连接两个场景 | 高能转场、地点切换 |
| `motion.camera.flyover` | 飞越 | 镜头在地图或空间上方移动 | 地理、城市、路线 |

## 6.8 退场与转场

| ID | 中文名称 | 定义 | 典型用途 |
|---|---|---|---|
| `motion.exit.fade` | 淡出 | 元素逐渐透明消失 | 通用、柔和结束 |
| `motion.exit.slide` | 滑出 | 元素沿方向离开画面 | 卡片、流程推进 |
| `motion.exit.collapse` | 收拢退场 | 元素缩回某个容器或中心 | 总结、返回上级 |
| `motion.exit.scatter` | 分散退场 | 整体拆散并离开 | 粒子、解体、转化 |
| `motion.transition.crossfade` | 交叉叠化 | 前后画面通过透明度交接 | 时间变化、柔和转场 |
| `motion.transition.match_cut` | 匹配剪辑 | 利用形状、位置或动作相似连接镜头 | 概念联想、连续叙事 |
| `motion.transition.object_bridge` | 对象桥接 | 保留一个对象连接前后镜头 | 章节连续、话题转移 |
| `motion.transition.zoom` | 缩放转场 | 通过快速放大或缩小进入下一场景 | 尺度、空间、节奏 |
| `motion.transition.page_turn` | 翻页 | 用书页或文档翻动连接内容 | 历史、文档、章节 |

---

# 七、视觉风格 Visual Style

视觉风格描述整体美术语言。风格可以组合，但应避免在同一段视频中无理由地频繁切换。

| ID | 中文名称 | 定义 | 适合内容 |
|---|---|---|---|
| `style.flat_vector` | 扁平矢量 | 使用纯色、简洁轮廓和低材质细节 | 通用科普、商业解释 |
| `style.outline` | 线框描边 | 主要依靠线条和少量色块构成对象 | 技术、结构、极简内容 |
| `style.geometric` | 几何图形 | 使用基础几何形状建立抽象视觉语言 | 概念、数据、转场 |
| `style.pictogram` | 象形图标 | 使用高度简化且统一的图标系统 | 数量、分类、公共信息 |
| `style.editorial` | 编辑设计 | 借鉴杂志版式、排版和图片编排 | 社会、文化、商业科普 |
| `style.swiss` | 瑞士排版 | 强调网格、无衬线字体、秩序和高对比 | 理性、现代、品牌内容 |
| `style.data_journalism` | 数据新闻 | 以清晰图表、注释和证据为中心 | 数据分析、政策、经济 |
| `style.kinetic_typography` | 动态字体 | 以文字的排版和运动承担主要叙事 | 金句、概念、强节奏段落 |
| `style.hand_drawn` | 手绘 | 保留手工线条和不完全规则感 | 亲切解释、教育、创意 |
| `style.whiteboard` | 白板 | 模拟在白色画面上实时书写和绘图 | 教学、推导、过程解释 |
| `style.chalkboard` | 黑板粉笔 | 使用深色底和粉笔式线条 | 课堂、数学、怀旧教育 |
| `style.paper_cut` | 纸片剪贴 | 使用纸张层次和剪切边缘构成画面 | 轻松、人文、儿童内容 |
| `style.collage` | 拼贴 | 组合照片、文字、纹理和图形碎片 | 历史、文化、观点表达 |
| `style.print_halftone` | 印刷半色调 | 使用网点、套色和纸张质感 | 新闻、复古、评论 |
| `style.watercolor` | 水彩 | 使用柔和、渗透和手绘色彩 | 自然、人文、治愈主题 |
| `style.ink` | 墨线 | 使用墨色线条、笔触和留白 | 历史、文化、东方主题 |
| `style.blueprint` | 蓝图 | 使用蓝底、网格、白线和尺寸标注 | 工程、机械、建筑 |
| `style.technical_schematic` | 技术示意 | 使用规范线条、编号和结构标注 | 设备、系统、技术原理 |
| `style.scientific_atlas` | 科学图鉴 | 使用准确插画、分类标注和图谱式布局 | 生物、地理、自然科学 |
| `style.medical_illustration` | 医学插画 | 使用准确的人体结构与医学配色 | 健康、解剖、生理机制 |
| `style.isometric` | 等距2.5D | 使用统一等距视角表现空间和系统 | 城市、流程、数字产品 |
| `style.low_poly` | 低多边形 | 使用简化多边形构成三维对象 | 地形、科技、抽象场景 |
| `style.clay` | 黏土风 | 使用圆润、柔软、手工模型质感 | 轻松、儿童、生活方式 |
| `style.voxel` | 体素风 | 使用规则立方体构成三维对象 | 游戏、数字、结构分解 |
| `style.stylized_3d` | 风格化3D | 使用非写实比例、材质和灯光 | 品牌、产品、娱乐科普 |
| `style.photoreal_3d` | 写实3D | 追求真实材质、光照和空间比例 | 产品、机械、科学模拟 |
| `style.glass` | 玻璃质感 | 使用透明、折射、模糊和高光 | 科技、界面、高端品牌 |
| `style.acrylic` | 亚克力层叠 | 使用半透明彩色板材形成层次 | 数据、结构、现代视觉 |
| `style.metallic` | 金属机械 | 使用金属材质、工业结构和机械细节 | 制造、工程、硬科技 |
| `style.neon_tech` | 霓虹科技 | 使用暗底、发光线条和高饱和强调色 | 网络、AI、未来科技 |
| `style.hud` | HUD界面 | 使用仪表、扫描线、网格和实时标记 | 军事、航天、监测系统 |
| `style.dark_tech` | 暗黑科技 | 使用深色空间、精细图形和克制光效 | AI、芯片、网络安全 |
| `style.retro_science` | 复古科教 | 模拟旧教材、胶片、早期科教片 | 历史科学、怀旧解释 |
| `style.pixel_art` | 像素风 | 使用低分辨率像素块构成画面 | 游戏、计算机史、轻松内容 |
| `style.documentary_overlay` | 纪实叠加 | 在照片或实拍上使用克制标题和标注 | 历史、调查、人物故事 |
| `style.ui_product` | 产品界面风 | 延续真实产品的界面和品牌系统 | 软件、应用、数字服务 |
| `style.photo_montage` | 照片蒙太奇 | 通过照片组合、裁切和镜头运动叙事 | 历史、人物、案例 |
| `style.live_action_graphics` | 实拍图形合成 | 将动态图形与真实人物或空间结合 | 口播、实验、现场科普 |
| `style.mixed_media` | 混合媒介 | 有控制地组合多种素材和美术语言 | 创意解释、复杂叙事 |
| `style.minimal` | 极简 | 使用少量元素、留白和有限色彩 | 核心概念、专业内容 |
| `style.maximal` | 高密度装饰 | 使用丰富层次、图形和纹理 | 高能片头、文化拼贴，慎用于复杂知识 |

---

# 八、运动气质 Motion Character

运动气质描述运动的整体感受。它不等于某一个具体动作，而是对节奏、重量、连续性和弹性的统一约束。

| ID | 中文名称 | 定义 | 适合内容 |
|---|---|---|---|
| `character.restrained` | 克制 | 动作幅度小、次数少，不抢夺内容注意力 | 严肃科普、数据、纪录 |
| `character.precise` | 精确 | 时间点清楚、路径明确、几乎没有多余摆动 | 技术、工程、流程、数据 |
| `character.calm` | 平静 | 节奏舒缓、过渡柔和、停留充分 | 医疗、人文、长解释 |
| `character.soft` | 柔和 | 加减速圆润、边界和动作不尖锐 | 生活、健康、儿童 |
| `character.snappy` | 干脆 | 动作短促、响应快速、停止明确 | 商业、产品、短视频 |
| `character.elastic` | 弹性 | 带有适度回弹和形变 | 轻松、活泼、角色和图标 |
| `character.playful` | 俏皮 | 使用意外节奏、拟人反应和趣味运动 | 儿童、生活、轻知识 |
| `character.mechanical` | 机械 | 运动像机器一样规则、分段或联动 | 制造、系统、工业 |
| `character.heavy` | 沉重 | 启动慢、惯性强、停止有重量感 | 大型机械、风险、重大结论 |
| `character.lightweight` | 轻盈 | 启动快、位移轻、视觉重量低 | 图标、标签、界面 |
| `character.fluid` | 流体 | 运动连续、可变形、方向转换平滑 | 液体、能量、抽象概念 |
| `character.floating` | 漂浮 | 缓慢悬浮、失重或轻微摆动 | 太空、梦境、背景元素 |
| `character.energetic` | 高能 | 节奏快、对比强、运动密度高 | 片头、高潮、年轻内容 |
| `character.rhythmic` | 节奏化 | 动作按照语音、音乐或固定拍点组织 | 动态字体、列表、总结 |
| `character.staged` | 分阶段教学式 | 一次只推进一个认知动作并留出理解时间 | 流程、公式、机制解释 |
| `character.continuous` | 连续 | 对象在镜头间保持位置、身份或运动连续 | 长流程、空间探索、形态变化 |
| `character.cinematic` | 电影化 | 使用镜头、景深、光影和较长铺垫建立氛围 | 历史、宇宙、重大主题 |
| `character.suspenseful` | 悬念式 | 延迟揭示结果并逐步收紧注意力 | 谜题、调查、反转 |
| `character.organic` | 有机 | 运动具有自然的不完全规则和生命感 | 生物、自然、手绘 |
| `character.glitchy` | 故障式 | 使用跳帧、错位、噪声和数字故障 | 网络安全、错误、数字主题 |
| `character.impactful` | 冲击式 | 使用快速聚焦、强停止和明显尺度变化 | 关键结论、警示、反转 |
| `character.invisible` | 隐性运动 | 运动仅用于维持连续性，观众不应主动注意 | 通用转场、严谨解释 |

---

# 九、组合示例

以下示例仅用于说明八个维度如何组合，不代表固定模板。

## 示例 A：解释“某指标增长了 20%”

```yaml
information_intent:
  primary: intent.magnitude
  secondary:
    - intent.proportion
    - intent.emphasis
visual_structure:
  primary: structure.data.kpi
  supporting:
    - structure.data.progress_ring
scene_composition: composition.fullscreen_takeover
visual_medium:
  - medium.number
  - medium.text
  - medium.chart
visual_container: container.card.metric
motion_pattern:
  - motion.build.count
  - motion.build.area_fill
  - motion.emphasis.scale
visual_style:
  - style.editorial
  - style.minimal
motion_character:
  - character.precise
  - character.restrained
```

## 示例 B：解释一个三阶段工作流程

```yaml
information_intent:
  primary: intent.process
visual_structure:
  primary: structure.process.linear_flow
scene_composition: composition.fullscreen_takeover
visual_medium:
  - medium.icon
  - medium.text
  - medium.diagram
visual_container: container.card.step
motion_pattern:
  - motion.build.sequential
  - motion.build.path_draw
  - motion.build.node_activate
visual_style:
  - style.flat_vector
motion_character:
  - character.staged
  - character.precise
```

## 示例 C：解释机械内部结构

```yaml
information_intent:
  primary: intent.mechanism
  secondary:
    - intent.part_whole
visual_structure:
  primary: structure.science.exploded_view
scene_composition: composition.object_stage
visual_medium:
  - medium.3d_model
  - medium.text
visual_container: container.callout
motion_pattern:
  - motion.transform.disassemble
  - motion.build.connector_draw
  - motion.emphasis.dim_others
visual_style:
  - style.technical_schematic
  - style.stylized_3d
motion_character:
  - character.mechanical
  - character.staged
```

---

# 十、词典边界

以下内容不属于本 Taxonomy：

- 语义块如何切割；
- 哪个语义块必须使用动效；
- 具体模板文件或代码组件；
- 元素的像素坐标、字号和色值；
- 动画的精确持续时间与缓动曲线；
- 素材搜索、生成或授权方式；
- 渲染引擎与技术实现。

这些内容可在后续的组合规则、模板注册表和制作规范中分别定义。
