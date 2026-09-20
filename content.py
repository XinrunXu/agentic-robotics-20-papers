"""Original teaching text based on the conversation's scope and cited papers.

No material is imported from other directories in the user's workspace.
"""
from html import escape
from deep_readings import NOTES
from site_config import REPO

def section(key, number, title, body):
    return f'<section id="{key}"><h2><span>{number:02}</span>{title}</h2>{body}</section>'

def think(question, answer):
    return f'<details class="reflection"><summary>{question}</summary><div class="answer"><p>{answer}</p></div></details>'

def table(heads, rows):
    return '<div class="table-scroll"><table><thead><tr>'+''.join(f'<th scope="col">{x}</th>' for x in heads)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{x}</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def refs(items):
    return '<div class="chapter-reading"><p class="nav-label">本章论文 · 方法与实验证据</p><ul class="source-list paper-capsules">'+''.join(f'<li><h3><a href="paper-{key}.html">{name} · 精读 →</a></h3><p>{escape(NOTES[key]["takeaway"])}</p><p class="capsule-result">{escape(NOTES[key]["result"])}</p><div class="paper-links"><a href="paper-{key}.html#method">方法拆解</a><a href="paper-{key}.html#results">实验与消融</a><a href="https://arxiv.org/abs/{aid}">原论文 ↗</a><a href="papers.html#{key}">时间线位置</a></div></li>' for name,aid,key in items)+'</ul></div>'

def exercise(title, body):
    return f'<aside class="experiment"><h3>{title}</h3>{body}</aside>'

def star_button():
    """阅读起点的 Star 入口；REPO 为空时不渲染。"""
    if not REPO:
        return ''
    return f'''<div class="star-cta"><a class="star-button" href="https://github.com/{escape(REPO)}" target="_blank" rel="noopener"><span aria-hidden="true">★</span>在 GitHub 上 Star 这份讲义</a><p>觉得这二十篇的整理有用，就点个 Star；读到有疑问的数字或边界，可以在每页底部的讨论区留言。仓库：<a href="https://github.com/{escape(REPO)}">{escape(REPO)}</a></p></div>'''

INTRO = '''<div class="abstract"><strong>核心问题</strong><p>一个已经会规划、调用工具和使用记忆的 Agent，进入物理世界以后，还缺少什么？这份读物沿着二十篇论文中的问题变化，讨论计划如何变成动作、失败如何成为证据，以及经验如何带来下一次改进。</p></div>''' + star_button()
INTRO += section('map',1,'先看问题，再记住系统名字', '''<p>设想机器人要整理早餐台：把餐具放进抽屉，把纸盒移到回收区，并留下仍在使用的杯子。任务理解只是开始。抽屉可能关闭，餐具可能互相遮挡，抓取后还可能滑落；计划中的每一个名词和动词都必须对应实际的状态与能力。</p><p>我们用一个工作定义贯穿全书：<strong>Agentic Robotics 研究如何让目标、环境观测、行为选择、物理执行和反馈形成可持续的决策过程。</strong>这里的 Agent 可以调用已有技能、生成程序、提出几何约束或编排学习策略。各篇论文覆盖的范围并不相同。</p>
<figure class="loop-figure"><div class="loop-row"><div><small>REPRESENT</small><b>目标与世界</b><span>语义 · 场景 · 几何</span></div><i aria-hidden="true">→</i><div><small>DECIDE</small><b>选择与构造</b><span>技能 · 程序 · 约束</span></div><i aria-hidden="true">→</i><div><small>EXECUTE</small><b>控制与接触</b><span>策略 · 规划器 · 设备</span></div></div><div class="loop-returns"><p><span aria-hidden="true">←</span><b>回到 REPRESENT</b>观测更新 · 独立验证任务是否真的完成</p><p class="return-short"><span aria-hidden="true">←</span><b>回到 DECIDE</b>重试 · 换技能 · 换顺序 · 先改变导致失败的条件</p></div><div class="loop-memory"><small>MEMORY</small><b>跨任务经验</b><span>技能 · 修复知识 · 执行记忆</span><em aria-hidden="true">↕ 决策前被检索，执行后被写入</em></div><figcaption>图 1 · 本讲义的概念框架。用于组织阅读，不对应某一篇论文的完整架构。三条回路的去向不同：证据更新表示，判断改变选择，经验跨任务保留；正文按这个区分讨论各篇论文。</figcaption></figure>
<p>阅读时始终问：这篇工作改变了哪一条连接？提供了新的表示、更好的技能、更有效的调度，还是更可靠的验证？用这个问题定位贡献，比把所有系统都记成“LLM + robot”更有帮助。</p>''')
INTRO += section('route',2,'按问题走一遍，再沿时间线回看', '''<p>正文按理解依赖排列。时间索引保留 arXiv 首次提交日期，方便追踪同一问题如何被反复改写；它不把发布时间当作优先权或影响力的充分证据。</p><div class="reading-list">
<a href="foundations.html"><b>01 · 规划为什么需要具身依据？</b><span>SayCan → Inner Monologue</span></a>
<a href="grounding.html"><b>02 · 语言怎样连接空间与动作？</b><span>CaP · ProgPrompt · VoxPoser · SayPlan · RoboCodeX · ReKep</span></a>
<a href="policies.html"><b>03 · VLA 应该扮演什么角色？</b><span>RT-2 · π₀.₅ · AtomicVLA · Harness VLA · RoboHarness</span></a>
<a href="learning.html"><b>04 · 经验究竟改变了什么？</b><span>Voyager · RoboClaw · Playful · ASPIRE</span></a>
<a href="systems.html"><b>05 · 一个系统如何持续运行？</b><span>RoboOS · PhyAgentOS</span></a>
<a href="evaluation.html"><b>06 · 什么才算可信的改进？</b><span>CaP-X · 对照实验 · 预算与泛化</span></a></div>
<p>第一轮先读每章解释并回答思考题；第二轮选两到三篇有关联的论文，检查方法和消融；第三轮进入<a href="experiments.html">按设备开展实验</a>，写出你自己的假设。</p>''')
INTRO += section('outcomes',3,'读完后，用三个产出来检验理解', '''<ol class="outcomes"><li><strong>一张你自己的系统图</strong><p>在每个模块旁写出输入、输出和失败条件，能说明哪些能力来自模型，哪些来自接口与底层控制。</p></li><li><strong>一份有条件的论文比较</strong><p>选择两篇工作，比较观察权限、动作抽象、数据、重试与计算预算，解释哪些结果可以比较。</p></li><li><strong>一个能被否定的研究假设</strong><p>写出设备条件、基线、唯一主要改动、测量指标，以及怎样的结果会让你放弃最初判断。</p></li></ol><p class="note">范围说明：这是一条以语言规划、代码控制、技能学习与策略编排为重点的阅读路线，主要围绕机器人操作与移动操作。它不覆盖机器人学的所有分支，也不把这二十篇定义为唯一的核心文献。</p>'''+think('起始问题：一个强大的 VLA 是否还需要 Agent？','先把目标拆开：如果任务固定、单次策略足够可靠，外部 agent 可能增加成本；如果需要消歧、跨技能组合、检查失败或利用历史经验，外部决策层可能有价值。需要用具体任务与同预算实验回答，不能仅凭架构名字决定。'))

FOUNDATIONS = section('affordance',1,'从“合理”到“此刻做得到”', '''<p>软件 Agent 的工具通常有比较明确的参数与返回值。机器人技能的可用性还随物理状态变化：相同的“打开抽屉”，在把手可见、夹爪空闲与路径畅通时可能可行，在另一种状态下就可能失败。<strong>Affordance 在这里可以理解为与当前状态相关的行动可能性。</strong></p><p>SayCan 将语言层的相关性与技能的可执行性结合。用简化的教学记号，可以把技能选择理解成：</p><div class="equation">score(skill) = task relevance × estimated feasibility</div><p>这只是帮助理解的表达。论文中的语言评分、价值函数与训练设置需要回原文查看；分数不是天然校准的真实成功概率。重要的是：模型认为“下一步有道理”，仍需要能力估计提供具身依据。</p><p>整理早餐台时，移开纸盒可能不是最终目标中最显眼的一步，却可能让抽屉变得可打开。可执行性和长期任务价值也不完全相同：眼前最容易完成的技能，不一定是整体最好的选择。</p>''')
FOUNDATIONS += section('feedback',2,'反馈使计划成为过程', '''<p>SayCan 帮助我们理解选择动作前的判断；Inner Monologue 强调执行期间如何更新判断。系统将场景、成功检测或人类反馈引入语言上下文，让后续计划随环境改变。</p><p>例如机器人尝试打开抽屉后，看到抽屉仍关闭。有效的闭环应重新考虑抓取位置、把手识别或是否存在障碍。简单重复同一条计划，并没有利用失败中的信息。</p>'''+table(['信息','它回答什么','仍然存在的疑问'],[
['语义目标','哪些行动有助于任务？','目标是否有歧义？'],['技能能力','当前技能可能做得到吗？','估计是否覆盖当前场景？'],['执行反馈','环境实际发生了什么？','反馈是否可靠且足够及时？'],['恢复决策','下一步应重复、调整还是结束？','是否改变了导致失败的条件？']])+'''<p>闭环不是一个二元标签。它可能只在子任务之间观察，也可能在动作内部持续反馈。读论文时标明反馈发生的时机，否则“我们也是闭环”不能构成清晰比较。</p>''')
FOUNDATIONS += section('partial',3,'机器人无法直接读取完整世界状态', '''<p>把真实状态记为 <var>s</var>，观测记为 <var>o</var>。相机图像、关节信息和接触信号只提供状态的部分证据。抽屉看上去关闭，可能是视角误差；夹爪闭合，也可能什么都没拿到。</p><p>因此，高层决策依赖的是对状态的判断，而不是一个永远正确的状态变量。对研究生而言，最有用的习惯是把“真值”与“系统能观察到的信息”分开记录。仿真评测可以用真值计算成功率，但如果 agent 也直接读取了真值，这就是额外的观察权限。</p><p>从这里开始，你可以把每篇论文的接口抽象成：<code>历史与观测 → 行为选择 → 执行 → 新证据</code>。再标注观测噪声、调用预算和谁负责判断结束，论文之间的差异就会清楚许多。</p>'''+think('思考：给一个更强的 LLM，能否补救错误的成功检测器？','不一定。如果规划器只收到一个错误的 success 标签而没有其他证据，它可能继续在错误前提上推理。可以给它独立视觉证据，或让检测器在不确定时输出无法判断；但这些都改变了系统输入，需要在对照实验中明确。'))
FOUNDATIONS += section('terms',4,'先统一几个机器人词汇', table(['术语','本讲义中的含义'],[
['策略（policy）','从观测或历史选择动作的规则或模型；它可以是学习得到的，也可以是程序实现的。'],
['技能（skill）','为一个子目标组织的一段行为，例如打开抽屉。不同论文可能用程序、参数化模型或工具接口承载它。'],
['原语（primitive）','当前系统允许直接调用的基本操作。其粒度由系统定义，不一定是最低层电机命令。'],
['末端位姿','机械臂末端的位置和朝向，一个 6 维量（位置 3 + 朝向 3），与关节数无关；需要说明相对哪个坐标系，数值正确也可能因坐标系不一致而执行错误。注意常见的三个“7”含义不同：7 自由度臂的关节数、位置加四元数的 7 个数（自由度仍是 6），以及夹爪 VLA 的 6 维位姿增量加 1 维开合。'],
['自由度（DoF）','可独立变化的关节变量个数，即关节空间的维数；它不等于末端位姿的维数，也不意味着有多个末端位姿。'],
['冗余自由度','关节数多于任务所需维数时多出的部分。7 自由度臂映射到 6 维末端位姿，同一个位姿对应无穷多组关节角，可在保持末端不动的前提下改变臂形以绕障或避奇异。'],
['多指手的“末端”','灵巧手的自由度是手指关节，不参与定义末端位姿。通常末端位姿指腕或掌的位姿（一个 6 维量），每个指尖另有自己的位姿；指尖一般以掌坐标系表达，掌再相对基座，混用这两个坐标系是常见错误。'],
['控制器（controller）','把目标或轨迹落实为执行信号，并利用反馈跟踪。高层的任务规划与这一过程处于不同层次。'],
['TAMP','Task and Motion Planning，任务与运动规划：连接任务步骤的选择与具体运动的可行性。']]))

FOUNDATIONS += exercise('本章研究练习：把失败定位到一条连接', '<p>为“打开抽屉并放入餐具”画出五个节点：目标、状态判断、技能选择、执行、验证。分别构造感知错误、技能不可执行、动作执行失败和完成误判四种情况。每种只改变一个因素，写出需要哪条日志才能区分它。</p><p><strong>完成标准：</strong>同一个失败视频，至少能提出两个不同解释，并说明还缺少什么证据，而不是立即归因于“模型不够强”。</p>')
FOUNDATIONS += refs([('SayCan','2204.01691','saycan'),('Inner Monologue','2207.05608','inner-monologue')])

GROUNDING = section('interface',1,'输出接口决定了模型需要解决多大的问题', '''<p>让模型调用 <code>put_away(cutlery)</code>，与让它输出末端位置、姿态和夹爪命令，是两种复杂度不同的任务。前者把大量感知、规划和控制能力放进了接口；后者要求模型或其他模块补上这些步骤。</p><p>Code as Policies 展示了程序作为策略表达的价值：代码能组合 API、计算几何关系、使用条件与循环。ProgPrompt 则通过程序式提示描述可用对象、动作与示例，使计划贴近具体环境。RoboCodeX 进一步涉及多模态代码生成的结构与训练数据。</p><p>这里需要区分三个改动：<strong>改变输出语言、改变接口抽象、改变模型训练。</strong>它们都可能提高表现，却对应不同的科研问题。若同时改变，很难知道哪一个机制起了作用。</p>'''+table(['表示','例子（示意）','外部系统已经承担什么'],[['技能调用','<code>open(drawer)</code>','把手定位、接近、抓取与拉动'],['程序组合','循环检查抽屉状态，再调用动作','可调用原语与执行环境'],['几何约束','把手与末端满足位置/方向关系','关键点感知、优化与控制'],['动作预测','由图像和指令输出动作块','训练获得的视觉运动能力']]))
GROUNDING += section('geometry',2,'语言与运动之间，需要可操作的空间表示', '''<p>“把纸盒放到杯子右侧”含有目标关系，但并没有给出机器人动作。系统需要确定“右侧”相对哪个坐标系、目标区域是否可达、杯子和纸盒的位置是什么。</p><p>VoxPoser 使用组合的三维价值图，把偏好的位置与约束交给轨迹规划；ReKep 用三维关键点之间的关系函数表达约束，通过分层优化产生动作。两者都把语义与连续运动之间的连接显式化，但表达能力、感知要求与求解过程并不相同。</p><figure class="representation"><div><b>自然语言目标</b><span>抽屉打开到可放入餐具</span></div><div><b>结构化表示</b><span>目标区域 / 关键点关系 / 路径约束</span></div><div><b>求解与控制</b><span>可达轨迹、末端姿态与执行反馈</span></div><figcaption>图 2 · 表示是一种责任分配：语言模型不必独自完成所有数值控制，但必须向求解器提出正确的问题。</figcaption></figure><p>读这两篇论文时，不妨把一次失败分成三类：目标约束就写错了；约束正确但关键点或几何有误；前两者都正确但执行出现接触问题。这会导向三个不同的改进方向。</p>''')
GROUNDING += section('scene',3,'从桌面走向房间：先决定记住哪些状态', '''<p>当任务跨越多个房间时，问题不只是更长的动作序列。Agent 还需要在环境中寻找相关对象，并决定把哪些信息带入当前推理。</p><p>SayPlan 用分层三维场景图组织环境，进行任务相关的语义搜索，再结合路径规划与迭代反馈。场景图是世界状态的结构化描述；VoxPoser 的价值图则用于表达动作偏好与约束。它们都涉及空间，但回答的是不同问题。</p><p>如果环境图记录“餐具在厨房”，它仍不足以告诉机械臂怎样避开桌上的杯子。反过来，一个精确的局部抓取点也不能告诉机器人餐具收纳位置在哪个房间。系统需要在表示层次之间传递任务相关信息。</p>'''+think('思考：给 LLM 更长的上下文，是否就不需要场景图了？','更长上下文可能容纳更多信息，但不自动保证信息及时、结构一致或容易检索。可以比较完整文本状态、任务相关摘要与分层场景表示，在相同观察和推理预算下测规划正确率、延迟与状态更新错误。'))
GROUNDING += exercise('本章研究练习：做一张接口账单','<p>选 CaP 与 ReKep，各追踪一个论文示例。把感知、几何计算、运动规划和控制四项能力分配给“模型生成”“已有工具”“训练策略”或“人工提供”。再提出一个删去某种辅助信息的实验。</p><p><strong>完成标准：</strong>能解释某篇方法看起来更容易完成任务，是否因为接口已提前解决了更多问题。</p>')
GROUNDING += refs([('Code as Policies','2209.07753','cap'),('ProgPrompt','2209.11302','progprompt'),('VoxPoser','2307.05973','voxposer'),('SayPlan','2307.06135','sayplan'),('RoboCodeX','2402.16117','robocodex'),('ReKep','2409.01652','rekep')])

POLICIES = section('vla',1,'先理解被编排的策略', '''<p>VLA（Vision-Language-Action）把视觉、语言与动作预测联系起来。RT-2 通过动作 token 和共同训练研究视觉语言知识如何转移到控制；π₀.₅ 通过异构数据共同训练等机制研究更广的环境泛化。</p><p>对有 Agent 基础的读者，重要的第一步是：一个 VLA 的接口虽然看起来像工具，但内部能力来自数据和训练，其有效范围未必能用几条显式规则完全描述。模型能理解“抽屉”，不代表所有把手形状、视角和接触方式都在它的能力范围内。</p><p>不要把外部编排与端到端策略看作只能二选一。研究可以问：哪些子问题更适合已有策略，哪些更适合几何规划，以及高层决策如何识别这个边界？但必须用任务证据回答，而不是默认增加一层 agent 就会更好。</p>''')
POLICIES += section('granularity',2,'“技能”可以存在于模型内部，也可以是外部接口', '''<p>AtomicVLA 在模型中组织原子技能与专家路由；Harness VLA 将冻结 VLA 暴露为接触操作原语，搭配固定解析原语，由带记忆的 agent 选择调用与预定位方式。前者涉及模型内部的技能学习，后者主要改变策略被使用的方式。</p>'''+table(['比较维度','模型内部技能学习','外部策略编排'],[['改动对象','参数、专家与路由机制','工具接口、状态判断、调用顺序与记忆'],['主要成本','数据与训练','执行探索、推理与接口集成'],['关键证据','技能划分、数据/参数控制、持续学习消融','同策略同预算对照、原语/记忆/恢复消融'],['常见误读','有多个专家就一定有可组合技能','冻结权重就没有经验与计算成本']])+'''<p>一个直接的阅读方法是标出系统在部署过程中改变了什么：参数、代码、记忆、场景状态，还是只是当前动作。不同层的“学习”不能用同一个词轻轻带过。</p>''')
POLICIES += section('handoff',3,'局部技能成功，为什么组合仍然失败？', '''<p>假设抓取策略把餐具拿起来，但结束时手腕姿态与放置策略的训练起点不同。抓取本身成功了，放置策略却可能在它不熟悉的状态下启动。这是策略交接问题。</p><div class="equation">skill A 的终态分布 ≠ skill B 的有效起始状态分布</div><p>Harness VLA 强调将冻结 VLA 用作局部接触能力，并由解析动作处理周围的移动与预定位。RoboHarness 则研究更广的异构策略组合，用能力证据进行路由，并通过 Memory Bridge 改善后续策略开始时的状态兼容性。</p><p>这里的一个研究机会是把“选错技能”与“选对技能但交接状态不合适”分开。两者都表现为下一步失败，却需要不同诊断：前者改变路由，后者可能需要改变进入姿态或场景条件。</p>'''+think('思考：如果 bridge 增加两次动作，成功率提升能证明编排更好吗？','只能说明整个系统在该设置下更成功。要分析机制，还要给基线相同预算，例如同样多的盲重试，比较成功率、交接状态误差与耗时。如果 bridge 只在额外预算下领先，就需要缩小结论。'))
POLICIES += exercise('本章研究练习：给一个策略写能力边界','<p>选择你想使用的策略，写出它接受的观察和动作空间，再列出可能影响成功的五个因素：相机视角、目标位置、物体属性、末端姿态、指令分布。选择一个因素做受控扰动，比较直接调用与带预定位调用。</p><p><strong>没有机器人也能开始：</strong>先用<a href="experiments.html#cpu">标量状态交接实验</a>理解“多次重试”和“改变起始条件”的差别。这个教学模型不代表真实机器人性能。</p>')
POLICIES += refs([('RT-2','2307.15818','rt2'),('π₀.₅','2504.16054','pi05'),('AtomicVLA','2603.07648','atomicvla'),('Harness VLA','2607.08448','harness-vla'),('RoboHarness','2607.18060','roboharness')])

LEARNING = section('carrier',1,'问“学到了什么”，先问它被存在哪里', '''<p>一次任务成功之后，系统下一次为什么能更好？答案可能是模型参数变了、保存了一段代码、增加了失败规则，也可能只是保留了同一任务的上下文。这些机制的迁移范围和成本不同。</p>'''+table(['经验载体','可能带来的能力','应该怎样检验'],[['模型参数','把新数据转成动作能力','固定数据与训练预算，测未见条件'],['可执行代码技能','复用动作组合和控制逻辑','与重新生成、随机检索比较'],['规则与修复知识','减少类似错误，指导程序改进','区分同任务重试与跨任务迁移'],['执行轨迹','支持相似状态检索、能力估计','检查检索数据与测试条件是否重叠']])+'''<p>“没有微调”通常只说明某些参数未更新，不代表没有训练前知识、探索轨迹、人工原语或额外测试时计算。读系统论文时，为这些资源单独列账。</p>''')
LEARNING += section('explore',2,'什么时候探索，决定了学习问题的样子', '''<p>Voyager 在 Minecraft 中通过自动课程与技能库积累行为。Playful 把“下游任务到来之前的自主 play”作为技能获取阶段，测试时从冻结的库中检索。它们提供一种思路：agent 不必只等待具体指令，也可以主动准备可复用能力。</p><p>RoboClaw 则把数据采集、策略学习和执行放进同一循环，利用正向与逆向动作对帮助自复位。其问题重心包含了真实数据采集中的人工成本。这与积累文本规则不同，也与单纯延长推理轮数不同。</p><p>探索任务太容易，可能没有新收益；太难，则大量预算消耗在无效失败上。一个好的实验应同时报告探索成本与下游收益。若只展示最后的成功率，无法判断准备阶段是否值得。</p>''')
LEARNING += section('repair',3,'从一次修复，到可迁移的经验', '''<p>ASPIRE 将细粒度执行反馈、失败诊断、程序修复与验证连接起来，并把有效经验积累到技能库。其价值主张不止是把当前程序修到能运行，还包括让之后的任务少走弯路。</p><p>想验证这一点，需要区分三个层次：同一初始状态反复调试；同一任务换一个初始状态；完全未参与经验构建的新任务。后两者分别检验不同程度的迁移，不能统称为“泛化”。</p><p>可以把有效经验设想为“在某些条件下，某类动作失败，采用某种修复后通过了验证”。这比一句无条件的“应该先旋转夹爪”保留了更多适用范围。这个表达是本讲义的研究建议，不是对所有系统记忆格式的描述。</p><p class="note">ASPIRE 的局限性部分明确指出，真实世界完全自主的终身学习仍受成功检测、复位与安全监控等条件限制。跨本体的个别技能迁移实验，也不能替代长期自主运行的证据。</p>'''+think('思考：技能库越大，效果就应该越好吗？','不必然。过期或不相关技能可能干扰生成，检索成本也会上升。可以固定模型与上下文预算，分别增加相关经验、无关经验和错误经验，观察检索准确性、成功率与修复次数。'))
LEARNING += exercise('本章研究练习：设计一个经验迁移矩阵','<p>以任务、物体、布局为三个维度，明确哪些参与经验收集，哪些仅用于测试。至少设置“无记忆”“随机经验”“相关经验”三组，控制提示长度与尝试预算。预先写出：如果随机经验同样有效，你会如何修改解释。</p>')
LEARNING += refs([('Voyager','2305.16291','voyager'),('RoboClaw','2603.11558','roboclaw'),('Playful Agentic Robot Learning','2606.19419','playful'),('ASPIRE','2607.00272','aspire')])

SYSTEMS = section('architecture',1,'分层的价值，在于让责任可观察', '''<p>当一个 demo 扩展成持续运行的系统，问题会从“模型能不能给出好计划”延伸到“谁维护共享状态、谁确认结果、谁处理异常”。RoboOS 组织高层模型、技能库与共享记忆，关注跨本体和多机器人协作；PhyAgentOS 将 session、状态协议、验证与经验整理为运行时服务。</p><p>阅读系统架构图时，为每条箭头追问三个问题：传的是什么，什么时候更新，错了由谁发现。统一接口有助于替换模块，但接口必须保留足够的执行语义，否则只是把不同设备包装成同名函数。</p>'''+table(['层次','应当保留的信息','不能直接推出的结论'],[['任务决策','目标、子目标、依赖与重规划原因','计划文本完整 ≠ 物理执行成功'],['技能执行','当前阶段、输入状态与退出原因','函数正常返回 ≠ 目标成立'],['共享状态','证据来源、观察时间与冲突处理','写入一次 ≠ 永久正确'],['任务验证','成功条件及其观测证据','检测器高置信度 ≠ 没有误判']]))
SYSTEMS += section('embodiment',2,'跨本体需要明确哪些东西被保留', '''<p>同样是抓取，两台机器人可能有不同的工作空间、末端结构、相机布局与动作表示。高层目标可以相同，但低层接口与能力边界可能必须重新适配。</p><p>所以，看到“跨本体”时应拆开询问：共享的是语言规划器、代码模板、空间约束、动作策略，还是经验规则？有多少标定、数据收集和接口改写发生在实验之前？这些不是否定系统贡献，而是让贡献的范围更准确。</p><p>在多机器人设置中，动作还会改变其他机器人的观察条件。例如一台机械臂移动纸盒，另一台基于旧图像执行抓取。共享记忆的价值不仅是“都能读”，还包括如何处理状态过期与相互影响。</p>''')
SYSTEMS += section('verification',3,'程序结束与任务结束，需要两种证据', '''<p>PhyAgentOS 强调将执行终止与语义任务完成区分开。这是读者可以迁移到自己项目中的系统原则：程序没有抛出异常，说明程序走到了某个终点；餐具是否进入抽屉、抽屉是否关闭，需要来自环境的证据。</p><p>你可以为一次任务保留两条并行记录：执行事件与环境判断。当最终失败发生时，先确定两条记录从哪里开始不一致。这样更容易分清规划错误、执行失败和验证误判，而不是把它们混成一个总体失败率。</p>'''+think('思考：统一一个机器人 API，就能直接复用整个 agent 吗？','高层逻辑可能更容易复用，但同名 API 的前置条件、动作范围与失败语义仍可能不同。一个有价值的迁移实验应固定高层逻辑，公开哪些低层适配发生了，并记录迁移成本与失败类型。'))
SYSTEMS += exercise('本章研究练习：画一次完整任务的证据流','<p>用你自己的方式表达：目标如何进入系统、状态从何而来、哪一步调用技能、怎样判断完成、失败后谁做决策。任选一个模块中断，解释系统还能知道什么、不能知道什么。无需先实现复杂平台。</p>')
SYSTEMS += refs([('RoboOS','2505.03673','roboos'),('PhyAgentOS','2607.16636','phyagentos')])

EVALUATION = section('budget',1,'先比较条件，再比较成功率', '''<p>CaP-X 把原语抽象、感知条件与交互方式放进同一研究框架。它提醒我们：agent 的成绩通常由模型、工具、经验和预算共同决定。</p><p>假设 A 系统获得物体真值位姿，B 系统只能看图像；或 A 可以尝试十次，B 只能执行一次。即便 A 成功率更高，也无法把差异全部归因于规划能力。公平不意味着所有系统必须相同，而是让比较回答一个明确问题。</p>'''+table(['需要固定或公开','为什么影响解释'],[['动作抽象与观察权限','高层工具或真值状态会提前解决部分问题'],['模型与训练/经验数据','更强模型和额外经验会改变能力起点'],['尝试、动作、时间与 token 预算','多轮恢复与搜索通常消耗更多资源'],['任务划分与初始状态','记忆可能已经见过相近任务或状态'],['成功检测与人工介入','系统自报成功、环境真值和人工判断不是同一口径']]))
EVALUATION += section('calculator',2,'一个算例：重试为什么有用，也为什么有代价', '''<p>先建立一个刻意简化的模型：任务有 <var>n</var> 步，每次尝试以相同概率 <var>p</var> 独立成功，失败不会改变环境；每步最多尝试 <var>r</var> 次，某步耗尽次数就结束任务。单步最终成功概率为 <code>q = 1 − (1 − p)^r</code>，全任务成功概率为 <code>q^n</code>。</p>
<div class="calculator"><div class="controls"><label>单次成功率 p <input id="probability" type="range" min="50" max="99" value="90"><output id="probability-label">0.90</output></label><label>任务步数 n <input id="steps" type="range" min="1" max="20" value="8"><output id="steps-label">8</output></label><label>每步最多尝试 <select id="attempts"><option value="1">1 次</option><option value="2" selected>2 次</option><option value="3">3 次</option></select></label></div><div class="result-row" aria-live="polite"><div><small>不重试：任务成功概率</small><strong id="base-success">43.0%</strong></div><div><small>允许重试：任务成功概率</small><strong id="retry-success">92.3%</strong></div><div><small>允许重试：最大调用次数</small><strong id="max-calls">16 次</strong></div></div><p class="note">教学推演，不是机器人实测。真实失败可能相关，重试可能改变状态；这里增加了最大动作预算，因此不能直接用它证明同预算下的算法优势。</p></div>
<p>现在把假设逐一拿掉：如果相机标定有系统偏差，连续三次失败就不独立；如果首次失败把餐具推远，第二次的成功概率也变了。这正是物理恢复值得单独研究的原因。</p>''')
EVALUATION += section('design',3,'让一个改进能被解释，也能被否定', '''<p>一个可操作的研究问题可以写成：“在冻结底层策略、相同总调用预算与相同初始状态下，状态条件化的预定位是否提高策略交接成功率？”这比“加入智能记忆提升长程能力”更容易形成实验。</p><ol><li><strong>先复现一个受限基线：</strong>从单个任务开始，确保观察、动作与评价协议清楚。</li><li><strong>一次改变一个主要机制：</strong>例如只增加 bridge，不同时更换模型和感知器。</li><li><strong>提供预算匹配的对照：</strong>直接执行、额外重试、带 bridge；必要时加入 oracle 条件作为诊断上限。</li><li><strong>保留失败：</strong>报告任务级结果、尝试数、耗时与介入，不只选择成功视频。</li><li><strong>明确统计单位：</strong>同一初始状态的多次尝试通常属于同一个 episode；相关样本不能随意当作独立样本。</li></ol><p>比较配对的初始状态有助于减少环境差异。样本量应结合方差和希望分辨的差异规划；少量试跑首先用于排错与估计波动，不足以支撑广泛结论。</p>'''+think('思考：一个方法从 8/10 提高到 9/10，足以说明稳定进步吗？','还不够。先确认是否同一批任务、是否配对、预算是否一致，再看更多独立运行与不确定性。一次成功与失败的变化，也可能来自场景难度、随机性或评价误差。论文里应报告计数和协议，避免只给一个百分比。'))
EVALUATION += exercise('本章研究练习：写一条会被实验推翻的句子','<p>填写：“我认为机制 M 会在条件 C 下改善指标 Y；如果在预算 B 下，对照方法 A 获得相同或更好的结果，我将把解释修正为 Z。”再列出能够排除替代解释的一个消融。</p><p><a href="downloads/research-protocol.md" download>下载研究问题与实验协议模板</a></p>')
EVALUATION += refs([('CaP-X','2603.22435','capx')])

EXPERIMENTS = section('choose',1,'从现有条件出发，选择能验证的问题', '''<p>设备决定你能测量哪一层现象。普通电脑可以研究表示、规划接口与实验设计；仿真支持受控的物理扰动；真机提供传感、接触与运行成本方面的证据。三条路线都可以形成严谨的小问题，关键是结论不超出实验条件。</p><div class="equipment-tabs" role="group" aria-label="选择设备条件"><button type="button" aria-pressed="true" data-equipment="cpu">普通电脑 · 无 GPU</button><button type="button" aria-pressed="false" data-equipment="sim">可用 GPU · 仿真</button><button type="button" aria-pressed="false" data-equipment="robot">已有机械臂 · 真机</button></div>
<div class="equipment-panel" id="equipment-cpu"><h3>优先研究：状态表示、接口与交接逻辑</h3><p><strong>先读：</strong>SayCan、CaP-X、RoboHarness。<strong>起点：</strong>运行下方 Python 标量状态实验，无第三方依赖，也不调用收费模型。</p><p><strong>唯一改动：</strong>把盲重试换成依据观测的状态修正，保持相同两次操作预算。<strong>产出：</strong>一张观测噪声与成功率的关系表、一组失败例子和适用范围说明。</p><p><strong>下一步：</strong>用相同状态与工具集合比较规则规划器和 LLM 输出；把 API 费用、输入与提示版本记录下来。符号环境结果只支持逻辑与接口层面的结论。</p></div>
<div class="equipment-panel" id="equipment-sim" hidden><h3>优先研究：受控扰动下的技能与恢复</h3><p><strong>先读：</strong>VoxPoser、ReKep、Harness VLA、CaP-X。<strong>起点：</strong>选择一个已能运行的仿真环境与单一操作任务，先复现官方基线的一段 rollout。</p><p><strong>唯一改动：</strong>只改变目标位置或策略交接姿态，比较固定脚本、同预算重试与反馈驱动调整。保持相机、策略权重、动作空间和评测状态一致。</p><p><strong>产出：</strong>成功率随扰动幅度变化的曲线、动作/时间成本、失败分类。先小规模检查显存和运行稳定性，再确定样本量。</p><p><strong>工具入口：</strong><a href="https://github.com/Lifelong-Robot-Learning/LIBERO">LIBERO</a>、<a href="https://github.com/haosulab/ManiSkill">ManiSkill</a>；使用预训练策略时查阅 <a href="https://github.com/Physical-Intelligence/openpi">openpi</a> 当前官方要求。安装、CUDA 和显存条件随版本及模型而变，不按“有一张 GPU”直接保证可运行。</p></div>
<div class="equipment-panel" id="equipment-robot" hidden><h3>优先研究：一个真实技能的能力边界</h3><p><strong>先读：</strong>Inner Monologue、Harness VLA、RoboClaw。<strong>起点：</strong>使用实验室已有、可稳定执行的控制或策略接口，选空载、低速、受控工作区里的单一任务。</p><p><strong>唯一改动：</strong>比较直接调用、固定重试、重新观测后预定位。先确认相机标定、动作单位、夹爪方向和停止机制；不要直接执行模型生成的任意设备命令。</p><p><strong>产出：</strong>包含人工复位与接管时间的运行记录、验证器误判样例，以及“哪些起始条件下技能可靠”的经验图。</p><p><strong>扩展：</strong>当单技能已可测量，再考虑两技能衔接或自主采集。采用 SO-101 等设备时，以 <a href="https://huggingface.co/docs/lerobot/so101">LeRobot 官方设备文档</a>与实验室操作规范为准。本讲义不提供未经设备确认的真机启动命令。</p></div>''')
EXPERIMENTS += section('cpu',2,'动手：让两个“会做事”的策略接起来', '''<p>这是为本讲义编写的独立教学实验。用一个标量 <code>x</code> 表示前一策略结束时的状态；下一策略仅在 <code>|x| ≤ 0.25</code> 时成功。Agent 观察到 <code>y = x + noise</code>。这个标量没有真实位置单位，也没有物理动力学。</p>'''+table(['方案','两次操作预算怎样使用','要回答什么'],[['直接重试','最多调用下一策略两次；失败不改变 x','如果没有改变起始条件，重复是否有用？'],['观测后桥接','先用带噪观测修正 x，再调用策略','改善起点是否比重复调用有效？'],['Oracle 桥接','用真实 x 修正，再调用策略','如果观测无误，理想化机制能达到什么？']])+'''<p><a class="download" href="downloads/state_handoff.py" download>下载 state_handoff.py</a>　<a href="downloads/research-protocol.md" download>下载实验记录模板</a></p><pre><code>python3 state_handoff.py --episodes 200 --seed 7 --noise 0.10
python3 state_handoff.py --episodes 200 --seed 7 --noise 2.00</code></pre><p>需要 Python 3.10 或更新版本，仅使用标准库。脚本输出 CSV 到终端，不写设备、不联网、不训练模型。相同 seed 生成配对初始状态；Oracle 只用于诊断，不能作为具有相同观察权限的公平竞争方法。</p>'''+think('运行前预测：当观测噪声很大，bridge 还会一直更好吗？','不会。修正依据变得不可靠后，bridge 可能把原本可执行的状态移出有效范围。请用不同噪声重复试验，并比较“原本在范围内”和“原本在范围外”两组。机制有效通常有条件，这比只展示一个有利设置更有研究价值。'))
EXPERIMENTS += section('extend',3,'把小实验延伸成研究，而不是扩成大系统', '''<p>先改变一个假设，再讨论增加组件。例如：</p><ul><li><strong>部分可观测：</strong>让观测误差具有偏差或随时间相关，检查单次观测修正是否仍有效。</li><li><strong>不确定时先观察：</strong>在固定总预算内，比较多观察一次与多执行一次的价值。</li><li><strong>能力估计：</strong>不直接告诉 agent 成功区间，而从独立的历史样本估计；用未见状态测试。</li><li><strong>迁移到仿真：</strong>用末端姿态或物体相对位置替换标量，保留同样的对照结构。</li></ul><p>这些都是研究假设，不是已证明结论。遇到负结果时，检查它是否揭示了能力边界：感知噪声过大、修正成本太高、或底层策略本来已覆盖目标状态，都可能使额外编排不值得。</p>''')
EXPERIMENTS += section('proposal',4,'提交一个一页研究提案', '''<ol><li><strong>现象：</strong>写出一个具体失败，不用“泛化不好”概括全部问题。</li><li><strong>假设：</strong>说明哪个机制可能解释失败，提出可被否定的预测。</li><li><strong>条件：</strong>设备、环境、模型、观察权限、数据来源与预算。</li><li><strong>对照：</strong>固定基线、预算匹配基线、主要改动和一个消融。</li><li><strong>测量：</strong>完成率、成本、误判、介入与失败类型。</li><li><strong>结论边界：</strong>说明结果支持什么，以及没有验证什么。</li></ol><p>当你能解释“为什么选择这个对照”以及“什么结果会改变自己的判断”，这份读物就开始转化成你的研究能力了。</p>''')

CHAPTERS = [
('index.html','阅读起点','从 Agent 到<br>Agentic Robotics','理解二十篇论文之间的联系，找到适合自己设备与兴趣的第一个研究问题。',INTRO,[('map','研究问题全景'),('route','建议阅读顺序'),('outcomes','三个学习产出')]),
('foundations.html','规划与具身依据','规划，怎样获得<br>具身依据？','从语言上的合理，走向当前状态下可执行的决策。',FOUNDATIONS,[('affordance','相关性与可执行性'),('feedback','反馈与计划更新'),('partial','不完整的观察'),('terms','机器人词汇')]),
('grounding.html','程序、空间与动作','语言，怎样连接<br>空间与动作？','比较技能调用、程序生成与几何约束，辨认接口中隐含的能力。',GROUNDING,[('interface','输出接口'),('geometry','几何表示'),('scene','场景与状态')]),
('policies.html','VLA 与策略编排','把学习策略放在<br>合适的位置','先理解策略的能力边界，再研究何时调用、怎样交接。',POLICIES,[('vla','理解 VLA'),('granularity','技能的不同载体'),('handoff','策略交接')]),
('learning.html','经验与技能积累','一次经历，如何<br>改变下一次行动？','区分代码技能、修复知识、执行记忆与模型参数中的学习。',LEARNING,[('carrier','经验存在哪里'),('explore','探索的时机'),('repair','修复与迁移')]),
('systems.html','系统与运行时','让一个系统<br>持续运行','从模块组合走向共享状态、跨本体接口与可追踪的任务结果。',SYSTEMS,[('architecture','责任与接口'),('embodiment','跨本体的边界'),('verification','任务完成的证据')]),
('evaluation.html','评测与研究判断','怎样证明<br>改进来自哪里？','从 CaP-X 出发，学习比较条件、控制预算，并设计可以被推翻的假设。',EVALUATION,[('budget','比较条件'),('calculator','重试教学算例'),('design','可解释的实验')]),
('experiments.html','按设备开展实验','从你的设备出发，<br>做一个小实验','普通电脑、仿真与真机，对应不同层次的证据；先选择一个能测清楚的问题。',EXPERIMENTS,[('choose','选择设备路线'),('cpu','标量交接实验'),('extend','受控延展'),('proposal','一页研究提案')]),
]
