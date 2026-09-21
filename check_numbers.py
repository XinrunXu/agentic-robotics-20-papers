"""核对精读里的数字是否能在原文中对上。

arXiv 的 LaTeXML 输出把公式同时写成 MathML 结构与 alttext，纯文本提取会把数字
写两遍（$1$ mm → “11 mm”）。这里先用 alttext 替换整个 <math> 子树重新提取一遍，
再检查精读里用到的数字能否在修正后的原文里找到。

缓存缺失时先跑 `python3 research_sources.py`（主线）或按 arXiv HTML 手动补
`.research/x-<key>.html`（补充阅读）。报出“对不上”不等于写错：讲义自己算出的
差值、换算成百分比的小数、以及出现在提醒句里的数字都会被标出来，需要人工判断。
"""
import html as htmllib
import re
import sys
from pathlib import Path

REPO = Path(__file__).parent
sys.path.insert(0, str(REPO))
from research_sources import Text
from deep_readings import NOTES
from extra_readings import EXTRA_NOTES
from papers import PAPERS
from extra_papers import EXTRA_PAPERS

CACHE = REPO / '.research'
MATH = re.compile(r'<math[^>]*?alttext="([^"]*)"[^>]*>.*?</math>', re.S)
NUM = re.compile(r'\d+(?:\.\d+)?')

def fixed_text(path):
    raw = path.read_text(errors='ignore')
    raw = MATH.sub(lambda m: ' ' + htmllib.unescape(m.group(1)) + ' ', raw)
    p = Text(); p.feed(raw)
    return ' '.join(''.join(p.chunks).split())

def numbers(value):
    if isinstance(value, str):
        return NUM.findall(value)
    if isinstance(value, (list, tuple)):
        return [n for v in value for n in numbers(v)]
    return []

def audit(label, note, cache_file):
    path = CACHE / cache_file
    if not path.is_file():
        return f'{label:<15} 缺少缓存 {cache_file}'
    text = fixed_text(path)
    missing = []
    for field in ('result', 'rows', 'findings', 'ablation', 'setup'):
        for n in set(numbers(note.get(field, ''))):
            if len(n) < 2 or n in ('20', '2026', '2025'):   # 跳过太短与年份
                continue
            if n not in text:
                missing.append(f'{field}:{n}')
    return f'{label:<15} {"对不上 " + ", ".join(sorted(set(missing))) if missing else "全部数字可对上"}'

if __name__ == '__main__':
    print('=== 主线')
    for p in PAPERS:
        print(' ', audit(p['key'], NOTES[p['key']], f"{p['key']}.html"))
    print()
    print('=== 补充阅读')
    for p in EXTRA_PAPERS:
        print(' ', audit(p['key'], EXTRA_NOTES[p['key']], f"x-{p['key']}.html"))
