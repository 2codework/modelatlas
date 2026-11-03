/* Optional enhancement only. Every lesson and navigation link is static HTML. */
(function(){'use strict';
const root=document.querySelector('.academy');if(!root)return;
const en=root.dataset.language==='en';
function read(key,fallback){try{const value=JSON.parse(localStorage.getItem(key));return value===null?fallback:value;}catch(_){return fallback;}}
function write(key,value){try{localStorage.setItem(key,JSON.stringify(value));return true;}catch(_){return false;}}
const notice=root.querySelector('.academy-storage-status');
function status(text){if(notice)notice.textContent=text;}
// One initial narrow-screen choice; native manual toggles remain untouched afterward.
const chaptersDisclosure=root.querySelector('.academy-chapter-disclosure');
if(chaptersDisclosure&&typeof window!=='undefined'&&typeof window.matchMedia==='function'){try{if(window.matchMedia('(max-width: 800px)').matches)chaptersDisclosure.open=false;}catch(_){/* keep readable native fallback */}}
// Native mobile disclosure; only Escape within this menu is enhanced.
const mainMenu=root.querySelector('.academy-main-menu');
if(mainMenu)mainMenu.addEventListener('keydown',event=>{if(event.key==='Escape'&&mainMenu.open){event.preventDefault();mainMenu.open=false;mainMenu.querySelector('summary').focus();}});
const region=root.querySelector('.academy-region'),remember=root.querySelector('.academy-remember-region');
const allowedRegions=['unknown','CN','US','GB','SG','international'];
const urlRegion=new URLSearchParams(location.search||'').get('region');
const boundedQuery=value=>Array.from(String(value||'')).slice(0,200).join('');
let query=boundedQuery(new URLSearchParams(location.search||'').get('q'));
let searchHistoryFailed=false;
function queryParams(current){const params=new URLSearchParams(current||'');params.set('region',region?region.value:'unknown');if(query.trim())params.set('q',query);else params.delete('q');return params;}
function syncSearchURL(){
 if(typeof history==='undefined'||!history.replaceState)return;
 try{const params=queryParams(location.search);history.replaceState(history.state,'',(location.pathname||'')+'?'+params.toString()+(location.hash||''));searchHistoryFailed=false;}
 catch(_){searchHistoryFailed=true;}
}

const saved=read('modelatlas.academy.region','unknown');
function propagateRegion(){if(!region)return;root.querySelectorAll('a[href]').forEach(link=>{const href=link.getAttribute('href')||'';if(/^(?:academy|attention-lab|video-sampling-lab|release-reading|benchmark-practice|tiny-training|retrieval-lab|tokenization-lab|diffusion-noise-lab)(?:-en)?\.html(?:[?#]|$)/.test(href)){const parts=href.split('#'),path=parts[0].split('?')[0],params=new URLSearchParams(parts[0].split('?')[1]||'');params.set('region',region.value);if(/^academy(?:-en)?\.html$/.test(path)&&query.trim())params.set('q',query);else params.delete('q');link.setAttribute('href',path+'?'+params.toString()+(parts.length>1?'#'+parts.slice(1).join('#'):''));}});}

if(region&&remember){region.value=allowedRegions.includes(urlRegion)?urlRegion:(allowedRegions.includes(saved)?saved:'unknown');remember.checked=saved!=='unknown'&&allowedRegions.includes(saved);propagateRegion();
function saveRegion(){syncSearchURL();searchFeedback();propagateRegion();if(remember.checked){if(!write('modelatlas.academy.region',region.value))status(en?'Cannot save region; selection applies to this page only.':'无法保存地区；选择仅用于当前页面。');else status(en?'Region saved on this device only.':'地区仅保存在本机。');}else{try{localStorage.removeItem('modelatlas.academy.region');status(en?'Region is not remembered; selection applies to this page only.':'不记住地区；选择仅用于当前页面。');}catch(_){status(en?'Cannot clear saved region; use browser storage settings.':'无法清除已存地区；请使用浏览器存储设置。');}}}
region.addEventListener('change',saveRegion);remember.addEventListener('change',saveRegion);}
root.querySelectorAll('a[data-language]').forEach(link=>{link.addEventListener('click',()=>{const hash=location.pathname.endsWith('index.html')||document.getElementById('academy-home')?'#home':location.hash;link.href=(link.dataset.language==='en'?'academy-en.html':'academy.html')+'?'+queryParams('').toString()+hash;});});
const coreLessons=[['foundations','模型、应用与 Agent','Models, applications and Agents','模型 应用 原理 训练 推理 rag model application training inference'],['tokens','token 与 attention','Tokens and attention','分词 token attention transformer 推理 mechanism'],['tools','工具调用与记忆边界','Tool calls and memory boundaries','工具 记忆 权限 memory tool authorization injection 注入'],['project','资料问答 Agent 项目','Document Q&A Agent project','agent 项目 代码 拒答 超时 测试 project code refusal timeout test retry'],['timeline','AI 发展史与日期','AI timeline and dates','进展 厂商 发布 日期 history release dates progress'],['multimodal','多模态、视频与世界模型','Multimodal, video and world models','多模态 视频 音频 图像 世界 multimodal video audio image world'],['resources','模型与资料','Models and resources','模型 资料 许可 resources license catalog'],['evaluation','评测与方法','Evaluation and methods','评测 方法 测试 evaluation benchmark test']];
// Reading and region feedback deliberately have separate live regions.
const key='modelatlas.academy.read.v1';let progress=[],storedProgress=[],progressWritable=true,temporary=false;
// Unsaved explicit intentions, not a stale copy of the entire stored array.
const pendingProgress=new Map();
function applyProgressIntent(values,id,done){return done?(values.includes(id)?values:[...values,id]):values.filter(value=>value!==id);}
function reconcileProgress(){
 progress=storedProgress;
 pendingProgress.forEach((done,id)=>{progress=applyProgressIntent(progress,id,done);});
 temporary=!progressWritable||pendingProgress.size>0;
}
const readingNotice=root.querySelector('.academy-reading-status');
const summary=root.querySelector('#academy-progress-summary'),next=root.querySelector('#academy-progress-next');
const buttons=Array.from(root.querySelectorAll('[data-read]'));
function loadProgress(){
 try{const raw=localStorage.getItem(key);const parsed=raw===null?[]:JSON.parse(raw);
  if(!Array.isArray(parsed)||parsed.some(x=>typeof x!=='string'))throw new Error('corrupt');
  storedProgress=parsed;progressWritable=true;
 }catch(_){progressWritable=false;}
 reconcileProgress();
}
function renderProgress(){
 const count=coreLessons.filter(([id])=>progress.includes(id)).length;
 if(summary)summary.textContent=en?`${count} / 8 core chapters marked read${temporary?' · temporary marks':''}`:`已标记 ${count} / 8 个核心章节${temporary?' · 临时标记':''}`;
 if(readingNotice)readingNotice.textContent=temporary?(en?'Reading storage unavailable or damaged. Marks are temporary on this page; leaving or refreshing may lose changes. Original stored data was not overwritten. Repair or clear only this key in browser settings to save again.':'已读存储不可用或损坏。标记仅在当前页面临时有效，离开或刷新可能丢失更改；未覆盖原存储数据。请在浏览器设置修复或清除该键后再保存。'):(en?'Reading marks are saved in this browser only. You can toggle them off in each chapter.':'阅读标记仅保存在本浏览器，可在各章取消。');
 root.querySelectorAll('[data-progress-id]').forEach(label=>{label.textContent=progress.includes(label.dataset.progressId)?(en?'Marked read':'已标记读过'):(en?'Not marked':'未标记');});
 if(next){const item=coreLessons.find(([id])=>!progress.includes(id));next.setAttribute('href',(en?'academy-en.html':'academy.html')+'#'+(item?item[0]:'foundations'));next.textContent=item?(en?'Next unmarked: '+item[2]+' →':'下一未标记章：'+item[1]+' →'):(en?'All 8 marked · Review from chapter 01 →':'8 章均已标记 · 从第一章复习 →');}
 buttons.forEach(button=>{const done=progress.includes(button.dataset.read);button.setAttribute('aria-pressed',String(done));button.textContent=button.dataset.unreadLabel;const note=button.parentElement.querySelector('small');if(note)note.textContent=(done?(en?'Marked read. ':'已标记读过。'):(en?'Not marked. ':'未标记。'))+(temporary?(en?'Storage unavailable or damaged: temporary mark only. Original stored data was not overwritten.':'存储不可用或损坏：本次标记仅临时有效，未覆盖原存储数据。'):(en?'Self-reported reading only; not mastery or lab completion.':'仅自行标记读过，不代表掌握或完成实验。'));});
 propagateRegion();
}
loadProgress();renderProgress();
buttons.forEach(button=>button.addEventListener('click',()=>{
 // Capture the action from the displayed state BEFORE reading another tab's changes.
 const id=button.dataset.read,done=!progress.includes(id);
 loadProgress();pendingProgress.set(id,done);reconcileProgress();
 // Reapply only explicit pending intentions to the latest valid array, preserving
 // unrelated IDs, unknown IDs, ordering and duplicates. localStorage is not atomic.
 if(progressWritable&&write(key,progress)){storedProgress=progress;pendingProgress.clear();reconcileProgress();}
 renderProgress();
}));
// Events are notifications, not authoritative snapshots: an older queued event
// must not roll back newer storage. Never write in response to an event. Pending
// page-only intentions survive external updates and Back/Forward cache restores.
if(typeof window!=='undefined'){
 window.addEventListener('storage',event=>{
  if(event.key!==key&&event.key!==null)return;
  try{if(event.storageArea&&event.storageArea!==localStorage)return;}catch(_){/* read below reports unavailable storage */}
  loadProgress();renderProgress();
 });
 window.addEventListener('pageshow',event=>{if(event.persisted){loadProgress();renderProgress();}});
}
// Explicit local learning destinations: labs are not additional core chapters.
const entries=coreLessons.map(([id,zh,en,keywords])=>({kind:'core',zh,en,keywords,destinations:['academy.html#'+id,'academy-en.html#'+id]}));
entries.push(
 {kind:'lab',zh:'原文检索与可核对引用',en:'Source retrieval and verifiable citations',keywords:'RAG 检索 分块 引用 权限 版本 retrieval chunk citation lexical source version',destinations:['retrieval-lab.html','retrieval-lab-en.html']},
 {kind:'lab',zh:'九个参数：真正训练一步',en:'Nine parameters: one training step',keywords:'训练 损失 梯度 交叉熵 参数 更新 bigram training loss gradient cross entropy frozen inference',destinations:['tiny-training.html','tiny-training-en.html']},
 {kind:'lab',zh:'评测阅读课：来源、条件与独立迁移',en:'Benchmark reading: evidence and independent transfer',keywords:'评测 阅读 比较 BAGEL RISE KRIS benchmark comparison evidence ledger harness judge 独立复现',destinations:['benchmark-practice.html','benchmark-practice-en.html']},
 {kind:'lab',zh:'发布阅读课：Qwen3-8B 有条件的简报',en:'Release reading: a qualified Qwen3-8B brief',keywords:'Qwen/Qwen3-8B Qwen3 发布 简报 YaRN 原生 上下文 权重 release brief native context announcement report',destinations:['release-reading.html','release-reading-en.html']},
 {kind:'lab',zh:'Attention 实验台：从分数到输出',en:'Attention lab: from scores to output',keywords:'注意力 attention softmax query key value Q K V mask 掩码 分数 权重 输出',destinations:['attention-lab.html','attention-lab-en.html']},
 {kind:'lab',zh:'视频抽帧实验：看见的，不等于连续的',en:'Video sampling lab: observed is not continuous',keywords:'视频 抽帧 采样 时序 连续 video sampling frames temporal evidence',destinations:['video-sampling-lab.html','video-sampling-lab-en.html']}
);
entries.push({kind:'lab',zh:'字符 BPE 分词：学习规则与冻结编码',en:'Character BPE: learn rules and freeze encoding',keywords:'分词 字符 编码 解码 bpe tokenizer tokenization encode decode subword',destinations:['tokenization-lab.html','tokenization-lab-en.html']});
entries.push({kind:'lab',zh:'扩散噪声与预测误差：加噪、反解与放大',en:'Diffusion noise and prediction error: mixing, inversion and amplification',keywords:'扩散 噪声 反解 预测误差 diffusion noise ddpm alpha epsilon denoising mse',destinations:['diffusion-noise-lab.html','diffusion-noise-lab-en.html']});
// Search-only normalization: keep the original bounded query in the input and URL.
// Han fragments remain searchable; other words match from the start, not inside
// unrelated words. Hyphens/slashes separate terms; dots retain version components.
function searchTokens(value){return String(value).normalize('NFKC').toLowerCase().replace(/\p{Script=Han}+/gu,' $& ').match(/[\p{L}\p{N}]+(?:\.[\p{L}\p{N}]+)*/gu)||[];}
function matchesSearch(item,terms){
 const words=[item.zh,item.en,item.keywords,...item.destinations].flatMap(searchTokens);
 return terms.length>0&&terms.every(term=>words.some(word=>
  /\p{Script=Han}/u.test(term)?word.includes(term):
  word.startsWith(term)&&!(/\d$/.test(term)&&/\d/.test(word[term.length]||''))&&
  (!/^\d/.test(term)||word.length===term.length||word[term.length]==='.')
 ));
}
const input=root.querySelector('#academy-search'),list=root.querySelector('#academy-search-results');
const clear=root.querySelector('#academy-search-clear'),searchNotice=root.querySelector('#academy-search-status');
function searchFeedback(){if(searchNotice)searchNotice.textContent=searchHistoryFailed?(en?'Search works on this page, but its URL could not be updated; reload or language changes may lose it.':'搜索仍可在本页使用，但无法更新网址；刷新或切换语言可能丢失检索词。'):'';}
function renderSearch(){if(!input||!list)return;input.value=query;if(clear)clear.hidden=!query;searchFeedback();
 list.replaceChildren();
 if(!query.trim()){propagateRegion();return;}
 const terms=searchTokens(query),matches=entries.filter(item=>matchesSearch(item,terms));
 for(const item of matches){
  const li=document.createElement('li'),a=document.createElement('a');
  a.href=item.destinations[en?1:0];
  const kind=item.kind==='lab'?(en?'Practical lab':'实践实验'):(en?'Core lesson':'核心课程');
  a.textContent=kind+' · '+item[en?'en':'zh'];li.append(a);list.append(li);
 }
 // Also handles already-rendered results when the region selector changes.
 propagateRegion();
 if(!matches.length){const li=document.createElement('li');li.textContent=en?'No lesson or lab matches. Try a broader term or open Models & Resources; absence does not mean a technology does not exist.':'未找到课程或实验。试试更宽泛的词，或进入“模型与资料”；未收录不代表不存在。';list.append(li);}
}
if(input&&list){
 input.addEventListener('input',()=>{query=boundedQuery(input.value);syncSearchURL();renderSearch();});
 if(clear)clear.addEventListener('click',()=>{query='';syncSearchURL();renderSearch();input.focus();});
 renderSearch();
 if(typeof window!=='undefined'){
  const restoreSearch=()=>{if(!searchHistoryFailed)query=boundedQuery(new URLSearchParams(location.search||'').get('q'));const r=new URLSearchParams(location.search||'').get('region');if(region&&allowedRegions.includes(r))region.value=r;renderSearch();};
  window.addEventListener('popstate',restoreSearch);
  window.addEventListener('pageshow',restoreSearch);
 }
}
})();
