"""发布配置：仓库位置与页面内讨论区。

改动本文件后运行 `python3 build.py` 重新生成 docs/。

REPO 为空时页面不含讨论入口；填上 "用户名/仓库名" 就会出现指向该仓库
Discussions 的链接；再补上 GISCUS 里的两个 id，讨论区会直接嵌在每页底部，
按页面路径分成独立话题。
"""
REPO = 'XinrunXu/agentic-robotics-20-papers'

# GitHub Discussions 中用于承载页面评论的分类名称，需与仓库里的分类一致。
DISCUSSION_CATEGORY = 'Announcements'

# 在 https://giscus.app 填入仓库后，页面会给出这两个 id，粘贴到这里即可。
GISCUS = {
    'repo_id': '',
    'category_id': '',
}
