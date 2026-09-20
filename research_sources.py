"""Cache public primary sources for editorial verification; never shipped."""
from pathlib import Path
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor
import urllib.request
from papers import PAPERS
from deep_readings import NOTES

# 精读引用的版本就是要缓存的版本，避免两处各记一份
VERSIONS = {key: int(note['version'].lstrip('v')) for key, note in NOTES.items()}
CACHE = Path(__file__).parent / '.research'
CACHE.mkdir(exist_ok=True)

class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.chunks=[]; self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.skip += 1
        if tag in ('p','div','tr','h1','h2','h3','h4','figcaption','li','section'): self.chunks.append('\n')
        if tag in ('td','th'): self.chunks.append(' | ')
        d=dict(attrs)
        if d.get('id') and (tag in ('section','figure','table') or 'table' in d.get('class','')): self.chunks.append('\n['+d['id']+'] ')
        if tag == 'img': self.chunks.append(' [IMAGE '+d.get('src','')+'] ')
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.skip -= 1
        if tag in ('p','tr','h1','h2','h3','h4','figcaption','li'): self.chunks.append('\n')
    def handle_data(self, data):
        if not self.skip: self.chunks.append(data)

def fetch(p):
    key=p['key']; ver=VERSIONS[key]
    url=f'https://arxiv.org/html/{p["arxiv"]}v{ver}'
    target=CACHE/(key+'.html')
    try:
        if not target.exists(): target.write_bytes(urllib.request.urlopen(url,timeout=60).read())
        parser=Text(); parser.feed(target.read_text())
        lines=[' '.join(line.split()) for line in ''.join(parser.chunks).splitlines() if line.strip()]
        (CACHE/(key+'.txt')).write_text('\n'.join(lines))
        return f'{key}: {len(lines)} lines {url}'
    except Exception as e: return f'{key}: ERROR {e}'

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(fetch,PAPERS): print(result,flush=True)
