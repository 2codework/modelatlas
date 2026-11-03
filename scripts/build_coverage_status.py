#!/usr/bin/env python3
"""Render the checked-in finite coverage snapshot. No network or sibling-repo reads."""
import argparse,html,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
def render(s):
 if s.get('schema')!='modelatlas.coverage-snapshot.v1':raise ValueError('unsupported snapshot schema')
 c=s['catalog'];m=s['monthly'];p=s['practice'];e=lambda x:html.escape(str(x),quote=True)
 for v in [c['records'],c['providers'],*c['urls'].values(),c['release_date_known'],*m.values(),p['cases'],p['synthetic_cases'],p['recipes'],p['product_books'],p['external_product_runs_observed']]:
  if type(v) is not int or v<0:raise ValueError('counts must be nonnegative integers')
 if p['external_product_runs_observed']!=0 or p['api_local_execution']!='never-run':raise ValueError('execution stage copy requires editorial update')
 if p['synthetic_cases']>p['cases']:raise ValueError('synthetic cases exceed case count')
 if m['weights_events']>m['events']:raise ValueError('weight events exceed all events')
 if m['dated']+m['undated']!=m['weights_events']:raise ValueError('weight counts inconsistent')
 if any(v>c['records'] for v in [*c['urls'].values(),c['release_date_known']]):raise ValueError('catalog numerator exceeds denominator')
 def metric(value,label,note):return f'<article class="cv-card"><p class="cv-number">{e(value)}</p><h2>{e(label)}</h2><p>{e(note)}</p></article>'
 def row(label,n,d):return f'<li><span>{e(label)}</span><strong>{n} / {d}</strong></li>'
 cards=metric(c['records'],'厂商目录记录',f"涉及{c['providers']}家厂商；有精确型号，也有别名，不能直接当独立模型总数。")+metric(m['events'],'月度事件记录','公告、论文、代码、权重与API分开记录；同一模型可对应多条事件。')+metric(p['recipes'],'产品练习配方',f"来自AgentWork的{p['product_books']}份产品手册；素材与参考答案不是实际产品成绩。")
 fields=''.join(row(label,c['urls'][k],c['records']) for label,k in [('模型卡入口','model_card'),('报告入口','report'),('用法资料入口','tutorial'),('代码仓库入口','repository')])+row('已登记发布日',c['release_date_known'],c['records'])
 return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'none'; style-src 'self'; connect-src 'none'; img-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'"><meta name="description" content="看清哪些内容已收录、哪些证据仍缺、哪些练习尚未运行。有限核验快照，不是全球完整率。"><title>收录与实践进度 · ModelAtlas</title><link rel="stylesheet" href="campus.css"><link rel="stylesheet" href="coverage-status.css"></head>
<body class="campus coverage-status" data-site="modelatlas"><a class="cv-skip" href="#main">跳至内容</a><header><a class="brand" href="index.html">ModelAtlas <small>一起学，慢慢弄懂</small></a><nav aria-label="主导航"><a href="index.html">开始学习</a><a href="monthly.html">每月模型发布</a><a href="coverage-status.html" aria-current="page">收录与实践进度</a></nav></header>
<main id="main"><section class="cv-hero"><p class="cv-kicker">核验快照 {e(s['checked_on'])}</p><h1>学到哪里，也看清还缺什么。</h1><p>把收录数量、证据完整度和真正做过的练习分开看。<br>不以条目多代替内容全面，也不把未运行写成成功。</p><p class="cv-snapshot">{e(s['snapshot_note'])}</p></section>
<section class="cv-grid" aria-label="三种不同的计数">{cards}</section>
<section class="cv-section" aria-labelledby="known"><h2 id="known">先看已登记的，再看待核对的</h2><p>每个数字都有固定分母；空白表示本次未登记或未核实，不代表世界上不存在。</p>
<div class="cv-pair"><article class="cv-panel"><h3>目录资料，还不均衡</h3><ul class="cv-metrics">{fields}</ul><p class="cv-small">分母均为这{c['records']}条目录记录。链接存在不等于正文已读懂、可运行或适用于每个版本。</p><details><summary>这些缺项意味着什么？</summary><p>托管API可能没有公开权重，因此权重许可不能要求每条都有。用法资料入口也可能是价格页或产品说明，不一概称为完整教程。型号的公告、论文、API上线和权重开放日期应分别核对，不能用资料核验日代替发布日期。</p></details><a href="index.html?view=vendor-catalog">查目录与具体来源 →</a></article>
<article class="cv-panel"><h3>权重开放，日期仍有待确认</h3><p class="cv-number cv-number-small">{m['dated']} <span>条有月份</span></p><p>默认权重范围共{m['weights_events']}条事件，其中<strong>{m['undated']}条尚无可归属月份</strong>。</p><p>日期未知的记录单独保留，不拿最后修改时间、论文日期或公告猜成首次上传。</p><details><summary>为什么不是“模型数量”？</summary><p>一次家族发布可能包含多个规格；同一模型也可能有论文、公告及权重等多条事件。月度补录是独立整理，与知识图谱不是同一个统计口径，不能相加。</p><p>某个月没有样本，只说明本站尚未收录，不表示当月全球没有发布。公开权重也不自动等于完整开源。</p></details><a href="monthly.html">按月查记录与未定日期 →</a></article></div></section>
<section class="cv-section"><h2>从“写了步骤”到“真的做过”，还有距离</h2><p>AgentWork历史快照包含{p['cases']}个历史案例，其中{p['synthetic_cases']}个为历史合成教学案例。截至2026-11-01的本地改版另有9个新增完整双语教学案例（办公、设计、数据、客服、编程、采用研究、营销内容、媒体制作方案、个人自动化），不计入这份历史快照，也不是线上实时清单；两者不应相加称为已核验案例总数，也不代表真实产品实测。{p['recipes']}条产品配方尚未获得真实产品运行记录。ModelAtlas的API与本地调用实践也仍标记为未运行。</p><ol class="cv-stages"><li><strong>01 · 文档与教学材料</strong><span>已有步骤、输入和检查方法；可供阅读练习。</span></li><li><strong>02 · 作者参考校验</strong><span>部分本地参考结果已检查；不代表外部产品输出。</span></li><li><strong>03 · 真实产品运行</strong><span>本快照未建立实跑证据；不展示虚构成功率。</span></li></ol><details class="cv-wide"><summary>一条练习怎样才算有运行证据？</summary><p>至少保留产品与版本、获准使用的输入、真实输出、验收结果、失败与修正。素材或检查脚本可执行，不代表它已经执行；局部检查通过，也不代表整条工作流成功。</p><p>涉及账号、付费、对外发送或写入的步骤应先确认权限。没有合适环境时可以完成纸面练习，并如实保留“未运行”。</p></details></section>
<section class="cv-section cv-next"><h2>下一步：补证据，不盲目堆条目</h2><ul><li><strong>补日期：</strong>逐条查官方发布日期；查不到也留下“未知”和核验范围。</li><li><strong>补许可与入口：</strong>分开模型权重和代码许可，区分教程、价格页与产品介绍。</li><li><strong>补可照做的过程：</strong>每条练习说明材料、交付物、验收和失败恢复，实跑记录单独保存。</li></ul><details><summary>阅读体验也需要验收</summary><p>已有桌面与窄屏内部预览检查，但不等于实体手机或读屏软件验收。继续检查键盘操作、焦点、缩放与长中文内容，不用测试总数代替用户能否读懂和完成任务。</p></details></section>
<p class="cv-ending">一个小任务做得可核对，比一个“全部完成”的数字更有用。</p></main><footer><a href="index.html?view=coverage">查看方法与证据 →</a><span>固定快照 · 非全球全集 · 非实时状态</span></footer></body></html>'''
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--snapshot',type=pathlib.Path,default=ROOT/'learning/coverage/2026-11-02-smollm3-family/snapshot.json');ap.add_argument('--output',type=pathlib.Path,default=ROOT/'web/coverage-status.html');args=ap.parse_args();args.output.write_text(render(json.loads(args.snapshot.read_text()))+'\n')
if __name__=='__main__':main()
