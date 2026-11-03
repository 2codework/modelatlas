"""Build original bilingual retrieval lesson and self-contained source ZIP."""
from pathlib import Path
from html import escape
import zipfile

FILES=('core.py','fixtures.py','demo.py','test_core.py','README-zh.md','README-en.md','REFERENCE-zh.md','REFERENCE-en.md','SOURCES.md')
IDS=('prepare','materials','worked','run','safety','evaluate','transfer','finish')

def markdown(text):
    # Controlled original Markdown subset; escaped code/text, no raw HTML execution.
    out=[]; in_code=False; section=0
    for line in text.splitlines():
        if line.startswith('# '):continue
        if line.startswith('```'):
            out.append('</code></pre>' if in_code else '<pre><code>');in_code=not in_code
        elif in_code:out.append(escape(line)+'\n')
        elif line.startswith('## '):
            if section:out.append('</section>')
            out.append(f'<section id="{IDS[section]}"><h2>{escape(line[3:])}</h2>');section+=1
        elif line:out.append('<p>'+escape(line)+'</p>')
    if section:out.append('</section>')
    return '\n'.join(out)

def render(root):
    lab=root/'learning/retrieval-lab';web=root/'web'
    with zipfile.ZipFile(web/'retrieval-lab.zip','w',zipfile.ZIP_DEFLATED) as z:
        for name in FILES:
            info=zipfile.ZipInfo('retrieval-lab/'+name,(2026,11,2,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,(lab/name).read_bytes())
    for lang in ('zh','en'):
        en=lang=='en';suffix='-en' if en else ''
        title='From source text to verifiable citations' if en else '从原文到可核对的引用'
        body=markdown((lab/f'README-{lang}.md').read_text())
        readers=''.join(f'<details id="source-{name}"><summary>{escape(name)}</summary><pre><code>{escape((lab/name).read_text())}</code></pre></details>' for name in FILES)
        ref=escape((lab/f'REFERENCE-{lang}.md').read_text())
        html=f'''<!doctype html><html lang="{'en' if en else 'zh-CN'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"><title>{title} · ModelAtlas</title><link rel="stylesheet" href="tiny-training.css"><script src="retrieval-lab.js" defer></script></head><body><a class="skip" href="#retrieval-main">{'Skip to lesson' if en else '跳至课程'}</a><header><a href="academy{suffix}.html#project">ModelAtlas · {'QA Agent project' if en else '资料问答项目'}</a><nav aria-label="{'Language' if en else '语言'}"><a data-retrieval-language href="retrieval-lab.html">中文</a> · <a data-retrieval-language href="retrieval-lab-en.html">English</a></nav></header><main id="retrieval-main"><p>READ → CHUNK → RETRIEVE → VERIFY → REVIEW</p><h1>{title}</h1><p>{'Original offline retrieval lab. Language and region are independent; no regional service is required.' if en else '原创离线检索实验。语言与地区独立，不依赖某地区服务。'}</p><nav aria-label="{'Lesson sections' if en else '课程目录'}"><a href="#worked">{'Worked example' if en else '完整推导'}</a> · <a href="#run">{'Run' if en else '运行'}</a> · <a href="#transfer">{'Transfer' if en else '独立迁移'}</a> · <a href="#downloads">{'Downloads' if en else '下载'}</a></nav>{body}<details id="reference"><summary>{'Reveal transfer reference after attempting' if en else '独立作答后展开迁移参考'}</summary><pre>{ref}</pre></details><section id="downloads"><h2>{'Complete source and materials' if en else '完整源码与材料'}</h2><p><a href="retrieval-lab.zip" download>{'Download 9-file Python lab ZIP' if en else '下载9文件Python实验包'}</a></p><p>{'Inspect every source below before running. The website never executes submitted code.' if en else '先查看下方全部源码再运行；网站不执行提交代码。'}</p>{readers}</section><footer><p>{'Method sources, checked 2026-11-02' if en else '方法来源，编辑核查2026-11-02'}: <a href="https://arxiv.org/abs/2005.11401">RAG original paper</a> · <a href="https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview">Microsoft RAG overview</a>. {'Exact dates and limits are in SOURCES.md above; no vendor model was run.' if en else '精确日期和限制见上方SOURCES.md，未运行厂商模型。'}</p><a href="academy{suffix}.html#evaluation">{'Continue to evaluation →' if en else '继续学习评测 →'}</a></footer></main></body></html>'''
        (web/f'retrieval-lab{suffix}.html').write_text(html)

if __name__=='__main__':render(Path(__file__).resolve().parents[1])
