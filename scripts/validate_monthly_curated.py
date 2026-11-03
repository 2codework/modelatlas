"""Structural admission checks only; these do not establish source truth or legal status."""
from datetime import date
from urllib.parse import urlsplit
import json
from pathlib import Path

def valid_url(value):
    if not isinstance(value, str): return False
    try:
        parsed = urlsplit(value)
        return parsed.scheme in ('http', 'https') and bool(parsed.hostname) and not parsed.username and not parsed.password
    except ValueError: return False

def validate(package):
    rows = package.get('events', package.get('records'))
    if not isinstance(rows, list) or not rows: raise ValueError('需要非空发布记录列表')
    seen = set()
    for r in rows:
        rid = r.get('id')
        if not isinstance(rid, str) or not rid.strip() or rid in seen: raise ValueError('记录 ID 缺失或重复')
        seen.add(rid)
        if not (r.get('name') or r.get('model_name')) or not (r.get('vendor') or r.get('provider')): raise ValueError(rid + ': 缺少型号或发布机构')
        checked = r.get('verified_on') or package.get('verified_on') or package.get('as_of')
        try: checked_date = date.fromisoformat(checked)
        except (TypeError, ValueError): raise ValueError(rid + ': 核验日期无效') from None
        evidence = r.get('evidence', [])
        if not evidence or any(not valid_url(s.get('url')) for s in evidence): raise ValueError(rid + ': 来源入口缺失或不安全')
        weights = r.get('weight_entries') or ([r['official_weights_url']] if r.get('official_weights_url') else [])
        if not weights or any(not valid_url(u) for u in weights): raise ValueError(rid + ': 权重入口缺失或不安全')
        licenses = r.get('licenses') or ([r['license']] if r.get('license') else [])
        if not licenses or any(not l.get('name') or not valid_url(l.get('url')) for l in licenses): raise ValueError(rid + ': 许可名称或来源缺失')
        for key in ('announcement_date', 'weights_release_date', 'paper_date', 'code_release_date'):
            value = r.get(key)
            if value is None: continue
            try: parsed = date.fromisoformat(value)
            except (TypeError, ValueError): raise ValueError(rid + ': 日期格式无效: ' + key) from None
            if parsed > checked_date: raise ValueError(rid + ': 不把核验日之后的计划当已发生事件')
        if r.get('weights_release_date') and not any('weights_release_date' in e.get('supports', []) for e in evidence): raise ValueError(rid + ': 权重日期未关联证据')
    return len(rows)

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1] / 'curated/monthly'
    count = sum(validate(json.loads(p.read_text())) for p in sorted(root.glob('*.json')))
    print(f'结构检查通过：{count} 条补录。此检查不替代事实和许可核验。')
