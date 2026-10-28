"""Static editorial diagram only. No registry mutation or external dependencies."""
import hashlib, html, json, shutil, xml.etree.ElementTree as ET
REL = 'learning/audio-diagram/r1'
MANIFEST_SHA = '8f59b7a3274f2d1cf6c85bf94f62cf79352db483641eea65dcb131a36f19bf5d'
SVG = 'realtime-audio-four-checks.zh.svg'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(root):
    p = root / REL
    assert sha(p / 'manifest.json') == MANIFEST_SHA, 'diagram manifest drift'
    manifest = json.loads((p / 'manifest.json').read_text())
    assert set(x.name for x in p.iterdir()) == set(manifest) | {'manifest.json'}
    for name, value in manifest.items():
        assert '/' not in name and sha(p / name) == value, 'diagram asset drift'
    svg = (p / SVG).read_text()
    assert '<!DOCTYPE' not in svg and 'url(' not in svg
    tree = ET.fromstring(svg)
    assert all(e.tag.split('}')[-1] in {'svg','g','text','rect','title','desc'} for e in tree.iter())
    assert all(not k.lower().endswith('href') and not k.lower().startswith('on') for e in tree.iter() for k in e.attrib)
    assert tree.attrib['aria-labelledby'] == 'title desc'
    assert {'title','desc'} <= {e.attrib.get('id') for e in tree.iter()}
    content = json.loads((p / 'text-equivalent.json').read_text())
    assert content['ordered_text'] == [e.text for e in tree.iter() if e.tag.endswith('}text')], 'equivalent text drift'
    mapping = json.loads((p / 'source-map.json').read_text())
    raw = json.loads((root / 'learning/realtime-audio/r1/raw/research-r2/raw-models.json').read_text())
    sources = {s['id']:s for s in raw['sources']}
    assert all(s == sources[s['id']] for s in mapping['sources']), 'source mapping drift'
    assert all(set(x['source_ids']) <= {s['id'] for s in mapping['sources']} for x in mapping['panels'])
    return content, mapping

def publish(root, out):
    content, mapping = load(root)
    target = out / 'audio-diagram'
    shutil.copytree(root / REL, target, dirs_exist_ok=True)
    esc = html.escape
    section = ['<section id="audio-learning-diagram" aria-labelledby="audio-learning-diagram-title">', '<h2 id="audio-learning-diagram-title">配图学习：四个问题分别核验</h2>', '<figure style="margin:1rem 0">', '<a href="audio-diagram/' + SVG + '" aria-label="查看实时音频核对图原尺寸"><img src="audio-diagram/' + SVG + '" width="1100" height="1140" style="display:block;width:100%;max-width:1100px;height:auto" alt="' + esc(content['alt'], quote=True) + '"></a>', '<figcaption>' + esc(content['caption']) + ' <a href="audio-diagram/' + SVG + '">查看原尺寸 SVG</a></figcaption>', '</figure>', '<details open><summary>完整文字版（正常字号，可展开或收起）</summary><div style="font-size:1rem;line-height:1.8">']
    section += ['<p>' + esc(t) + '</p>' for t in content['ordered_text']]
    section += ['</div></details><h3>配图官方来源与许可</h3><p><a href="audio-diagram/source-map.json">source_ids 映射（沿用已验收来源，非本次重新联网核验）</a> · <a href="audio-diagram/RIGHTS.zh.md">原创内容与第三方权利边界</a></p><ul>']
    section += ['<li><a href="' + esc(s['url'], quote=True) + '" rel="noopener noreferrer">' + esc(s['id']) + '</a></li>' for s in mapping['sources']]
    section += ['</ul></section>']
    path = out / 'realtime-audio.html'
    original = path.read_text()
    assert original.count('</nav>') == 1
    path.write_text(original.replace('</nav>', '</nav>\n' + '\n'.join(section), 1))
