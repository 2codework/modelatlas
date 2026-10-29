"""Deterministic cache keys for same-build entrypoint assets (not an integrity check)."""
import hashlib
import re
from urllib.parse import urlsplit

def pin(output):
    def version(url):
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc or parsed.path.startswith('/'):
            raise ValueError('entrypoint assets must be relative and local: '+url)
        path = output / parsed.path
        if '..' in path.relative_to(output).parts:
            raise ValueError('asset path escapes output')
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        return parsed.path+'?v='+digest
    # Only script src and stylesheet href attributes, never arbitrary content links.
    def tag(match):
        text = match.group(0)
        attribute = 'src' if text.lower().startswith('<script') else 'href'
        return re.sub(r'\b'+attribute+r'="([^"]+)"', lambda m: attribute+'="'+version(m.group(1))+'"', text)
    for name in ['index.html', 'realtime-audio.html', 'creative-learning.html']:
        html_path = output/name
        if not html_path.exists():
            continue
        html = html_path.read_text()
        html = re.sub(r'<script\b[^>]*>|<link\b(?=[^>]*\brel="stylesheet")[^>]*>', tag, html, flags=re.I)
        if name == 'index.html':
            html = re.sub(r'\sdata-data-url="[^"]*"', '', html)
            html = re.sub(r'<html\b', '<html data-data-url="'+version('data.json')+'"', html, count=1)
        html_path.write_text(html)
