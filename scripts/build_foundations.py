"""Render accepted original paper exercises without changing the research graph or progress schema."""
import json, hashlib
import foundation_self_checks
from pathlib import Path
from html import escape
from urllib.parse import urlsplit
SOURCE_SHA='8c8fe93cac66423d12bea51f03d1e110bd056a8e6f21be79d234cf1b7ada1053'
def render(root):
 source=root/'learning/foundations/r2/lessons.json'
 assert hashlib.sha256(source.read_bytes()).hexdigest()==SOURCE_SHA,'foundation source changed without admission'
 data=json.loads(source.read_text());h=lambda x:escape(str(x),quote=True)
 lessons=data['lessons']; sources={s['id']:s for s in data['sources']}
 nav=''.join(f'<a href="#{h(l["id"])}"><span>{i:02}</span>{h(l["title"])}</a>' for i,l in enumerate(lessons,1))
 head='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'"><meta name="description" content="六节有例子、纸面练习和答案的大模型零基础导读；无需账号、代码或付费。"><title>零基础六课 · ModelAtlas</title><link rel="stylesheet" href="foundations.css"><script src="foundations.js" defer></script><script src="foundation-self-checks.js" defer></script></head><body><a class="skip" href="#course-main">跳至正文</a><aside><a class="course-brand" href="index.html">M◎DEL ATLAS<small>零基础阅读室</small></a><nav aria-label="六课目录">'''+nav+'''</nav><a class="back-map" href="foundations.html">六课导读说明</a><a class="back-map" href="index.html">← 返回知识地图</a><a class="back-map" href="BOOK.md">完整技术书稿 ↗</a></aside><main id="course-main"><p id="course-status" role="status" aria-live="polite"></p><header id="course-intro"><p class="kicker">FOUNDATIONS / 从常识开始</p><h1>先理解，再动手。</h1><p>六个小问题，建立大模型与 Agent 的基本判断。</p><div class="course-contract"><strong>无需账号、代码或付费</strong><span>你会带走：术语区分、任务契约和一份可核对的纸面草稿。</span><span>常识导读 → 原创新例 → 纸面练习 → 答案理由</span></div><p class="boundary">'''+h(data['scope'])+''' 不以阅读次数或练习答案宣称掌握，不写入原知识节点的已读进度。</p><p class="admission">六课内容已于 2026-10-29 通过独立来源与纸面推演审查；不是模型、SDK、产品效果或浏览器实测。<a href="foundations-source.json">原始课程记录</a>与本次接纳范围分开保留，不将内容审查改写为执行证据。</p></header>'''
 parts=[head]
 for i,l in enumerate(lessons):
  parts.append(f'<article id="{h(l["id"])}"><div class="lesson-number">第 {i+1:02} 课 / 06 · 常识导读</div><h2>{h(l["title"])}</h2><p class="lesson-status">作者原创合成 · 纸面练习 · 无真实模型或 Agent 执行</p>')
  for label,text in l['sections'].items():
   if label=='答案理由':parts.append(f'<details class="answer"><summary>完成纸面练习后，展开答案与理由</summary><p>{h(text)}</p></details>')
   else:parts.append(f'<section class="{ "exercise" if label=="纸面练习" else "lesson-section" }"><h3>{h(label)}</h3><p>{h(text)}</p></section>')
  parts.append(foundation_self_checks.render(i,l['id']))
  parts.append('<details class="evidence"><summary>来源、适用范围与技术延伸</summary><p>以下来源支持概念依据；例子、练习与答案是作者原创，不是来源中的实测结果。</p><ul>')
  for sid in l['source_ids']:
   s=sources[sid];assert urlsplit(s['url']).scheme=='https'
   parts.append(f'<li><a href="{h(s["url"])}" target="_blank" rel="noopener noreferrer">{h(s["claim"])} ↗</a><small>来源核验：{h(s["checked_at"])}</small></li>')
  nid=l['next_node_id'];assert all(c.isalnum() or c in '-_' for c in nid)
  parts.append(f'</ul><p><a href="index.html?node={h(nid)}">深入技术节点与登记先修 →</a> 技术节点比本课更深，可能需要另读先修。</p></details><nav class="lesson-next" aria-label="第{i+1}课前后导航">')
  if i:parts.append(f'<a href="#{h(lessons[i-1]["id"])}">← 上一课</a>')
  if i+1<len(lessons):parts.append(f'<a class="next" href="#{h(lessons[i+1]["id"])}">下一课：{h(lessons[i+1]["title"])} →</a>')
  else:parts.append('<a class="next" href="index.html?view=learn">继续技术学习路线 →</a>')
  parts.append('</nav></article>')
 parts.append('<noscript>六课全文在下方可直接阅读。开启 JavaScript 可按目录逐课阅读；无脚本不影响正文与来源访问。</noscript><footer>ModelAtlas · 有限基础导读，非全领域全集。原创编辑内容 CC BY 4.0；第三方来源保留各自权利。无账号，无追踪，无自动执行。</footer></main></body></html>')
 (root/'web/foundations.html').write_text(''.join(parts)+'\n')
 (root/'web/foundations-source.json').write_bytes(source.read_bytes())
if __name__=='__main__':render(Path(__file__).resolve().parents[1])
