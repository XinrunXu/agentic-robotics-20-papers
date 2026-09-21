"""Build a dependency-free, accessible static research reader."""
from pathlib import Path
from html import escape
import json
import re
import hashlib
from content import CHAPTERS, table, think
from extras import EXTRA_PAGES
from extra_papers import EXTRA_PAPERS, EXTRA_GROUPS
from extra_readings import EXTRA_NOTES
from papers import PAPERS
from deep_readings import NOTES
from figures import FIGURES, local_file, origin_url
from site_config import REPO, DISCUSSION_CATEGORY, GISCUS

ROOT = Path(__file__).parent
DIST = ROOT / 'docs'
DIST.mkdir(exist_ok=True)

def span():
    """文献时间范围，由 papers.py 的首发日期推导。"""
    dates = sorted(p['date'] for p in PAPERS)
    fmt = lambda d: d[:7].replace('-', '.')
    return f'{fmt(dates[0])}—{fmt(dates[-1])}'

YEARS = sorted({p['date'][:4] for p in PAPERS})
ALL_NOTES = {**NOTES, **EXTRA_NOTES}   # 精读内容：主线 + 补充阅读

def discussion(slug):
    """讨论入口：填了 GISCUS 就在页面内嵌评论区，只填 REPO 就给出讨论区链接。"""
    if not REPO:
        return ''
    board = f'https://github.com/{REPO}/discussions'
    block = f'''<section class="discuss" id="discuss"><h2><span>QA</span>就这一页提问或讨论</h2>
<p>对某个数字、某条边界或某个推演有疑问，欢迎直接留言：讨论按页面分开，回复会保留在 <a href="{board}">{escape(REPO)} 的 Discussions</a> 里，需要一个 GitHub 账号。</p>'''
    if GISCUS.get('repo_id') and GISCUS.get('category_id'):
        block += f'''<div class="giscus"></div>
<script src="https://giscus.app/client.js" data-repo="{escape(REPO)}" data-repo-id="{escape(GISCUS['repo_id'])}" data-category="{escape(DISCUSSION_CATEGORY)}" data-category-id="{escape(GISCUS['category_id'])}" data-mapping="pathname" data-strict="1" data-reactions-enabled="1" data-emit-metadata="0" data-input-position="top" data-theme="light" data-lang="zh-CN" crossorigin="anonymous" async></script>
<p class="source-note">评论区由 giscus 驱动，内容存放在本仓库的 GitHub Discussions；加载需要联网。</p>'''
    else:
        block += f'<p class="paper-links"><a class="deep-link" href="{board}">打开讨论区留言 →</a></p>'
    return block + '</section>'

def render_page(slug, title, eyebrow, intro, body, nav, toc=(), prev=None, nxt=None, nav_active=None, pager_label='章'):
    style_version = hashlib.sha256((DIST/'style.css').read_bytes()).hexdigest()[:10]
    menu = ''.join(f'<a href="{url}"'+(' aria-current="page"' if url == (nav_active or slug) else '')+f'><span>{num}</span>{label}</a>' for num,label,url in nav)
    talk = discussion(slug)
    if talk:
        toc = list(toc) + [('discuss','提问与讨论')]
    contents = ''.join(f'<a href="#{anchor}">{label}</a>' for anchor,label in toc)
    pager = '<nav class="page-turn" aria-label="章节翻页">'
    pager += f'<a href="{prev[0]}"><small>上一{pager_label}</small>{prev[1]}</a>' if prev else '<span></span>'
    pager += f'<a href="{nxt[0]}"><small>下一{pager_label} →</small>{nxt[1]}</a>' if nxt else '<a href="papers.html"><small>回到时间线</small>串起这些论文的问题脉络</a>'
    pager += '</nav>'
    plain_title = re.sub('<[^>]+>', ' ', title)
    html = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(plain_title)} · Agentic Robotics 研究讲义</title><meta name="description" content="面向已有 Agent 基础的研究生：通过多篇论文理解 Agentic Robotics 的问题脉络、方法边界与按设备条件开展的研究实验。"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css?v={style_version}"><script src="app.js" defer></script></head>
<body><a class="skip" href="#main">跳到正文</a><header class="topbar"><a class="brand" href="index.html"><span class="brand-mark">AR</span><span>AGENTIC ROBOTICS <b>研究讲义</b></span></a><span class="edition">阅读 · 推演 · 实验</span><button class="menu-toggle" aria-expanded="false" aria-controls="sidebar">目录</button></header>
<div class="layout"><aside class="sidebar" id="sidebar"><p class="nav-label">从 Agent 到物理世界</p><nav aria-label="讲义目录">{menu}</nav><div class="side-note">面向有 Agent 基础的研究生<br>文献范围：{span()}<br>整理日期：2026.09.18</div></aside>
<main id="main"><div class="chapter-meta">{eyebrow}</div><h1>{title}</h1><p class="lead">{intro}</p>{body}{talk}{pager}<footer>本讲义区分论文主张、教学推演与研究假设。引用以原论文为准；实验结果只在相应设置下成立。</footer></main>
<aside class="contents"><p class="nav-label">本页内容</p><nav aria-label="本页目录">{contents}</nav><button class="print-button" onclick="window.print()">打印本章 / 存为 PDF</button></aside></div></body></html>'''
    (DIST / slug).write_text(html, encoding='utf-8')

def paper_index():
    body = '<div class="abstract"><strong>从一句话，到一个机制，再到一组证据</strong><p>每篇都有独立精读：问题切口、方法拆解、具体例子、实验设置、关键结果、消融解释与研究练习。先记住下面的核心观点，再进入精读，检查数字为什么成立。</p></div>'
    body += '<p class="note">时间线按 arXiv v1（UTC）排序，精读明确标出实际引用版本。所有实验数字为作者报告，教学例子另作标记；百分比、百分点、任务进度和整任务成功率分别解释。不同论文的数字不构成统一排行榜。</p>'
    year = None
    for i,p in enumerate(PAPERS,1):
        n = NOTES[p['key']]
        if year != p['date'][:4]:
            year = p['date'][:4]
            body += f'<h2 id="y{year}">{year}</h2>'
        body += f'''<article class="paper-entry" id="{p['key']}"><div class="paper-meta"><span>{i:02} / {p['date']}</span><span class="tag">{p['topic']}</span></div><h3><a href="paper-{p['key']}.html">{p['name']}</a></h3><p class="paper-title">{escape(p['title'])}</p><p class="paper-takeaway">{escape(n['takeaway'])}</p><div class="paper-evidence"><span>一组关键证据 · {n['version']}</span><p>{escape(n['result'])}</p></div><p class="paper-links"><a class="deep-link" href="paper-{p['key']}.html">进入精读：方法、实验与消融 →</a><a href="https://arxiv.org/abs/{p['arxiv']}">原论文 ↗</a><a href="{p['chapter']}.html">相关章节</a></p></article>'''
    body += '<p class="note">同日排序：VoxPoser 于 2023-07-12 07:40:48 UTC 首次提交，SayPlan 为 12:37:55 UTC。ASPIRE 的编号为 2607.00272，首次提交日期仍为 2026-06-30。</p>'
    body += '<p class="note">原始来源：每条 arXiv 链接对应论文的元数据、摘要与全文入口。本文不复述未经核查的跨论文统一排名；硬件延展中的工具链接指向各项目的官方仓库或文档。所有教学推演与研究建议均单独标明。</p>'
    body += '<p class="paper-links"><a class="deep-link" href="extras-wbc.html">补充阅读：全身控制 →</a><a class="deep-link" href="extras-tactile.html">补充阅读：触觉 →</a></p>'
    return body

def source_url(p, anchor=''):
    n = ALL_NOTES[p['key']]
    kind = n.get('source_kind', 'html')
    return f'https://arxiv.org/{kind}/{p["arxiv"]}{n["version"]}' + (f'#{anchor}' if anchor else '')

def png_size(path):
    """从 PNG 头部读出像素尺寸，写进 img 标签避免加载时布局跳动。"""
    head = path.read_bytes()[:24]
    if not head.startswith(b'\x89PNG\r\n\x1a\n') or head[12:16] != b'IHDR':
        return ''
    width = int.from_bytes(head[16:20], 'big')
    height = int.from_bytes(head[20:24], 'big')
    return f' width="{width}" height="{height}"'

def paper_figure(key):
    """论文自己的框图 / 方法图；图片文件由 fetch_figures.py 下载到 docs/figures/。"""
    f = FIGURES.get(key)
    if not f:
        return ''
    name = local_file(key)
    stored = DIST / 'figures' / name
    if not stored.is_file():
        raise SystemExit(f'缺少图片 docs/figures/{name}，请先运行 python3 fetch_figures.py {key}')
    note = ' ' + escape(f['note']) if f.get('note') else ''
    return (f'<figure class="paper-figure"><a href="{origin_url(key)}" target="_blank" rel="noopener">'
            f'<img src="figures/{name}" alt="{escape(f["what"])}" loading="lazy" decoding="async"{png_size(stored)}></a>'
            f'<figcaption><b>原文 {f["label"]}</b>{escape(f["what"])}。图片转载自 arXiv {f["ver"]}，'
            f'版权归论文作者；点击图片查看原文图注 ↗{note}</figcaption></figure>')

def paper_body(p, number, back=None):
    n = ALL_NOTES[p['key']]
    e = escape
    source_links = ' · '.join(f'<a href="{source_url(p,anchor)}">{e(label)} ↗</a>' for label,anchor in n['sources'])
    crumb_href, crumb_label = back or (f"papers.html#{p['key']}", f'{len(PAPERS)} 篇论文时间线')
    chapter_link = '' if back else f'<a href="{p["chapter"]}.html">回到相关章节 →</a>'
    body = f'''<nav class="paper-breadcrumb" aria-label="论文位置"><a href="{crumb_href}">{crumb_label}</a><span> / {number:02}</span>{chapter_link}</nav><p class="paper-full-title">{e(p['title'])}</p><div class="paper-bibliography"><span>首发 {p['date']}</span><span>精读版本 {n['version']}</span><a href="{source_url(p)}">阅读原文 ↗</a></div><div class="abstract paper-memory"><strong>先记住这组证据</strong><p>{e(n['result'])}</p></div>'''
    body += '<nav class="paper-jumps" aria-label="精读快速跳转"><a href="#method">看方法</a><a href="#results">看实验</a><a href="#ablation">看消融与边界</a><a href="#practice">做研究练习</a></nav>'
    body += f'<section id="problem"><h2><span>01</span>这篇要解决什么？</h2><p>{e(n["why"])}</p></section>'
    body += f'<section id="scene"><h2><span>02</span>先看一个场景</h2><div class="scene"><span class="small-label">具体情境 · 先有画面，再看机制</span><p>{e(n["scene"])}</p></div></section>'
    body += f'<section id="method"><h2><span>03</span>方法怎样运转？</h2>{paper_figure(p["key"])}<ol class="method-steps">'
    for i,(title,desc) in enumerate(n['steps'],1):
        body += f'<li><span class="step-index">{i:02}</span><div><h3>{e(title)}</h3><p>{e(desc)}</p></div></li>'
    body += f'</ol><figure class="mechanism"><pre><code>{e(n["code"])}</code></pre><figcaption>机制示意 · 讲义编写的简化流程或伪代码，用来解释信息流；不是论文源码或可直接部署的控制程序。</figcaption></figure><p class="source-note">方法与结果的原文定位见<a href="#sources">本页引用</a>。</p></section>'
    example_label = '原文案例解读' if n['example'].startswith('原文') else '教学推演'
    body += f'<section id="example"><h2><span>04</span>跟着这个场景走一遍</h2><div class="worked-example"><span class="small-label">{example_label}</span><p>{e(n["example"])}</p></div></section>'
    body += f'<section id="results"><h2><span>05</span>实验到底表现怎样？</h2><p>{e(n["setup"])}</p><p class="measurement-label">作者报告的实验结果 · {n["version"]}</p>'
    body += table([e(x) for x in n['headers']], [[e(x) for x in row] for row in n['rows']])
    body += f'<p class="source-note">原始证据：{source_links}</p><div class="result-interpretation"><strong>怎样读这组数字</strong><p>{e(n["findings"])}</p></div></section>'
    body += f'<section id="ablation"><h2><span>06</span>收益来自哪里，又停在哪里？</h2><h3>消融与机制证据</h3><p>{e(n["ablation"])}</p><h3>结论的适用边界</h3><p>{e(n["boundary"])}</p></section>'
    body += f'<section id="connect"><h2><span>07</span>放回全书的脉络</h2><p>{e(n["transfer"])}</p><p><a href="{p["chapter"]}.html">{'回到补充阅读，对照另一条支线 →' if back else '回到问题章节，对照相关方法 →'}</a></p></section>'
    body += f'<section id="practice"><h2><span>08</span>把阅读变成一个小研究</h2><div class="experiment"><span class="small-label">讲义提出的研究练习 · 不是论文复现结果</span><p>{e(n["exercise"])}</p></div>'
    body += think('先自己回答：这项实验怎样才有解释力？', e(n['answer']))
    body += '<div class="recall"><strong>合上原文后，试着回答</strong><ol><li>用自己的话说出这篇改变了哪个模块。</li><li>画出它的输入、输出和一次失败如何被处理。</li><li>复述一个结果，同时说清基线、指标与实验条件。这一问不给答案，材料在第 05 节。</li></ol>'
    body += ('<details class="reflection recall-answer"><summary>先自己答，再看前两问的参考答案</summary><div class="answer">'
             f'<p><b>这篇改了哪个模块</b>{e(n["recall_module"])}</p>'
             f'<p><b>输入、输出与一次失败如何被处理</b>{e(n["recall_io"])}</p></div></details>')
    body += f'<p>{e(n["takeaway"])}</p></div></section>'
    body += f'<section id="sources"><h2><span>↗</span>带着位置回到原文</h2><p class="source-note">首发日期用于时间排序；以下方法与结果对应 {n["version"]}。数据为论文作者报告，本讲义没有独立复现实验。</p><ul class="source-list">'
    body += ''.join(f'<li><a href="{source_url(p,anchor)}">{e(label)} ↗</a></li>' for label,anchor in n['sources'])
    body += '</ul></section>'
    return body

if __name__ == '__main__':
    pages = CHAPTERS + [('papers.html',f'{len(PAPERS)} 篇论文精读',f'{len(PAPERS)} 篇论文，<br>记住方法与证据',f'{span()} · 按首次提交时间排序，逐篇解释方法、实验与结论。',paper_index(),[(f'y{y}',y) for y in YEARS])] + EXTRA_PAGES
    nav = [(f'{i:02}',p[1],p[0]) for i,p in enumerate(pages)]
    for i,(slug,label,title,intro,body,toc) in enumerate(pages):
        prev = (pages[i-1][0],pages[i-1][1]) if i else None
        nxt = (pages[i+1][0],pages[i+1][1]) if i+1 < len(pages) else None
        render_page(slug,title,f'{i:02} / AGENTIC ROBOTICS READER',intro,body,nav,toc,prev,nxt)
    paper_toc = [('problem','问题切口'),('scene','具体场景'),('method','方法拆解'),('example','跟着走一遍'),('results','设置与结果'),('ablation','消融与边界'),('connect','论文联系'),('practice','研究与回忆'),('sources','原文定位')]
    for i,p in enumerate(PAPERS):
        prev = (f'paper-{PAPERS[i-1]["key"]}.html', PAPERS[i-1]['name']) if i else ('papers.html','论文时间线')
        nxt = (f'paper-{PAPERS[i+1]["key"]}.html', PAPERS[i+1]['name']) if i+1 < len(PAPERS) else None
        render_page(f'paper-{p["key"]}.html',escape(p['name']),f'PAPER {i+1:02} / {len(PAPERS)} · {escape(p["topic"])}',escape(NOTES[p['key']]['takeaway']),paper_body(p,i+1),nav,paper_toc,prev,nxt,'papers.html','篇')
    for group, (label, group_page) in EXTRA_GROUPS.items():
        group_papers = [p for p in EXTRA_PAPERS if p['group'] == group]
        for i, p in enumerate(group_papers):
            prev = (f'extra-{group_papers[i-1]["key"]}.html', group_papers[i-1]['name']) if i else (group_page, f'补充阅读 · {label}')
            nxt = (f'extra-{group_papers[i+1]["key"]}.html', group_papers[i+1]['name']) if i+1 < len(group_papers) else None
            render_page(f'extra-{p["key"]}.html', escape(p['name']),
                        f'补充阅读 · {escape(label)} {i+1:02} / {len(group_papers):02}',
                        escape(ALL_NOTES[p['key']]['takeaway']),
                        paper_body(p, i+1, back=(f'{group_page}#papers', f'补充阅读 · {label}')),
                        nav, paper_toc, prev, nxt, group_page, '篇')
    export = [{**p,'evidence':NOTES[p['key']]['result'],'reading':NOTES[p['key']]} for p in PAPERS]
    (DIST/'papers.json').write_text(json.dumps(export,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Built {len(pages)+len(PAPERS)+len(EXTRA_PAPERS)} pages with {len(PAPERS)} complete paper readings.')
