"""Project the explicit D presentation delta out of historical byte contracts.

Only the added theme link/body marker and brand casing are removed. Every lesson,
source, restriction, interaction and prior asset hash still has to match the old
fixed digest. The new theme and cache hashes have their own positive contracts.
"""
import re

def before_campus(html):
    html, count = re.subn(r'<link rel="stylesheet" href="campus\.css(?:\?v=[a-f0-9]{64})?">', '', html)
    assert count == 1, 'expected exactly one campus stylesheet'
    body = '<body class="campus" data-site="modelatlas">'
    assert html.count(body) == 1, 'unexpected reader body marker'
    html = html.replace(body, '<body>')
    brand = '<a class="brand" href="index.html">ModelAtlas</a>'
    assert html.count(brand) == 1, 'unexpected reader brand'
    return html.replace(brand, '<a class="brand" href="index.html">MODEL ATLAS</a>')
