"""Bilingual source-reading lesson; original fictional transfer, never executes a model."""
from pathlib import Path
from html import escape
import re

TRANSFER = {
'zh': {
 'title':'4．独立迁移：同名任务，是否同一条件？',
 'intro':'先离开上面的 BAGEL 答案。以下是原创虚构记录卡，没有真实厂商、运行日志或成绩；编号和版本仅用于纸面练习。不要把它们录入模型目录。',
 'cards':[
 ('T-A','教学模型 Cedar-r1；教学数据 LedgerQA-v1 / Full（100题）；程序 harness-h1；提示 p1；一次输出；精确匹配准确率；同一虚构运行环境 e1。以上是题设字段，不是运行证据。'),
 ('T-B','与 T-A 其他题设字段相同，但子集为 LedgerQA-v1 / Hard（20题）。没有任何成绩或原始输出。'),
 ('T-C','数据为 LedgerQA-v1 / Full（100题），提示、输出次数、指标与环境同 T-A；模型仅写滚动别名 Cedar-latest，具体快照未知；程序版本未知。没有任何成绩或原始输出。')],
 'task':'独立写两条比较决定：T-A 与 T-B 是否能直接作同条件模型排名？T-A 与 T-C 是否已确认条件相同？每条都写：判断、卡片字段证据、缺什么、未补齐前的处理。再写两句不排名的结论。题设相同也不证明真实实验执行。',
 'r1title':'做完再看：T-A / T-B 参考',
 'r1':'不能直接作同条件模型排名。明确差异是 Full / Hard 子集及100 / 20题，不应把两者合并成同一测试；两卡模型甚至相同。先固定同一数据修订与子集、题目范围和计分聚合，再索取对应输出与运行记录。现有卡片只支持识别条件差异，没有性能结论。',
 'r2title':'做完再看：T-A / T-C 参考',
 'r2':'条件是否相同仍未知。Full 相同不足以弥补 Cedar-latest 未固定快照和 harness 版本缺失。需要别名在该次运行时对应的模型修订、程序提交与配置及输出记录，不能照抄 T-A 的版本补空。当前停止直接比较，不能推断 C 更强、较弱或等同。',
 'check':'迁移验收：两条决定各有具体字段依据；区分“已知不同”和“未知是否相同”；各列至少一项缺失证据和暂缓动作；没有虚构分数、假装独立复现或把题设当日志。四项全满足才完成本练习的人工自查，不代表掌握认证。',
 'nav':'4．独立迁移练习', 'finish':'5．验收与停止',
 'review':'原摘记核验：2026-10-31；本轮对上述两处官方页面重新读取：2026-11-01。重读确认这些定位内容仍可见，不固定历史提交、不证明实验执行。学习者未亲自核验时应写“未独立核验”，不要继承编辑日期。',
 'download':'下载空白 Markdown 模板', 'reference':'做完再下载参考与迁移自查',
 'back':'返回核心课：08 · 评测与方法', 'language':'English', 'region':'地区上下文仅用于返回课程，不改变证据与判断；语言不代表地区或服务可用性。',
 'accept':'还需交付 T-A/T-B 与 T-A/T-C 两条独立比较决定，并完成迁移四项人工自查。'},
'en': {
 'title':'4. Independent transfer: same task, same conditions?',
 'intro':'Set aside the BAGEL answers. These original fictional cards contain no real vendor, execution logs or scores. IDs and versions are paper-exercise labels; do not add them to a model catalog.',
 'cards':[
 ('T-A','Teaching model Cedar-r1; teaching data LedgerQA-v1 / Full (100 items); harness-h1; prompt p1; one output; exact-match accuracy; fictional environment e1. These are stipulated fields, not execution evidence.'),
 ('T-B','All other stipulated fields match T-A, but the subset is LedgerQA-v1 / Hard (20 items). No scores or raw outputs are supplied.'),
 ('T-C','LedgerQA-v1 / Full (100 items), with prompt, output count, metric and environment as in T-A. The model is only the rolling alias Cedar-latest, exact snapshot unknown; harness version unknown. No scores or raw outputs are supplied.')],
 'task':'Independently decide: can T-A versus T-B support a same-condition model ranking? Are T-A and T-C confirmed to use identical conditions? For each, write a decision, supporting card fields, missing evidence and what to defer. Finish with two non-ranking sentences. Matching stipulated fields would not prove that a real experiment ran.',
 'r1title':'After your attempt: T-A / T-B reference',
 'r1':'No same-condition model ranking is supported. Full versus Hard and 100 versus 20 items are known differences; do not merge them into one test. The stated model is even the same. Align the dataset revision, subset, item scope and aggregation, then request corresponding outputs and run records. The cards reveal a condition difference, not performance.',
 'r2title':'After your attempt: T-A / T-C reference',
 'r2':'Whether conditions match remains unknown. Full does not resolve the unpinned Cedar-latest snapshot or missing harness version. Request the alias-to-revision mapping for that run, program commit, configuration and outputs. Do not copy T-A versions into the gaps. Defer comparison; C is not established as better, worse or equivalent.',
 'check':'Transfer review: cite concrete fields for both decisions; distinguish known difference from unknown equivalence; name missing evidence and a deferral action for each; invent no score, independent reproduction or execution log. Meeting all four completes this manual exercise check, not a mastery certification.',
 'nav':'4. Independent transfer', 'finish':'5. Review and stop',
 'review':'Original editorial check: 2026-10-31. The two official pages above were reread on 2026-11-01; the cited content remains visible. This does not pin a historical commit or establish execution. Unless you open and check sources yourself, record “not independently checked”; do not inherit the editor date.',
 'download':'Download blank Markdown template', 'reference':'After your attempt: download references and transfer review',
 'back':'Return to core chapter 08 · Evaluation & Methods', 'language':'中文', 'region':'Region context is only carried back to the course; it does not change evidence or decisions. Language implies neither region nor service availability.',
 'accept':'Also deliver the T-A/T-B and T-A/T-C independent decisions and complete the four-part manual transfer review.'}
}

def render(root):
 for lang,c in TRANSFER.items():
  suffix='-en' if lang=='en' else ''
  other='' if lang=='en' else '-en'
  text=(root/'learning/benchmark-practice'/f'lesson-{lang}.html').read_text()
  text=text.replace("script-src 'none'", "script-src 'self'").replace('</head>','<script src="benchmark-practice.js" defer></script></head>')
  nav=f'<div class="benchmark-nav"><a href="academy{suffix}.html#evaluation">{c["back"]}</a><a data-benchmark-language href="benchmark-practice{other}.html">{c["language"]}</a></div><p class="benchmark-context">{c["region"]}</p>'
  text=text.replace('<p class="eyebrow">',nav+'<p class="eyebrow">',1)
  old='4．验收与停止' if lang=='zh' else '4. Review and stop'
  text=text.replace(old,c['finish'])
  text=text.replace('<a href="#finish">',f'<a href="#transfer">{c["nav"]}</a><a href="#finish">',1)
  transfer=f'<section id="transfer"><h2>{c["title"]}</h2><p class="caution">{c["intro"]}</p>'
  transfer+=''.join(f'<div class="material-card" id="{ident.lower()}"><h3>{ident}</h3><p>{body}</p></div>' for ident,body in c['cards'])
  transfer+=f'<p>{c["task"]}</p><details><summary>{c["r1title"]}</summary><p>{c["r1"]}</p></details><details><summary>{c["r2title"]}</summary><p>{c["r2"]}</p></details><p>{c["check"]}</p></section>'
  text=text.replace('<section id="finish">',transfer+'<section id="finish">')
  text=text.replace(f'<h2>{c["finish"]}</h2>',f'<h2>{c["finish"]}</h2><p><strong>{c["accept"]}</strong></p>')
  text=text.replace('<section id="worksheet">',f'<p class="material-card">{c["review"]}</p><section id="worksheet">')
  worksheet=re.search(r'<pre class="worksheet"[^>]*>(.*?)</pre>',text,re.S).group(1)
  downloads=f'<p><a href="benchmark-ledger-template{suffix}.md" download>{c["download"]}</a></p>'
  text=text.replace('</pre>', '</pre>'+downloads,1)
  refs=re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>',text,re.S)
  reference='\n\n'.join('## '+re.sub('<[^>]+>','',title)+'\n\n'+re.sub('<[^>]+>','',body) for title,body in refs)
  reference+='\n\n'+c['check']+'\n\n'+c['review']
  # Reference download appears inside the final collapsed answer, not beside the blank worksheet.
  pos=text.rfind('</details>')
  text=text[:pos]+f'<p><a href="benchmark-ledger-reference{suffix}.md" download>{c["reference"]}</a></p>'+text[pos:]
  extra=('\n\n独立迁移：T-A / T-B 与 T-A / T-C\n每条填写：判断 / 卡片字段 / 缺失证据 / 暂缓动作\n两句不排名的结论：\n' if lang=='zh' else '\n\nIndependent transfer: T-A / T-B and T-A / T-C\nFor each: decision / card fields / missing evidence / deferral action\nTwo non-ranking conclusion sentences:\n')
  sources=('\n\n## 来源与完整题设\n\n' if lang=='zh' else '\n\n## Sources and full exercise\n\n')
  sources+='- A · BAGEL README · News / June 15, 2025: https://github.com/ByteDance-Seed/Bagel/blob/main/README.md\n'
  sources+='- B · BAGEL EVAL · KRIS / RISE Evaluation; RISE Results: https://github.com/ByteDance-Seed/Bagel/blob/main/EVAL.md\n'
  sources+=f'- [{"完整课程与虚构迁移卡" if lang=="zh" else "Full lesson and fictional transfer cards"}](benchmark-practice{suffix}.html)\n'
  (root/'web'/f'benchmark-ledger-template{suffix}.md').write_text('# '+('评测阅读空模板' if lang=='zh' else 'Blank evaluation-reading ledger')+'\n\n'+worksheet+extra+'\n'+c['review']+sources+'\n')
  (root/'web'/f'benchmark-ledger-reference{suffix}.md').write_text('# '+('评测阅读参考：先独立作答' if lang=='zh' else 'Evaluation-reading references: attempt independently first')+'\n\n'+reference+sources+'\n')
  (root/'web'/f'benchmark-practice{suffix}.html').write_text(text)
if __name__=='__main__': render(Path(__file__).resolve().parents[1])
