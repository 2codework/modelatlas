"""Test-only closed finite stage; not an independent content review.
Old tests receive their exact historical stage only after full new-stage checks.
"""
import copy,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE_SHA='ada2b8832d334eecd6122e152f95af84a2c1eb9e9c61cdfc7dc3b6e81e55b6e6'
GOLDEN_SHA='1946fd50c9c186efa8b8628ed731cf1c05d98ed5f6efbf6bf7e4e7f614c4a7ab'
REGISTRY_SHA='9f1ff5208b4b2683cb77d7532edb71a265b01264737f2d72e17795e4a5de1c06'
def need(ok,msg):
 if not ok:raise ValueError('early NLP closed contract: '+msg)
def fixture(name,sha):
 p=ROOT/'tests/fixtures'/name
 need(hashlib.sha256(p.read_bytes()).hexdigest()==sha,'fixture hash '+name)
 return json.loads(p.read_text())
def baseline():return fixture('early-nlp-baseline.json',BASE_SHA)
def validate(data):
 b=baseline();o=fixture('early-nlp-golden.json',GOLDEN_SHA);r=fixture('early-nlp-registry.json',REGISTRY_SHA)
 need(set(data)==set(b)|{'early_nlp_registry'},'top-level fields')
 for k in b:
  if k in o:
   ids=[x['id'] for x in data[k]]
   need(len(ids)==len(set(ids)),'duplicate '+k)
   need(data[k]==b[k]+o[k],'complete ordered objects '+k)
  else:need(data[k]==b[k],'old complete field '+k)
 need(data['early_nlp_registry']==r,'registry complete object')
 need(tuple(len(data[k]) for k in ('nodes','sources','events','edges'))==(254,405,211,151),'exact counts')
 need(len(data['vendor_catalog']['records'])==77,'catalog count')
 need(sum(bool(e['date']) for e in data['events'])==127,'dated count')
 return data
def legacy_view(data):
 validate(data);return copy.deepcopy(baseline())
