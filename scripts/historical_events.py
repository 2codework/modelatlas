"""Strict non-weight historical-event admission; no fetching or openness inference."""
import datetime
import json
import re
from urllib.parse import urlsplit

SCHEMA = 'modelatlas.typed-historical-events.v1'
KINDS = {'paper', 'paper_revision', 'api_ga_announcement', 'api_availability_announcement', 'model_family_announcement'}
TOP = {'schema', 'checked_at', 'scope', 'events'}
FIELDS = {'id', 'kind', 'title', 'provider', 'version', 'api_alias', 'date', 'timestamp_utc', 'checked_at', 'modalities', 'evidence', 'context_sources', 'summary', 'note', 'first_paper_submission', 'first_public_weights_date', 'pinned_api_revision', 'execution_status'}
EVIDENCE = {'url', 'kind', 'date', 'supports'}
SUPPORTS = {'event_kind', 'event_date', 'event_identity'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def exact(obj, keys, name):
    require(type(obj) is dict and set(obj) == keys, 'invalid fields: ' + name)

def text(value):
    return type(value) is str and bool(value.strip())

def day(value):
    require(type(value) is str and re.fullmatch(r'\d{4}-\d{2}-\d{2}', value), 'invalid day')
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        raise ValueError('invalid calendar day') from None

def bilingual(value):
    exact(value, {'zh', 'en'}, 'bilingual text')
    require(all(text(v) for v in value.values()), 'empty translation')

def url(value):
    require(text(value), 'missing source URL')
    try:
        parsed = urlsplit(value)
        require(parsed.scheme == 'https' and bool(parsed.hostname) and not parsed.username and not parsed.password and not any(c.isspace() for c in value), 'unsafe source URL')
        parsed.port
    except (ValueError, AttributeError):
        raise ValueError('unsafe source URL') from None

def validate(package):
    exact(package, TOP, 'package')
    require(package['schema'] == SCHEMA, 'unsupported schema')
    checked = day(package['checked_at'])
    require(text(package['scope']), 'missing scope')
    require(type(package['events']) is list and bool(package['events']), 'missing events')
    ids = set()
    identities = set()
    for row in package['events']:
        require(type(row) is dict, 'event must be object')
        exact(row, FIELDS | {'family_members'} if row.get('kind') == 'model_family_announcement' else FIELDS, 'event')
        require(text(row['id']) and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', row['id']) and row['id'] not in ids, 'invalid or duplicate event ID')
        ids.add(row['id'])
        require(text(row['kind']) and row['kind'] in KINDS, 'unsupported non-weight event kind')
        require(text(row['provider']) and text(row['version']), 'missing identity')
        require(row['checked_at'] == package['checked_at'], 'check date mismatch')
        require(day(row['date']) <= checked, 'future event')
        for key in ('title', 'summary', 'note'):
            bilingual(row[key])
        require(type(row['modalities']) is list and row['modalities'] and all(type(v) is str for v in row['modalities']) and len(set(row['modalities'])) == len(row['modalities']) and all(v in {'text','image','audio','video','time_series','未登记'} for v in row['modalities']), 'invalid modalities')
        require(row['first_public_weights_date'] is None and row['pinned_api_revision'] is None, 'non-weight event cannot establish weights or pinned API revision')
        require(row['execution_status'] == 'not_executed', 'unsupported execution claim')
        if row['timestamp_utc'] is not None:
            require(type(row['timestamp_utc']) is str and re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z',row['timestamp_utc']), 'invalid UTC timestamp')
            try:
                stamp = datetime.datetime.fromisoformat(row['timestamp_utc'].replace('Z','+00:00'))
            except ValueError:
                raise ValueError('invalid UTC timestamp') from None
            require(stamp.date().isoformat() == row['date'], 'timestamp/date mismatch')
        if row['kind'] == 'paper':
            require(row['api_alias'] is None and row['timestamp_utc'] is not None, 'paper/API identity mismatch')
            require(row['first_paper_submission'] == row['date'], 'first submission date mismatch')
            require(re.fullmatch(r'arXiv:\d{4}\.\d{4,5}v1', row['version']), 'first submission requires pinned arXiv v1')
        elif row['kind'] == 'paper_revision':
            require(re.fullmatch(r'arXiv:\d{4}\.\d{4,5}v(?:[2-9]|[1-9]\d+)', row['version']), 'revision requires pinned arXiv v2 or later')
            require(row['api_alias'] is None and row['timestamp_utc'] is not None, 'paper/API identity mismatch')
            require(day(row['first_paper_submission']) < day(row['date']), 'revision must follow first submission')
        elif row['kind'] == 'model_family_announcement':
            require(row['api_alias'] is None and row['timestamp_utc'] is None and row['first_paper_submission'] is None, 'family announcement cannot borrow API or paper identity/time')
            require(row['context_sources'] == [], 'family announcement cannot borrow API context')
            require(type(row['family_members']) is list and len(row['family_members']) >= 2, 'family requires named members')
            member_names, member_urls = set(), set()
            for member in row['family_members']:
                exact(member, {'name','url','source_url'}, 'family member')
                require(text(member['name']) and member['name'] not in member_names, 'invalid or duplicate family member')
                url(member['source_url'])
                # null means named in the announcement, with no member-specific URL registered.
                if member['url'] is not None:
                    url(member['url'])
                    require(member['url'] not in member_urls, 'duplicate member URL')
                    member_urls.add(member['url'])
                member_names.add(member['name'])
        else:
            require(text(row['api_alias']) and re.fullmatch(r'[a-z0-9-]+',row['api_alias']), 'missing API alias')
            require(row['first_paper_submission'] is None and row['timestamp_utc'] is None, 'API event must not borrow paper time')
        identity = (row['provider'],row['version'],row['kind'],row['date'])
        require(identity not in identities, 'duplicate historical event identity')
        identities.add(identity)
        require(type(row['evidence']) is list and bool(row['evidence']), 'missing evidence')
        seen_urls = set()
        for source in row['evidence']:
            exact(source,EVIDENCE,'evidence')
            url(source['url'])
            require(source['url'] not in seen_urls, 'duplicate evidence URL')
            seen_urls.add(source['url'])
            require(source['kind'] == row['kind'] and source['date'] == row['date'], 'source/event type or date mismatch')
            require(type(source['supports']) is list and len(source['supports']) == 3 and all(type(v) is str for v in source['supports']) and set(source['supports']) == SUPPORTS, 'source must support identity, kind and date')
        if row['kind'] == 'model_family_announcement':
            require(all(m['source_url'] in seen_urls and m['url'] not in seen_urls for m in row['family_members']), 'member linkage must identify event evidence and distinct member URL')
        if row['kind'] == 'paper':
            require('https://arxiv.org/abs/' + row['version'][6:] in seen_urls, 'first submission requires matching pinned evidence')
        if row['kind'] == 'paper_revision':
            require('https://arxiv.org/abs/' + row['version'][6:] in seen_urls, 'revision requires matching pinned evidence')
        require(type(row['context_sources']) is list, 'invalid context sources')
        for source in row['context_sources']:
            exact(source, {'url','role','date'}, 'context source')
            url(source['url'])
            require(text(source['role']) and source['role'] in {'api_alias','later_lifecycle'}, 'invalid context role')
            require(day(source['date']) <= checked, 'future context evidence')
            if source['role'] == 'later_lifecycle':
                require(day(source['date']) > day(row['date']), 'later lifecycle must follow event')
            require(row['kind'] not in {'paper', 'paper_revision'}, 'API context on paper event')
    return package

def load(path):
    def pairs(items):
        obj = {}
        for key,value in items:
            require(key not in obj, 'duplicate JSON key')
            obj[key] = value
        return obj
    def constant(value):
        raise ValueError('non-finite JSON constant')
    return validate(json.loads(path.read_text(),object_pairs_hook=pairs,parse_constant=constant))

def project(package):
    validate(package)
    return [{'id':'historical-'+r['id'], 'title':r['title']['zh'], 'kind':r['kind'], 'date':r['date'], 'precision':'day', 'month':r['date'][:7], 'providers':[r['provider']], 'modalities':r['modalities'][:], 'nodes':[], 'version':r['version'], 'sources':list(dict.fromkeys(e['url'] for e in r['evidence'] + r['context_sources'] + r.get('family_members', []) if e['url'] is not None)), 'checked_at':r['checked_at'], 'summary':r['summary']['zh'], 'note':r['note']['zh'], 'license':[], 'historical_typed':True, 'raw':r} for r in package['events']]

def collect(directory, existing_ids):
    rows = []
    seen = set(existing_ids)
    identities = set()
    for path in sorted(directory.glob('*.json')):
        for row in project(load(path)):
            require(row['id'] not in seen, 'duplicate monthly ID')
            key=(tuple(row['providers']),row['version'],row['kind'],row['date'])
            require(key not in identities, 'duplicate cross-package historical identity')
            seen.add(row['id']); identities.add(key); rows.append(row)
    return rows
