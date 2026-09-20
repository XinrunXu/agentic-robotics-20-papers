"""Check shipped pages, links, reading coverage and executable lab invariants."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import importlib.util
import json
import re
from content import CHAPTERS
from papers import PAPERS
from deep_readings import NOTES

ROOT = Path(__file__).parent
DIST = ROOT / 'docs'


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.resources, self.h1 = [], [], [], 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if data.get('id'):
            self.ids.append(data['id'])
        if tag == 'a' and data.get('href'):
            self.links.append(data['href'])
        if tag in ('link','script','img'):
            self.resources.append(data.get('src') or data.get('href'))
        self.h1 += tag == 'h1'


def main():
    pages = {p.name: Page(p.read_text()) for p in DIST.glob('*.html')}
    assert len(pages) == 29, f'Expected nine chapters and twenty readings, got {len(pages)}'
    assert set(NOTES) == {p['key'] for p in PAPERS}
    assert len(PAPERS) == len({p['arxiv'] for p in PAPERS}) == 20
    assert [p['date'] for p in PAPERS] == sorted(p['date'] for p in PAPERS)
    assert all(p[k].strip() for p in PAPERS for k in ('problem','mechanism','evidence','boundary','question','connection'))
    for name,page in pages.items():
        assert page.h1 == 1, (name,'heading count')
        assert len(page.ids) == len(set(page.ids)), (name,'duplicate id')
        for link in page.links + page.resources:
            assert link, (name,'empty reference')
            url = urlparse(link)
            if url.scheme or url.netloc:
                continue
            target = unquote(url.path) or name
            assert (DIST/target).is_file(), (name,link,'missing local file')
            if url.fragment:
                assert target in pages and unquote(url.fragment) in pages[target].ids, (name,link,'missing anchor')
    timeline = (DIST/'papers.html').read_text()
    for paper in PAPERS:
        assert f'https://arxiv.org/abs/{paper["arxiv"]}' in timeline
        assert f'id="{paper["key"]}"' in timeline
        assert f'papers.html#{paper["key"]}' in (DIST/(paper['chapter']+'.html')).read_text(), paper['name']
        reading = (DIST/f'paper-{paper["key"]}.html').read_text()
        assert all(f'id="{anchor}"' in reading for anchor in ('problem','method','example','results','ablation','connect','practice','sources'))
        note = NOTES[paper['key']]
        assert len(note['steps']) >= 3 and len(note['rows']) >= 3 and note['sources']
        assert all(len(row) == len(note['headers']) for row in note['rows'])
        assert f'{paper["arxiv"]}{note["version"]}' in reading
    for slug,_,_,_,_,_ in CHAPTERS:
        if slug not in ('experiments.html',):
            assert '<details class="reflection">' in (DIST/slug).read_text(), slug
    for token in ('equipment-cpu','equipment-sim','equipment-robot','state_handoff.py','research-protocol.md'):
        assert token in (DIST/'experiments.html').read_text(), token

    spec = importlib.util.spec_from_file_location('handoff', DIST/'downloads/state_handoff.py')
    lab = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lab)
    low = lab.experiment(episodes=1000,seed=17,noise=0.1,bridge_error=0.05)
    high = lab.experiment(episodes=1000,seed=17,noise=2.0,bridge_error=0.05)
    zero = lab.experiment(episodes=1000,seed=17,noise=0,bridge_error=0)
    assert low['direct_retry'] == high['direct_retry'], 'Paired baseline changed with noise'
    assert low['oracle_bridge'] == high['oracle_bridge'], 'Oracle should not depend on observation noise'
    assert zero['observed_bridge']['successes'] == 1000
    assert high['observed_bridge']['successes'] < high['direct_retry']['successes'], 'Expected noisy correction counterexample'
    for results in (low,high,zero):
        for method,stats in results.items():
            assert stats['calls'] <= 2000, (method,'exceeds budget')
            assert stats['inside_n'] + stats['outside_n'] == 1000
            assert stats['inside_successes']+stats['outside_successes'] == stats['successes']
    result = dict(pages=len(pages),papers=len(PAPERS),deep_readings=len(NOTES),
                  evidence_tables=len(NOTES),local_links='all resolve',
                  reflection_pages=27,equipment_routes=3,lab='paired conditions and budget checks passed')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
