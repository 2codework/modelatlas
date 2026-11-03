"""Build original bilingual BPE lesson and byte-identical downloadable sources."""
from pathlib import Path
from html import escape
import zipfile
FILES=('core.py','fixtures.py','demo.py','test_core.py','README-zh.md','README-en.md','WORKSHEET-zh.md','WORKSHEET-en.md','REFERENCE-zh.md','REFERENCE-en.md','SOURCES.md')
IDS=('contract','worked','run','transfer','finish')
def prose(text):
 parts=[]
 for block in text.strip().split('\n\n'):
  if all(line.startswith('    ') for line in block.splitlines()):parts.append('<pre><code>'+escape('\n'.join(line[4:] for line in block.splitlines()))+'</code></pre>')
  else:parts.append('<p>'+escape(block).replace('\n','<br>')+'</p>')
 return ''.join(parts)
def render(root):
 source=root/'learning/bpe-tokenizer';web=root/'web'
 with zipfile.ZipFile(web/'tokenization-lab.zip','w',zipfile.ZIP_DEFLATED) as z:
  for name in FILES:
   info=zipfile.ZipInfo('bpe-tokenizer/'+name,(2026,11,2,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(source/name).read_bytes())
 for name in FILES:(web/('tokenization-'+name)).write_bytes((source/name).read_bytes())
 for language in ('zh','en'):
  en=language=='en';suffix='-en' if en else '';title='From characters to token IDs' if en else '从字符到 token ID'
  chunks=(source/f'README-{language}.md').read_text().split('\n## ')
  intro=prose(chunks[0].split('\n',1)[1]);sections=''
  for identity,chunk in zip(IDS,chunks[1:]):
   heading,body=chunk.split('\n',1);sections+=f'<section id="{identity}"><h2>{escape(heading)}</h2>{prose(body)}</section>'
  links=''.join(f'<li><a href="tokenization-{n}">{escape(n)}</a> · <a href="#source-{n}">{"Inspect source" if en else "检查源码"}</a></li>' for n in FILES)
  readers=''.join(f'<details id="source-{n}"><summary>{escape(n)}</summary><pre><code>{escape((source/n).read_text())}</code></pre></details>' for n in FILES)
  reference=escape((source/f'REFERENCE-{language}.md').read_text())
  page=f'''<!doctype html><html lang="{'en' if en else 'zh-CN'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"><title>{title} · ModelAtlas</title><link rel="stylesheet" href="tokenization-lab.css"><script src="tokenization-lab.js" defer></script></head><body><a class="skip" href="#tokenization-main">{'Skip to lesson' if en else '跳至课程'}</a><header><a href="academy{suffix}.html#tokens">ModelAtlas · {'Tokens and attention' if en else '分词与 attention'}</a><nav aria-label="{'Language' if en else '语言'}"><a data-tokenization-language href="tokenization-lab.html">中文</a> · <a data-tokenization-language href="tokenization-lab-en.html">English</a></nav></header><main id="tokenization-main"><p>READ → COUNT → MERGE → ENCODE → EXPLAIN</p><h1>{title}</h1>{intro}<p>{'Language and region are independent. This offline algorithm needs no provider account; navigation preserves a valid selected region only.' if en else '语言与地区独立。离线算法不需要厂商账号；导航只保留有效的明确地区选择。'}</p><nav aria-label="{'Lesson sections' if en else '课程目录'}"><a href="#worked">{'Worked trace' if en else '完整推导'}</a> · <a href="#run">{'Run the source' if en else '实际运行源码'}</a> · <a href="#transfer">{'Independent transfer' if en else '独立迁移'}</a> · <a href="#downloads">{'Downloads' if en else '下载'}</a></nav>{sections}<details id="reference"><summary>{'Reveal transfer reference after your attempt' if en else '独立作答后展开迁移参考'}</summary><pre>{reference}</pre></details><section id="downloads"><h2>{'Complete source packet' if en else '完整源码材料包'}</h2><p><a href="tokenization-lab.zip" download>{'Download standalone Python lab ZIP' if en else '下载可独立运行的 Python 实验 ZIP'}</a></p><ul>{links}</ul>{readers}</section><footer><p>{'Mechanism sources, checked 2026-11-02; original fixtures and implementation, no vendor model execution.' if en else '机制来源核对于2026-11-02；语料与实现原创，未运行厂商模型。'} <a href="https://huggingface.co/learn/llm-course/en/chapter6/5">Hugging Face · BPE</a> · <a href="https://arxiv.org/abs/1508.07909">Sennrich et al. · Subword units</a></p><a href="attention-lab{suffix}.html">{'Next: compute attention →' if en else '下一步：计算 attention →'}</a></footer></main></body></html>'''
  (web/f'tokenization-lab{suffix}.html').write_text(page)
if __name__=='__main__':render(Path(__file__).resolve().parents[1])
