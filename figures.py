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
