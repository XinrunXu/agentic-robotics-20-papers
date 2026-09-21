"""每篇精读中引用的原文框图 / 方法图。

图片文件保存在 `docs/figures/`，由 `fetch_figures.py` 从 arXiv 的 HTML 版下载；
版权归论文作者，页面上保留出处、版本与跳回原文图注的链接。
`ver` 为图片所在的 arXiv 版本，正常与精读引用的版本一致；不一致时用 `note` 说明。
`anchor` 是原文 HTML 中该图的锚点，用于点击图片跳回原文图注。
`what` 同时作为图片的替代文本，描述图里画了什么，不替代论文主张。
"""
from pathlib import PurePosixPath
FIGURES = {
 'saycan': dict(ver='2204.01691v2', path='figures/intro.png', anchor='S0.F1', label='图 1',
  what='语言模型给出与任务相关的候选技能，价值函数给出当前状态下的可执行性，两者结合后决定下一步'),
 'inner-monologue': dict(ver='2207.05608v1', path='feedback-teaser.png', anchor='S1.F1', label='图 1',
  what='场景描述、成功检测与人类反馈如何转成语言，回到规划上下文形成闭环'),
 'cap': dict(ver='2209.07753v4', path='overview_v2.png', anchor='S1.F2', label='图 2',
  what='语言模型生成的策略代码在桌面操作、绘图与移动机器人等多类平台上的调用方式'),
 'progprompt': dict(ver='2209.11302v1', path='plan_and_exec.png', anchor='S1.F2', label='图 2',
  what='程序式提示由导入语句、对象列表与示例任务组成，生成的计划再交给执行'),
 'voyager': dict(ver='2305.16291v2', path='pull_fig_fig.png', anchor='S1.F2', label='图 2',
  what='自动课程、可执行技能库与迭代提示三个组件组成的持续探索循环'),
 'voxposer': dict(ver='2307.05973v2', path='method.png', anchor='S3.F2', label='图 2',
  what='指令与 RGB-D 观测经由代码生成与视觉语言模型组合成三维价值图，再由规划器产生轨迹'),
 'sayplan': dict(ver='2307.06135v1', path='SayPlan_Overview.png', anchor='S1.F1', label='图 1',
  what='先在折叠的三维场景图上做语义搜索，再结合路径规划与场景图模拟器反馈迭代修正计划',
  note='图片取自 v1 的 HTML 版，v2 没有 HTML；本篇精读的方法与结果引用 v2（PDF）。'),
 'rt2': dict(ver='2307.15818v1', path='rt2_teaser.png', anchor='S1.F1', label='图 1',
  what='把机器人动作表示成 token，与网络规模的视觉语言数据联合训练，模型直接输出动作'),
 'robocodex': dict(ver='2402.16117v1', path='teaser_muyao_v2.png', anchor='S0.F1', label='图 1',
  what='树状思维推理把指令分解为面向对象的操作单元，并生成带物理约束的代码'),
 'rekep': dict(ver='2409.01652v2', path='method.png', anchor='S3.F2', label='图 2',
  what='关键点提议、关系约束生成、在线跟踪与分层优化，逐步把语言要求变成末端动作'),
 'pi05': dict(ver='2504.16054v1', path='Figure_3.png', anchor='S2.F3', label='图 3',
  what='两阶段训练：先用多来源异构数据预训练，再后训练得到可部署的策略'),
 'roboos': dict(ver='2505.03673v2', path='overview.png', anchor='S3.F2', label='图 2',
  what='Brain–Cerebellum 分层架构的三个核心组件，以及跨本体协作依赖的共享记忆'),
 'atomicvla': dict(ver='2603.07648v2', path='pipeline.png', anchor='S2.F2', label='图 2',
  what='VLM 预测原子技能与任务进度，再由技能引导的混合专家生成动作'),
 'roboclaw': dict(ver='2603.11558v3', path='figure/RoboClaw.png', anchor='S2.F2', label='图 2',
  what='VLM 作为元控制器，在上下文学习下调度工具与技能，并组织正向操作与逆向复位'),
 'capx': dict(ver='2603.22435v2', path='capagent0_figure.png', anchor='S3.F7', label='图 7',
  what='CaP-Agent0 的结构：自动合成的辅助技能库，配合验证与调试循环'),
 'playful': dict(ver='2606.19419v1', path='f2.png', anchor='S3.F2', label='图 2',
  what='play 阶段自主提出任务、由代码智能体团队求解，并用验证与诊断反馈迭代'),
 'aspire': dict(ver='2607.00272v1', path='system_design.png', anchor='S1.F1', label='图 1',
  what='协调器为每个任务派生 coding agent，逐原语执行证据回流后更新技能库'),
 'harness-vla': dict(ver='2607.08448v4', path='figures/scheme.png', anchor='S0.F1', label='图 1',
  what='规划器在解析原语与冻结 VLA 调用之间选择，并借记忆决定预定位、调用时机与失败后重整'),
 'phyagentos': dict(ver='2607.16636v1', path='paos.png', anchor='S3.F3', label='图 3',
  what='agent 层把目标编译成可执行 session，runtime 层负责监督执行与独立验证'),
 'roboharness': dict(ver='2607.18060v2', path='harness.png', anchor='S3.F1', label='图 1',
  what='异构策略与理解、记忆、执行三类技能库组成的整体框架'),
 'emerge': dict(ver='2608.29896v2', path='2608.29896v2/framework_appendix.png', anchor='S2.F1', label='图 1',
  what='Main Agent 维持活动任务上下文，调度感知、验证、监控等角色化 Sub Agent 与 Operational、Imagination、Evaluation 三类 Skill；结构化证据与技能结果在每次交互后更新任务状态，验证通过推进计划，失败先进入 Branch Stack 局部恢复，Episode 记忆贯穿全程'),
 # 补充阅读的框图
 'vla-touch': dict(ver='2507.17294v2', path='2_framework.png', anchor='S1.F1', label='图 1',
  what='框架总览：上半部是场景图与语言化触觉描述进入 VLM 规划器的循环，下半部是 VLA 动作块经插值控制器按触觉力改写后执行。'),
 'touchguide': dict(ver='2601.20239v6', path='cpm.png', anchor='S4.F3', label='图 3',
  what='框架总览：左侧是接触物理模型的结构，中间是它在采样过程中以可行性分数引导基座策略，右侧画出动作分布被推向真实分布。'),
 'at-vla': dict(ver='2605.07308v2', path='method-v8.png', anchor='S2.F2', label='图 2',
  what='框架总览：触觉门决定触觉 token 是否作为动作专家的条件，门关时各模态同频，门开时触觉以更高频率单独进入。'),
 'vital': dict(ver='2606.14981v1', path='front_figure_corl_v7.png', anchor='S1.F1', label='图 1',
  what='视觉采样与验证先选出行为模式，触觉引导的扩散改写再修正局部接触，基础策略权重不变'),
 'taco': dict(ver='2607.02840v2', path='pipeline_v6.png', anchor='S3.F2', label='图 2',
  what='识别失败邻近状态、联合生成视触修正段、逐帧贴动作与进度标签，过滤排序后并入后训练数据'),
 'touchworld': dict(ver='2607.07287v2', path='3-layer.png', anchor='S2.F2', label='图 2',
  what='慢速的高层规划层、中速的视触目标条件策略与控制回路内的触觉残差修正三层结构'),
 'n0-vtla': dict(ver='2607.23782v1', path='vtlateaser_3.png', anchor='S1.F1', label='图 1',
  what='触觉差分图与图像、指令一起编码，由预测器给出潜在触觉 token z，z 条件化流匹配动作专家；右侧三块面板是三个评测集上的均值对比'),
 'star': dict(ver='2609.12549v2', path='pipeline1_new.png', anchor='S4.F3', label='图 3',
  what='训练配方的三部分：RGB 与触觉图像的掩码联合重建预训练、按接触门筛出的稀疏加全局触觉 token、以及动作时域上五个时刻的未来触觉预测'),
 'ultra': dict(ver='2603.03279v2', path='method_new.png', anchor='S2.F2', label='图 2',
  what='四个阶段串成一条流水线：神经重定向产出物理可行的 rollout，特权教师跟踪它，再蒸馏成多模态学生并做 RL 微调，最后在真实传感下部署'),
 'cybo-waiter': dict(ver='2603.10675v1', path='framework.png', anchor='S3.F1', label='图 1',
  what='VLM 把指令编译成带谓词的子任务，分割与 RGB-D 落成三维几何状态，监督者据此判定并回传诊断，执行层再分派步行与上半身操作'),
 'spatial-brain': dict(ver='2605.21133v2', path='framework.png', anchor='S2.F2', label='图 2',
  what='上半是主动空间大脑的三个模块（主动感知、记忆库、自适应规划），下半是动作小脑按上下肢分成的四个动作 agent 与它们的输出'),
 'simple': dict(ver='2606.08278v1', path='pipeline.png', anchor='S3.F2', label='图 2',
  what='三段流水线：在 MuJoCo 里用运动规划与遥操作采数据，离线在 Isaac Sim 回放渲染，再在不同随机化设置下评测策略'),
 'openhlm': dict(ver='2606.22174v1', path='teaser.png', anchor='S0.F1', label='图 1',
  what='三阶段路线图：先比遥操作接口定下关节式全身，再沿几条轴把操作 VLA 适配到人形全身动作空间，最后用定点遥操作或 HuMI 共训扩展到新物体与新指令'),
 'omega0': dict(ver='2608.06375v2', path='framework.png', anchor='S3.F2', label='图 2',
  what='全身动作 VLM 出前缀，联合视频—动作潜变量预测器让动作查询去注意视频查询，动作 DiT 再去噪出 SONIC 可执行的全身动作潜变量'),
 'wholebodywam': dict(ver='2609.16644v1', path='fig2.png', anchor='S2.F2', label='图 2',
  what='左边是共享扩散 Transformer 从结构化 token 序列联合生成未来视觉、操作动作与 UWBC 指令，右边是按任务方向可操作度下降开合的操作到 UWBC 注意力偏置'),
}

def local_file(key):
    """仓库内的图片文件名：论文 key + 原图扩展名。"""
    return f'{key}{PurePosixPath(FIGURES[key]["path"]).suffix}'

def remote_url(key):
    """图片在 arXiv 上的原始位置，用于下载与标注出处。"""
    f = FIGURES[key]
    return f'https://arxiv.org/html/{f["ver"]}/{f["path"]}'

def origin_url(key):
    """原文中该图所在位置，点击图片跳到这里看完整图注。"""
    f = FIGURES[key]
    return f'https://arxiv.org/html/{f["ver"]}#{f["anchor"]}'
