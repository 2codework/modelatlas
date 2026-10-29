"""Render accepted task-first connection guides, without mutating their source."""
import json
from pathlib import Path
from html import escape as h

def render(root):
 d=json.loads((root/'learning/task-first/connections.json').read_text());out=['''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'"><title>连接与设置 · ModelAtlas</title><link rel="stylesheet" href="learn.css"><script src="connections.js" defer></script></head><body><a class="skip" href="#lesson-main">跳至正文</a><header><a class="brand" href="index.html">MODEL ATLAS</a><nav aria-label="主导航"><a href="learn.html#step-4">← 工具入门</a><a href="index.html?view=explore">资料库</a></nav></header><div class="learn-layout"><aside><details class="chapter-menu" open><summary>选择连接方式</summary><nav aria-label="连接路线">''']
 for r in d['routes']:out.append(f'<a href="#{h(r["id"])}">{h(r["title"])}</a>')
 out.append('</nav></details></aside><main id="lesson-main"><p id="connection-status" role="status"></p><section id="connection-intro"><h1>先完成任务，再决定接什么</h1><p>只是整理文字，不需要 MCP 或 Skill。需要读外部资料、或复用固定方法时，再选择相应路线。</p><a class="primary-action" href="#no-extra-tool">先做不接工具的文字练习 →</a></section>')
 for r in d['routes']:
  out.append(f'<article id="{h(r["id"])}" data-route><p class="eyebrow">{h(r["level"])}</p><h1>{h(r["title"])}</h1><p class="lesson-lead">{h(r["outcome"])}</p><p>{h(r["product"])}</p><a class="primary-action" href="{h(r["start_url"])}" target="_blank" rel="noopener noreferrer">{h(r["start_label"])} ↗</a><h2>第一次使用，从这里开始</h2><ol>')
  for x in r['onboarding_steps']:out.append('<li>'+h(x)+'</li>')
  out.append('</ol>')
  out.append('<div class="caution"><strong>费用与权限，先看清</strong><p>'+h(r['accounts_cost'])+'</p><p>'+h(r['minimum_access'])+'</p></div><h2>按顺序做</h2><ol>')
  for x in r['steps']:out.append('<li>'+h(x)+'</li>')
  out.append('</ol>')
  out.append('<details><summary>本路线的测试输入</summary><pre>'+h(r['test_input'])+'</pre></details>')
  if r.get('config_filename'):out.append('<p>配置文件：<code>'+h(r['config_filename'])+'</code></p>')
  for key,title in [('onboarding_commands','环境准备命令（由你核对后执行）'),('commands','连接命令'),('config','配置内容'),('creator_prompt','创建方法包的提示词'),('prompt','完整提示词'),('file_prompt','处理你自己的附件：专用提示词'),('followup_prompt',r.get('followup_prompt_label','修正这个合成样例的提示词')),('file_correction_prompt','真实附件的通用纠错提示词'),('disable_path_note','停用配置：先替换为自己的真实路径'),('disable_config','停用配置'),('windows_disable_config','Windows 停用配置示例（正斜杠路径）')]:
   if r.get(key):
    cid=r['id']+'-'+key;out.append(f'<section class="prompt-card"><h2>{h(title)}</h2><pre id="{cid}">{h(r[key])}</pre><button type="button" data-copy="{cid}">复制{h(title)}</button><p id="{cid}-status" role="status"></p></section>')
  out.append('<h2>应该看到什么</h2><ul>')
  for x in r['expected_observations']:out.append('<li>'+h(x)+'</li>')
  out.append('</ul><details><summary>展开参考结果（供对照，不是实跑记录）</summary><pre>'+h(r['reference_output'])+'</pre></details><h2>不对时，先这样检查</h2>')
  for x in r['recovery']:out.append('<details><summary>'+h(x['symptom'])+'</summary><p>'+h(x['action'])+'</p></details>')
  out.append('<h2>结束与撤销</h2><p>'+h(r['disconnect'])+'</p>')
  for x in r['platform_notes']:out.append('<p>'+h(x)+'</p>')
  out.append('<details class="sources"><summary>步骤依据、核验范围与原始记录</summary><p>'+h(d['verification_scope'])+'</p><ul>')
  for sid in r['source_ids']:
   src=next(x for x in d['sources'] if x['id']==sid);out.append('<li><a href="'+h(src['url'])+'" target="_blank" rel="noopener noreferrer">'+h(src['title'])+'</a> · '+h(src['checked_on'])+'</li>')
  out.append('</ul><p>自编虚构样例；验收结果供对照，不代表已替你实跑。</p><a href="connections-source.json">完整原始指南记录</a></details><nav class="lesson-next"><a href="learn.html#step-4">← 回到工具入门</a><a href="index.html">回到首页</a></nav></article>')
 out.append('<noscript>未开启脚本时可阅读全部路线；提示词可手动选择复制。</noscript></main></div></body></html>')
 (root/'web/connections.html').write_text(''.join(out)+'\n');(root/'web/connections-source.json').write_bytes((root/'learning/task-first/connections.json').read_bytes())
