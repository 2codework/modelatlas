"""Finite documented web-feature projection; no network or product execution."""
import copy
import json
import hashlib
import shutil
from pathlib import Path
from urllib.parse import urlsplit

REL = 'learning/chatgpt-images-feature/r1'
PUBLIC_REL = 'chatgpt-images-feature'
NODE_ID = 'creative-chatgpt-web-images'
ADMISSION_SHA = '31aa079b1e7d49a599af219e0a4d60a206a48796405b5333bcd382225a7e6401'
FILES = frozenset({'FEATURE.zh-CN.md', 'PROJECTION.md', 'overlay.json', 'admission.json', 'registry.json'})
SOURCE_IDS = ('cgw-src-generation', 'cgw-src-inputs', 'cgw-src-api-sunburst', 'cgw-src-images-help-reused', 'cgw-src-free-reused', 'cgw-src-regions-reused')

def need(ok, message):
    if not ok:
        raise ValueError('ChatGPT web images: ' + message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def no_symlinks(path, root):
    path, root = Path(path), Path(root)
    need(path.is_relative_to(root), 'path outside root')
    for item in (path, *path.parents):
        need(not item.is_symlink(), 'symlink forbidden: ' + item.name)
        if item == root:
            break
    if path.exists() and path.is_dir():
        need(not any(x.is_symlink() for x in path.rglob('*')), 'nested symlink forbidden')

def load(root):
    p = Path(root) / REL
    no_symlinks(p, Path(root))
    need(p.is_dir(), 'missing projection')
    need({str(x.relative_to(p)) for x in p.rglob('*') if x.is_file()} == FILES, 'closed projection files')
    need(not any(x.is_dir() for x in p.iterdir()), 'unexpected projection directory')
    need(sha(p / 'admission.json') == ADMISSION_SHA, 'admission hash')
    a = json.loads((p / 'admission.json').read_text())
    need(set(a['files_sha256']) == FILES - {'admission.json'}, 'registered file set')
    for name, h in a['files_sha256'].items():
        need(sha(p / name) == h, 'file hash ' + name)
    o = json.loads((p / 'overlay.json').read_text())
    validate_overlay(o)
    for key, values in o.items():
        need([x['id'] for x in values] == a['expected_ids'][key], 'exact admitted IDs ' + key)
        need([digest(x) for x in values] == a['expected_object_sha256'][key], 'exact admitted records ' + key)
    return a, o

def validate_overlay(o):
    need(type(o) is dict and set(o) == {'nodes', 'sources', 'events', 'edges', 'view_nodes'}, 'overlay schema')
    need(all(type(x) is list for x in o.values()), 'array types')
    need(tuple(len(o[k]) for k in ('nodes', 'sources', 'events', 'edges', 'view_nodes')) == (1, 6, 0, 0, 1), 'finite scope')
    n = o['nodes'][0]
    need(n['id'] == NODE_ID and n['type'] == 'application_feature', 'application not model')
    need(all(n.get(k, 'missing') is None for k in ('exact_backend_model', 'first_feature_release_date', 'weights_release_date', 'architecture')), 'unknown backend and dates')
    need(n['runtime_verified'] is False and n['execution_status'] == 'never-run', 'no execution claim')
    need(n['checked_at'] == '2026-10-29' and n['lifecycle_scope'] == 'current_documented_web_feature_as_of_2026-10-29_not_account_availability', 'bounded observation')
    need(n['source_ids'] == [s for s in SOURCE_IDS if s != 'cgw-src-api-sunburst'], 'API not backend evidence')
    need(tuple(s['id'] for s in o['sources']) == SOURCE_IDS, 'source identity')
    for i, s in enumerate(o['sources']):
        u = urlsplit(s['url'])
        need(u.scheme == 'https' and u.hostname in {'learn.chatgpt.com', 'help.openai.com', 'developers.openai.com'} and not u.username and not u.password and not any(c.isspace() for c in s['url']), 'official source URL')
        need(s['checked_at'] == '2026-10-29' and s['evidence_scope'] and s['unknown_boundary'], 'source scope')
        need(s['evidence_mode'] == ('fresh_official_web_read' if i < 3 else 'reused_local_qa_reviewed_official_source_record_not_fresh_web_open'), 'fresh/reused partition')
    need(o['view_nodes'] == [{k: n[k] for k in ('id', 'lifecycle', 'vendor', 'availability', 'license')}], 'display identity')

def preflight(root):
    load(root)
    for folder in ('dist', 'docs'):
        target = Path(root) / folder / PUBLIC_REL
        no_symlinks(target, Path(root))
        if target.exists():
            need(target.is_dir(), 'output not directory')
            need({str(p.relative_to(target)) for p in target.rglob('*') if p.is_file()} <= FILES, 'unregistered output asset')
            need(not any(p.is_dir() for p in target.iterdir()), 'unregistered output directory')

def apply(data, root):
    a, o = load(root)
    need(set(data) == set(a['base_object_sha256']), 'baseline fields')
    for key, value in data.items():
        need(digest(value) == a['base_object_sha256'][key], 'baseline drift ' + key)
    for key in ('nodes', 'sources', 'events', 'edges', 'view_nodes'):
        need([digest(x) for x in data[key]] == a['original_record_sha256'][key], 'historical record drift ' + key)
    need(digest(data['vendor_catalog']) == a['original_catalog_sha256'], 'catalog unchanged')
    for key in ('nodes', 'sources', 'view_nodes'):
        old_ids = [x['id'] for x in data[key]]
        new_ids = [x['id'] for x in o[key]]
        need(len(old_ids) == len(set(old_ids)) and not set(old_ids) & set(new_ids), 'duplicate ID ' + key)
    need(not {s['url'] for s in data['sources']} & {s['url'] for s in o['sources']}, 'new source URL collision')
    for key in ('nodes', 'sources', 'view_nodes'):
        data[key].extend(copy.deepcopy(o[key]))
    for key, count in a['expected_counts'].items():
        need(len(data[key]) == count, 'final count ' + key)
    data['chatgpt_images_feature_registry'] = json.loads((Path(root) / REL / 'registry.json').read_text())
    return data

def publish(root, out):
    preflight(root)
    target = Path(out) / PUBLIC_REL
    no_symlinks(target, Path(root))
    if target.exists():
        need(target.is_dir(), 'publish target not directory')
        need({str(x.relative_to(target)) for x in target.rglob('*') if x.is_file()} <= FILES, 'publish target asset set')
    shutil.copytree(Path(root) / REL, target, dirs_exist_ok=True)
