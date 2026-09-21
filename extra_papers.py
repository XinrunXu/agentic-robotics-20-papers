"""补充阅读的论文元数据。

这些论文不进主线时间线，也不计入主线篇数；它们有各自的精读页
（`extra-<key>.html`），入口在补充阅读页（`extras.html`）的表格里。
图片位置登记在 `figures.py`，与主线共用下载与校验流程。
"""
# 组名 → （页面上的中文标签, 该组所在页面）
EXTRA_GROUPS = {
    'wbc': ('全身控制', 'extras-wbc.html'),
    'tactile': ('触觉反馈', 'extras-tactile.html'),
}

# 组内按 arXiv 首发日期排序；chapter 指回补充阅读页，供面包屑与章节链接使用。
EXTRA_PAPERS = [
dict(key='vla-touch', name='VLA-Touch', date='2025-07-23', arxiv='2507.17294', group='tactile', chapter='extras-tactile',
     topic='触觉双层反馈',
     title='VLA-Touch: Enhancing Vision-Language-Action Models with Dual-Level Tactile Feedback'),
dict(key='touchguide', name='TouchGuide', date='2026-01-28', arxiv='2601.20239', group='tactile', chapter='extras-tactile',
     topic='触觉引导采样',
     title='TouchGuide: Inference-Time Steering of Visuomotor Policies via Touch Guidance'),
dict(key='at-vla', name='AT-VLA', date='2026-05-08', arxiv='2605.07308', group='tactile', chapter='extras-tactile',
     topic='按需注入触觉',
     title='AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models'),
dict(key='vital', name='ViTaL', date='2026-06-12', arxiv='2606.14981', group='tactile', chapter='extras-tactile',
     topic='视触双层引导',
     title='Inference-time Policy Steering via Vision and Touch'),
dict(key='taco', name='TACO', date='2026-07-03', arxiv='2607.02840', group='tactile', chapter='extras-tactile',
     topic='触觉自我修正',
     title='TACO: TActile World Model as a Self-COrrector for Scalable Robot Policy Post-Training'),
dict(key='touchworld', name='TouchWorld', date='2026-07-08', arxiv='2607.07287', group='tactile', chapter='extras-tactile',
     topic='触觉分层控制',
     title='TouchWorld: A Predictive and Reactive Tactile Foundation Model for Dexterous Manipulation'),
dict(key='n0-vtla', name='N₀-VTLA', date='2026-07-26', arxiv='2607.23782', group='tactile', chapter='extras-tactile',
     topic='预测式触觉',
     title='N₀-VTLA: Scaling Vision–Tactile–Language–Action Model with Latent Tactile Tokens'),
dict(key='star', name='STAR', date='2026-09-11', arxiv='2609.12549', group='tactile', chapter='extras-tactile',
     topic='稀疏触觉表示',
     title='STAR: Sparse Tactile Representation Learning in Vision–Tactile–Language–Action Models for Dexterous Manipulation'),
dict(key='ultra', name='ULTRA', date='2026-03-03', arxiv='2603.03279', group='wbc', chapter='extras-wbc',
     topic='统一全身控制',
     title='ULTRA: Unified Multimodal Control for Autonomous Humanoid Whole-Body Loco-Manipulation'),
dict(key='cybo-waiter', name='Cybo-Waiter', date='2026-03-11', arxiv='2603.10675', group='wbc', chapter='extras-wbc',
     topic='谓词监督执行',
     title='Cybo-Waiter: A Physical Agentic Framework for Humanoid Whole-Body Locomotion–Manipulation'),
dict(key='spatial-brain', name='Active Spatial Brain + Action Cerebellum', date='2026-05-20', arxiv='2605.21133', group='wbc', chapter='extras-wbc',
     topic='主动感知分层',
     title='Humanoid Whole-Body Manipulation via Active Spatial Brain and Generalizable Action Cerebellum'),
dict(key='simple', name='SIMPLE', date='2026-06-06', arxiv='2606.08278', group='wbc', chapter='extras-wbc',
     topic='人形全身评测',
     title='SIMPLE: Simulation-Based Policy Learning and Evaluation for Humanoid Loco-manipulation'),
dict(key='openhlm', name='OpenHLM', date='2026-06-20', arxiv='2606.22174', group='wbc', chapter='extras-wbc',
     topic='全身训练配方',
     title='OpenHLM: An Empirical Recipe for Whole-Body Humanoid Loco-Manipulation'),
dict(key='omega0', name='ω-0', date='2026-08-06', arxiv='2608.06375', group='wbc', chapter='extras-wbc',
     topic='全身世界模型',
     title='ω-0: A Latent Predictive World Action Model for Concurrent Humanoid Loco-Manipulation'),
dict(key='wholebodywam', name='WholeBodyWAM', date='2026-09-15', arxiv='2609.16644', group='wbc', chapter='extras-wbc',
     topic='全身接口对齐',
     title='WholeBodyWAM: Generalizing Pre-trained World-Action Priors to Humanoid Loco-Manipulation via WBC-Grounded Coordination'),
]
