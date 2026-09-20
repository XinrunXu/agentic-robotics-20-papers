"""把每篇论文的框图 / 方法图从 arXiv 下载到 docs/figures/。

用法：python3 fetch_figures.py [key ...]        不带参数则检查全部 20 篇，
已存在的文件默认跳过，加 --force 重新下载。图片版权归论文作者，本脚本只记录来源。
"""
import sys
import urllib.request
from pathlib import Path
from figures import FIGURES, local_file, remote_url

DEST = Path(__file__).parent / 'docs' / 'figures'
UA = 'Mozilla/5.0 (compatible; agentic-robotics-reader figure fetcher)'

def fetch(key, force=False):
    DEST.mkdir(parents=True, exist_ok=True)
    target = DEST / local_file(key)
    if target.is_file() and not force:
        return f'{key:<17} skip   {target.stat().st_size/1024:8.0f} KB  {target.name}'
    url = remote_url(key)
    request = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
        kind = response.headers.get('Content-Type', '')
    if not kind.startswith('image/'):
        raise SystemExit(f'{key}: 返回的不是图片（{kind}） {url}')
    target.write_bytes(data)
    return f'{key:<17} saved  {len(data)/1024:8.0f} KB  {target.name}'

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    force = '--force' in sys.argv
    for key in args or FIGURES:
        print(fetch(key, force))
