"""Exact additive images stage; legacy graph is checked before it is returned."""
import copy,hashlib,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE_DATA_SHA='c97ae6a9c72f085eb936c1a0d56b79033a313e6927f1fc9b9b775ec6cf4b8955'
def encoded(d):return (json.dumps(d,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode()
def json_value(value,ancestors=None):
 if value is None or type(value) in (str,bool,int):return
 if type(value) is float:
  if not math.isfinite(value):raise ValueError('non-finite JSON number')
  return
 if type(value) not in (dict,list):raise ValueError('unsupported JSON value')
 if ancestors is None:ancestors=set()
 if id(value) in ancestors:raise ValueError('cyclic JSON value')
 ancestors.add(id(value))
 if type(value) is dict:
  if any(type(k) is not str for k in value):raise ValueError('non-string JSON key')
  items=value.values()
 else:items=value
 for item in items:json_value(item,ancestors)
 ancestors.remove(id(value))
def legacy_view(data):
 json_value(data)
 import sys
 sys.path.insert(0,str(ROOT/'scripts'))
 import chatgpt_images_feature as C
 a,o=C.load(ROOT)
 old=copy.deepcopy(data)
 for k in ('nodes','sources','view_nodes'):
  size=len(o[k])
  if encoded(old[k][-size:])!=encoded(o[k]):raise ValueError('images exact addition '+k)
  old[k]=old[k][:-size]
 old.pop('chatgpt_images_feature_registry',None)
 if hashlib.sha256(encoded(old)).hexdigest()!=BASE_DATA_SHA:raise ValueError('images complete legacy graph mismatch')
 expected=C.apply(copy.deepcopy(old),ROOT)
 if encoded(expected)!=encoded(data):raise ValueError('images complete stage mismatch')
 return old
