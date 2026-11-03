#!/usr/bin/env python3
"""Render one bounded evidence-reading supplement; validation is not fact verification."""
import argparse
import datetime
import html
import json
import math
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'learning/evaluation-evidence/2026-10-31/evidence.json'
IDENTITY = 'ByteDance-Seed/Seed-Coder-8B-Instruct'
PAPER = 'https://arxiv.org/html/2506.03524v1'
LABELS = {'model':'报告型号','model_version':'精确发布型号','model_version_note':'型号边界','evaluated_weight_revision':'评测权重提交','evaluated_weight_revision_note':'权重未知原因','benchmark':'评测任务','benchmark_version':'数据版本','benchmark_version_note':'数据版本未知原因','split':'子集','split_note':'子集依据','metric':'指标','unit':'单位','value':'自报值','shot':'示例数量（shot）','shot_note':'shot 未知原因','prompt':'实际提示模板','prompt_note':'提示模板未知原因','harness':'评测程序','harness_note':'程序未知原因','sampling':'采样配置','sampling_note':'采样未知原因','report_date':'固定论文版本日期','report_date_note':'日期口径','report_first_published_date':'最早公开报告日期','report_first_published_date_note':'最早日期未知原因','report_version':'固定论文版本','checked_at':'资料核对日期','source_url':'论文来源','evidence_locator':'证据定位','reported_by':'报告发布者','evidence_type':'证据类型','verification_status':'核对状态','score_comparable':'可直接横比','limitations_zh':'适用边界','correction_note_zh':'设置更正史','id':'记录标识','title':'标题'}

def require(ok, message):
    if not ok: raise ValueError(message)

def safe_url(value):
    try:
        p=urlsplit(value)
        return p.scheme=='https' and bool(p.hostname) and not p.username and not p.password and not any(c.isspace() for c in value)
    except (TypeError, ValueError): return False

def validate(data):
    require(data.get('schema_version')=='modelatlas.scoped_evaluation_evidence.v1','schema')
    s=data.get('snapshot',{})
    require(data.get('not_executed') is True and s.get('score_comparable') is False,'execution boundary')
    require(s.get('model_version')==IDENTITY and s.get('model')=='Seed-Coder-8B-Instruct','exact identity')
    require(s.get('benchmark')=='BigCodeBench-Completion' and s.get('split')=='Full' and s.get('metric')=='pass@1','task scope')
    v=s.get('value');require(isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) and 0<=v<=100 and s.get('unit')=='%','finite percentage')
    require(v==53.3 and s.get('report_date')=='2025-06-04' and data.get('checked_at')=='2026-10-31' and s.get('checked_at')=='2026-10-31','reviewed snapshot identity')
    require(s.get('source_url')==PAPER and s.get('report_version')=='arXiv:2506.03524v1','fixed paper version')
    require(s.get('verification_status')=='primary_report_checked_not_independently_reproduced','verification boundary')
    for k in ['evaluated_weight_revision','benchmark_version','shot','prompt','harness','sampling','report_first_published_date']:
        require(k in s and s[k] is None and isinstance(s.get(k+'_note'),str) and bool(s[k+'_note'].strip()),'unknown reason: '+k)
    for k in ['id','title','model_version_note','evidence_locator','reported_by','limitations_zh','correction_note_zh','report_date_note']:
        require(isinstance(s.get(k),str) and bool(s[k].strip()),'required field: '+k)
    for v in [data.get('checked_at'),s.get('checked_at'),s.get('report_date')]:
        try: require(datetime.date.fromisoformat(v).isoformat()==v,'date')
        except (TypeError,ValueError): raise ValueError('date')
    sources=data.get('sources',[])
    require(len(sources)==4 and {x.get('id') for x in sources}=={'paper-v1','paper-v1-date','model-card-pinned','official-correction'},'source identity')
    for source in sources:
        require(safe_url(source.get('url')) and source.get('locator') and source.get('kind') and source.get('checked_at'),'source fields')
    require(next(x for x in sources if x['id']=='paper-v1')['url']==PAPER,'primary source')
    card=next(x for x in sources if x['id']=='model-card-pinned')
    require(card.get('revision')=='1c5af72afa21c22c9272a0b60a3a404195e88fcd' and '/blob/'+card['revision']+'/README.md' in card['url'],'fixed model card')
    require(data.get('local_identity_match',{}).get('exactid')==IDENTITY,'catalog identity')
    return s

def e(value): return html.escape(str(value),quote=True)
def render(data):
    s=validate(data)
    metadata=''.join('<dt>'+e(LABELS.get(k,k))+'</dt><dd>'+e('未知' if v is None else '否' if v is False else {'primary_report_aggregate_metadata':'原始报告汇总元数据','primary_report_checked_not_independently_reproduced':'已核对原始报告，未独立复现','ByteDance Seed — original report self-reported':'ByteDance Seed（论文发布者自报）'}.get(str(v),v))+'</dd>' for k,v in s.items())
    names={'paper-v1':'固定论文 v1','paper-v1-date':'论文版本与日期','model-card-pinned':'固定提交的官方模型卡','official-correction':'官方设置更正公告'}
    cards=''.join('<article class="source-card"><h3>'+e(names[x['id']])+'</h3><p>'+e(x['locator'])+'</p><p class="muted">'+e(x.get('note','固定论文版本；只核对公开资料。'))+'</p><a href="'+e(x['url'])+'" target="_blank" rel="noopener noreferrer">查看官方原文 ↗</a></article>' for x in data['sources'])
    return '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'none'; style-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"><title>一条成绩，完整口径 · ModelAtlas</title><meta name="description" content="Seed-Coder-8B-Instruct 一项论文自报成绩的来源、未知配置与更正史；不是实测或排名。"><link rel="stylesheet" href="evaluation-evidence.css"></head><body><a class="skip" href="#main">跳至正文</a><header><a class="brand" href="index.html">ModelAtlas</a><nav aria-label="主导航"><a href="index.html?view=evaluation">评测资料索引</a><a href="benchmark-practice.html">评测阅读练习</a></nav></header><main id="main"><p class="eyebrow">一条成绩，完整口径 · 独立证据补充</p><h1>这个 53.3%，<br>究竟说明什么？</h1><p class="lead">先确认型号、任务和来源，再决定一个分数能回答什么。</p><section class="score" aria-labelledby="score-title"><p class="badge">厂商论文自报 · 本站未实跑、未独立复现</p><h2 id="score-title">Seed-Coder-8B-Instruct</h2><p class="identity">ByteDance-Seed/Seed-Coder-8B-Instruct</p><p class="value">'''+e(s['value'])+'''<span>%</span></p><p><strong>BigCodeBench-Completion · Full · pass@1</strong></p><p>不是 Hard 子集，也不是 BigCodeBench-Instruct；不能据此直接横比或生成排名。</p></section><p class="scope">原评测索引保留 3 条历史快照，本页独立补充 1 条；不改变原记录，不代表完整覆盖。</p><section aria-labelledby="read"><h2 id="read">已确认与仍未知</h2><p>固定依据：arXiv:2506.03524v1，§5.2.1 / Table 7。<strong>2025-06-04 是 arXiv v1 提交日</strong>，不是权重发布日期、实际运行日或已核实的最早报告公开日。资料核对：2026-10-31。</p><p>精确发布型号已确认，但<strong>评测权重 SHA、数据 revision、实际提示模板、shot、评测程序提交和采样配置仍未知</strong>。模型卡提交不等于评测权重提交，Quickstart 示例不等于评测配置。</p><details><summary>展开全部口径与未知原因</summary><dl>'''+metadata+'''</dl></details></section><section aria-labelledby="correction"><h2 id="correction">先读更正，再读成绩</h2><p>'''+e(s['correction_note_zh'])+'''</p><p class="muted">更正公告来自滚动 master，未固定提交；2025-05-14 是条目日期，2026-10-31 是本次读取日期。</p></section><section aria-labelledby="sources"><h2 id="sources">四个官方证据入口</h2><div class="source-grid">'''+cards+'''</div><p><a href="learning/evaluation-evidence/2026-10-31/evidence.json">查看结构化来源与口径 JSON</a></p></section><aside class="boundary"><strong>读过来源，不等于完成实验。</strong><p>本站未下载权重或执行评测。结构校验仅检查字段与约定，不证明论文事实、复现成功或模型性能。完整任务、提示词与运行版本未锁定前，停止横比。</p><a href="benchmark-practice.html">继续：练习填写一份评测阅读账本 →</a></aside></main><footer>公开汇总元数据 · 不镜像试题或答案 · 无需 JavaScript</footer></body></html>\n'''

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,default=DATA);ap.add_argument('--output',type=Path,default=ROOT/'web/evaluation-evidence.html');args=ap.parse_args();args.output.write_text(render(json.loads(args.input.read_text())))
if __name__=='__main__': main()
