'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const code=fs.readFileSync(__dirname+'/../web/academy.js','utf8');
class Element{constructor(dataset={}){this.dataset=dataset;this.handlers={};this.children=[];this.attrs={};this.value='';this.textContent='';this.checked=false;}addEventListener(k,fn){this.handlers[k]=fn;}fire(k){this.handlers[k]?.();}setAttribute(k,v){this.attrs[k]=v;if(k==='href')this.href=v;}getAttribute(k){return k==='href'?(this.href||''):(this.attrs[k]||'');}append(x){this.children.push(x);}replaceChildren(){this.children=[];}}
function setup(initial={},blocked=false,language='en',search=''){const values=new Map(Object.entries(initial)),writes=[];const region=new Element(),remember=new Element(),notice=new Element(),input=new Element(),list=new Element(),note=new Element(),button=new Element({read:'tools',readLabel:'Read',unreadLabel:'Mark'}),zh=new Element({language:'zh'}),en=new Element({language:'en'});button.parentElement={querySelector:()=>note};const elements={'.academy-region':region,'.academy-remember-region':remember,'.academy-storage-status':notice,'#academy-search':input,'#academy-search-results':list};const root={dataset:{language},querySelector:s=>elements[s],querySelectorAll:s=>s==='[data-read]'?[button]:s==='a[href]'?[zh,en,...list.children.flatMap(li=>li.children)]:[zh,en]};const ctx={URLSearchParams,document:{querySelector:()=>root,getElementById:()=>null,createElement:()=>new Element()},location:{search,pathname:'/academy-en.html',hash:'#tools'},localStorage:{getItem:k=>{if(blocked)throw Error();return values.get(k)??null;},setItem:(k,v)=>{if(blocked)throw Error();writes.push(k);values.set(k,v);},removeItem:k=>{if(blocked)throw Error();values.delete(k);}}};vm.runInNewContext(code,ctx);return {values,writes,region,remember,notice,input,list,button,note,zh,en};}
test('new read marks toggle without touching legacy records',()=>{const old='{"schema":"modelatlas.progress.v1","completed":["agents"]}';const s=setup({'modelatlas.progress':old});s.button.fire('click');assert.equal(s.button.attrs['aria-pressed'],'true');s.button.fire('click');assert.equal(s.button.attrs['aria-pressed'],'false');assert.equal(s.values.get('modelatlas.progress'),old);assert.deepEqual(s.writes,['modelatlas.academy.read.v1','modelatlas.academy.read.v1']);});
test('damaged new reading record is preserved byte-for-byte and cannot be overwritten',()=>{for(const bad of ['{bad','{}','[1]']){const s=setup({'modelatlas.academy.read.v1':bad});s.button.fire('click');assert.equal(s.values.get('modelatlas.academy.read.v1'),bad);assert.equal(s.writes.length,0);assert.match(s.note.textContent,/not overwritten/);}});
test('storage denial gives visible temporary-state guidance',()=>{const s=setup({},true);s.button.fire('click');assert.match(s.note.textContent,/temporary/);s.remember.checked=true;s.region.fire('change');assert.match(s.notice.textContent,/Cannot save/);});
test('region persistence is opt-in, international differs from unknown, and language keeps chapter',()=>{const s=setup();s.region.value='international';s.region.fire('change');assert.equal(s.writes.length,0);s.remember.checked=true;s.remember.fire('change');assert.equal(s.values.get('modelatlas.academy.region'),'"international"');s.zh.fire('click');assert.equal(s.zh.href,'academy.html?region=international#tools');assert.equal(s.region.value,'international');s.remember.checked=false;s.remember.fire('change');assert.equal(s.values.has('modelatlas.academy.region'),false);});
test('bilingual core search supports memory, no results and safe repeated input',()=>{const s=setup();s.input.value='记忆';s.input.fire('input');assert.equal(s.list.children.length,1);assert.equal(s.list.children[0].children[0].href,'academy-en.html?region=unknown&q=%E8%AE%B0%E5%BF%86#tools');s.input.value='<script>unknown';s.input.fire('input');assert.equal(s.list.children.length,1);assert.match(s.list.children[0].textContent,/No lesson or lab/);s.input.value='';s.input.fire('input');assert.equal(s.list.children.length,0);});

function search(s,query){s.input.value=query;s.input.fire('input');return s.list.children.flatMap(li=>li.children);}
for(const language of ['zh','en'])for(const region of ['CN','US','GB','SG','international','unknown']){
 test(`learning entry discovery: ${language}, ${region}`,()=>{
  const s=setup({},false,language,'?region='+region),suffix=language==='en'?'-en':'';
  for(const [queries,file] of [
   [['bigram','gradient','交叉熵','九个参数：真正训练一步','Nine parameters: one training step'],'tiny-training'],
   [['softmax',' SOFTMAX ','Attention 实验台：从分数到输出','Attention lab: from scores to output'],'attention-lab'],
   [['抽帧','sampling','视频抽帧实验：看见的，不等于连续的','Video sampling lab: observed is not continuous'],'video-sampling-lab'],
   [['BAGEL','RISE','KRIS','评测阅读课：来源、条件与独立迁移','Benchmark reading: evidence and independent transfer'],'benchmark-practice'],
   [['Qwen/Qwen3-8B','Qwen3-8B','YaRN','发布阅读课：Qwen3-8B 有条件的简报','Release reading: a qualified Qwen3-8B brief'],'release-reading']
  ])for(const query of queries){
   const links=search(s,query);assert.equal(links.length,1,query);
   assert.equal(links[0].href,`${file}${suffix}.html?region=${region}`);
   assert.match(links[0].textContent,language==='en'?/^Practical lab · /:/^实践实验 · /);
   assert.equal(links[0].handlers.click,undefined,'ordinary anchor; no click interception');
   assert.equal(links[0].handlers.keydown,undefined,'native Enter activation is not intercepted');
  }
  const links=search(s,'attention');assert.equal(links.length,2);
  assert.equal(new Set(links.map(a=>a.href)).size,2);
  assert.equal(links[0].href,`academy${suffix}.html?region=${region}&q=attention#tokens`);
  assert.match(links[0].textContent,language==='en'?/^Core lesson · /:/^核心课程 · /);
  s.region.value=region==='CN'?'US':'CN';s.region.fire('change');
  assert.equal(links[0].href,`academy${suffix}.html?region=${s.region.value}&q=attention#tokens`);
  assert.equal(links[1].href,`attention-lab${suffix}.html?region=${s.region.value}`);
  const video=search(s,'sampling')[0];s.region.value='SG';s.region.fire('change');
  assert.equal(video.href,`video-sampling-lab${suffix}.html?region=SG`);
  assert.equal(search(s,'sampling')[0].href,video.href,'repeated searches keep current region');
  for(const query of ['','  '])assert.equal(search(s,query).length,0);
  for(const query of ['nonexistent-learning-entry','<img src=x onerror=alert(1)>','<script>alert(1)</script>']){
   assert.equal(search(s,query).length,0);assert.equal(s.list.children.length,1);
   assert.match(s.list.children[0].textContent,language==='en'?/No lesson or lab/:/未找到课程或实验/);
  }
  assert.equal(s.writes.length,0,'search does not write storage');
 });
}
test('all eight original core chapter destinations remain searchable',()=>{
 for(const language of ['zh','en']){
  const s=setup({},false,language);
  for(const id of ['foundations','tokens','tools','project','timeline','multimodal','resources','evaluation']){
   assert.ok(search(s,id).some(a=>a.href===`academy${language==='en'?'-en':''}.html?region=unknown&q=${id}#${id}`),id);
  }
 }
});
