# 具身 VLA / Agentic Robotics · 20 篇论文精读

一个无依赖的静态网页讲义：按时间顺序精读 2022.04—2026.07 的 20 篇具身智能论文（SayCan、Code as Policies、RT-2、π₀.₅、AtomicVLA、Harness VLA、RoboHarness 等），并把它们串成六条问题线索。面向已有 Agent 基础、想进入 Agentic Robotics 的读者。

每页底部有讨论区，欢迎就某个数字、某条边界或某个推演提问。

## 网页入口

- 阅读起点：`docs/index.html`
- 20 篇时间线：`docs/papers.html`
- 单篇精读：`docs/paper-<key>.html`，例如 `docs/paper-harness-vla.html`
- 结构化数据：`docs/papers.json`

发布后由 GitHub Pages 托管 `docs/` 目录，直接在浏览器打开即可，无需后端或账户；只有留言需要 GitHub 账号。

## 每篇精读包含什么

核心记忆点、问题切口、三步方法拆解、机制伪代码、一个具体例子、实验设置与作者报告的结果表、结果解释、消融与结论边界、与其他论文的交叉阅读、一个可自己动手的研究练习。

## 内容边界

- 所有实验数字都是**原论文作者报告**的结果，本讲义没有独立复现。
- π₀.₅ 等图中读数标注为约值；任务成功率、任务进度、计划可执行率、工具调用准确率分别解释，不跨协议合成排行榜。
- 日期为 arXiv v1 首次提交日期（UTC）；每篇另外标出精读所依据的版本，并链接到具体章节或表格。
- 教学推演、伪代码和研究建议都单独标记，不属于论文主张。`docs/downloads/state_handoff.py` 是为讲解编写的标量教学模型，不能作为机器人实验证据。

## 本地预览

需要 Python 3.10+，无第三方依赖：

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory docs
```

然后打开 http://127.0.0.1:8765/papers.html 。也可以直接打开 `docs/index.html`。

## 修改内容后重新生成

```sh
python3 build.py    # 生成 docs/ 下的 29 个页面
python3 verify.py   # 检查内链、锚点、资源、文献范围与实验约束
```

- `content.py`：正文各章、思考题与设备路线。
- `papers.py`：20 篇文献的元数据与简要阅读提示。
- `deep_readings.py`：20 篇完整精读、版本、实验数据与原文定位。
- `build.py`：静态页面生成器。
- `site_config.py`：仓库位置与讨论区配置。
- `research_sources.py`：核查 arXiv 公开 HTML 的缓存工具，产物只留在本地 `.research/`，不随网站发布。

生成页面的样式 URL 带内容哈希，避免浏览器继续使用旧样式。

## 讨论区怎么接

`site_config.py` 里的 `REPO` 决定讨论入口指向哪个仓库。只填 `REPO` 时，每页显示一个指向该仓库 Discussions 的链接；在 <https://giscus.app> 生成 `repo_id` 与 `category_id` 并填入 `GISCUS` 后，评论区会直接嵌在每页底部，按页面路径分成独立话题。改完运行 `python3 build.py`。

前提：仓库公开、已在 Settings 里打开 Discussions、并为仓库安装 giscus 应用。
