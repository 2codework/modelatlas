import json
from core import train, encode, decode
from fixtures import WORKED
model, trace = train(WORKED, 2)
before = repr(model)
encoded = {s: list(encode(model, s)) for s in ('abab','abac','ababc')}
print(json.dumps({'corpus': WORKED, 'vocabulary': model.vocabulary, 'merges': model.merges,
 'trace': trace, 'encoded': encoded, 'roundtrips': {s: decode(model, ids) for s,ids in encoded.items()},
 'frozen_tokenizer_unchanged': before == repr(model)}, ensure_ascii=False, indent=2))
