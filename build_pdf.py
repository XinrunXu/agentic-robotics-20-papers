"""把整站导出成一份 PDF 合集。

做法：按阅读顺序抽出每页 <main> 的正文，拼成一个打印版 HTML（pdf/reader.html），
再用无头 Chrome 打成单份 PDF。屏幕上的导航、翻页、讨论区与 Star 入口都不进 PDF。

用法：
    python3 build_pdf.py            # 生成 pdf/reader.html 与 pdf/合集.pdf
    python3 build_pdf.py --html     # 只生成 HTML，不调用 Chrome
"""
import re
import subprocess
import sys
from html import unescape
from pathlib import Path

from content import CHAPTERS
from extra_papers import EXTRA_GROUPS, EXTRA_PAPERS
from extras import EXTRA_PAGES
from papers import PAPERS

ROOT = Path(__file__).parent
DOCS = ROOT / 'docs'
OUT = ROOT / 'pdf'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

TITLE = 'Agentic Robotics 研究讲义'
SUBTITLE = '从 Agent 到物理世界'

# 这些元素只服务于网页，不进 PDF；其中前两项还带着仓库地址。
DROP = [
    re.compile(r'<section[^>]*id="discuss"[^>]*>.*?</section>', re.S),
    re.compile(r'<div[^>]*class="star-cta"[^>]*>.*?</div>', re.S),
    re.compile(r'<nav class="page-turn".*?</nav>', re.S),
    re.compile(r'<nav class="paper-breadcrumb".*?</nav>', re.S),
    re.compile(r'<nav class="paper-jumps".*?</nav>', re.S),
]
MAIN = re.compile(r'<main id="main">(.*?)</main>', re.S)
LOCAL_LINK = re.compile(r'<a [^>]*href="(?!https?:)[^"]*"[^>]*>(.*?)</a>', re.S)


def order():
    """阅读顺序：起点与各章 → 时间线 → 主线精读 → 每条支线的页与精读。"""
    items = [(slug, label) for slug, label, *_ in CHAPTERS]
    items.append(('papers.html', f'{len(PAPERS)} 篇论文精读'))
    for p in PAPERS:
        items.append((f'paper-{p["key"]}.html', p['name']))
    for group, (label, page) in EXTRA_GROUPS.items():
        items.append((page, next(lbl for slug, lbl, *_ in EXTRA_PAGES if slug == page)))
        for p in EXTRA_PAPERS:
            if p['group'] == group:
                items.append((f'extra-{p["key"]}.html', f'{label} · {p["name"]}'))
    return items


def body_of(slug):
    html = (DOCS / slug).read_text()
    body = MAIN.search(html).group(1)
    for pattern in DROP:
        body = pattern.sub('', body)
    body = LOCAL_LINK.sub(r'\1', body)              # 站内链接在纸上没有意义，留文字
    body = body.replace('src="figures/', 'src="../docs/figures/')
    return body


CSS = '''
@page { size: A4; margin: 18mm 16mm; }
body { margin: 0; }
.pdf-item { break-before: page; }
.pdf-cover { break-after: page; text-align: left; padding-top: 32mm; }
.pdf-cover h1 { font-size: 34pt; line-height: 1.25; margin: 0 0 10mm; }
.pdf-cover p { font-size: 12pt; color: #66737c; margin: 0 0 4mm; }
.pdf-toc { break-after: page; }
.pdf-toc h2 { font-size: 18pt; margin: 0 0 6mm; }
.pdf-toc ol { padding-left: 7mm; font-size: 10.5pt; line-height: 1.9; }
.pdf-toc li { margin: 0; }
.pdf-toc .group { list-style: none; margin-top: 4mm; font-weight: 650; color: #245b79; }
main { padding: 0 !important; max-width: none; }
.contents, .sidebar, .topbar { display: none !important; }
'''


def build_html():
    OUT.mkdir(exist_ok=True)
    items = order()
    toc = []
    for slug, label in items:
        mark = ' class="group"' if slug.endswith(('papers.html', 'extras-wbc.html', 'extras-tactile.html')) or slug in [c[0] for c in CHAPTERS] else ''
        toc.append(f'<li{mark}>{label}</li>')
    parts = [f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>{TITLE}</title>
<link rel="stylesheet" href="../docs/style.css"><style>{CSS}</style></head><body>
<div class="pdf-cover"><h1>{SUBTITLE}<br>{TITLE}</h1>
<p>{len(PAPERS)} 篇主线精读，另含两条支线共 {len(EXTRA_PAPERS)} 篇</p>
<p>文献范围 {min(p["date"] for p in PAPERS)[:7].replace("-", ".")}—{max([p["date"] for p in PAPERS] + [p["date"] for p in EXTRA_PAPERS])[:7].replace("-", ".")}</p>
<p>实验数字均为论文作者报告，本讲义未独立复现；教学推演与研究练习为讲义编写内容。</p></div>
<div class="pdf-toc"><h2>目录</h2><ol>{"".join(toc)}</ol></div>''']
    for slug, label in items:
        parts.append(f'<div class="pdf-item">{body_of(slug)}</div>')
    parts.append('</body></html>')
    target = OUT / 'reader.html'
    target.write_text('\n'.join(parts), encoding='utf-8')
    return target, len(items)


def check_name(path, forbidden=('XinrunXu', 'xinrunxu')):
    text = path.read_text(errors='ignore')
    found = [w for w in forbidden if w in text]
    if found:
        raise SystemExit(f'{path.name} 里仍出现 {found}，请先移除再导出')
    return True


if __name__ == '__main__':
    html, count = build_html()
    check_name(html)
    print(f'已生成 {html.relative_to(ROOT)}：{count} 个条目，未出现仓库地址与用户名')
    if '--html' in sys.argv:
        sys.exit()
    pdf = OUT / 'agentic-robotics-reader.pdf'
    subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-pdf-header-footer',
                    f'--print-to-pdf={pdf}', html.as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f'已生成 {pdf.relative_to(ROOT)}：{pdf.stat().st_size // 1024} KB')
