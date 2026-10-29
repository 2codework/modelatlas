"""Self-authored finite stage contract, not independent content QA.
Return old stage only after exact full new-stage validation; never truncate blindly.
"""
import copy,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def fixture(name,sha):
 p=ROOT/'tests/fixtures'/name
 if hashlib.sha256(p.read_bytes()).hexdigest()!=sha:raise ValueError('runtime fixture hash')
 return json.loads(p.read_text())
def baseline():return fixture('runtime-baseline.json','08bfa349e52cdb40d382765db007559bf8b48218c38258168ebdc656155e6d21')
def golden():return fixture('runtime-golden.json','2c41d29f1313c3c5afc66062fbab01fab82a5f6d713ddd3c5543a77a9a15a89a')
def registry():return fixture('runtime-registry.json','fbe74aefff276896a454e1d8ee4ff01706d1886e9e5cd726e78f83aeac2ff768')
def validate(data):
 b=baseline();o=golden();expected=copy.deepcopy(b)
 for k in o:expected[k]+=o[k]
 expected['inference_runtime_registry']=registry()
 # Serialized canonical equality is type-sensitive (False is not zero).
 dump=lambda v:json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
 if dump(data)!=dump(expected):raise ValueError('runtime complete stage mismatch')
 return data
def legacy_view(data):validate(data);return copy.deepcopy(baseline())
