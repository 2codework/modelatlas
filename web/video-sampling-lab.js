(function(){
 'use strict';
 const $=id=>document.getElementById(id),en=document.documentElement.lang==='en',t=(zh,english)=>en?english:zh,api=window.VideoSampling;
 const query=new URLSearchParams(location.search||''),state=new URLSearchParams((location.hash||'').replace(/^#/,''));
 const unique=(p,key)=>p.getAll(key).length===1?p.get(key):null;
 const r=unique(query,'region'),region=['unknown','CN','US','GB','SG','international'].includes(r)?r:'unknown';
 const allowed={sequence:['worked','exercise'],stride:['1','2','3','4'],offset:['0','1','2','3'],answer:['0','1','2','3','4','5','6','7','8'],claim:['limited','continuous']};
 for(const id of Object.keys(allowed))$(id).value=allowed[id].includes(unique(state,id))?unique(state,id):({sequence:'worked',stride:'4',offset:'0'}[id]||'');
 if(Number($('offset').value)>=Number($('stride').value))$('offset').value='0';
 function links(){
  const fragment=new URLSearchParams();
  for(const id of Object.keys(allowed))if(allowed[id].includes($(id).value))fragment.set(id,$(id).value);
  document.querySelectorAll('a[href]').forEach(link=>{
   const href=link.getAttribute('href')||'';
   if(/^(?:academy|video-sampling-lab)(?:-en)?\.html(?:[?#]|$)/.test(href)){
    const [path,hash]=href.split('#');
    link.setAttribute('href',path.split('?')[0]+'?region='+region+(/^video-sampling-lab/.test(path)?'#'+fragment.toString():(hash?'#'+hash:'')));
   }
  });
 }
 function clear(){ $('feedback').textContent='';$('report').hidden=true;$('report-facts').textContent='';$('report-limits').textContent=''; }
 function label(f){return `F${f.index} · ${f.ms} ms · ID ${f.identity} · x=${f.x}`;}
 function render(){
  links();clear();
  for(const option of $('offset').options)option.disabled=Number(option.value)>=Number($('stride').value);
  try{
   const frames=api.sample($('sequence').value,Number($('stride').value),Number($('offset').value));
   $('samples').replaceChildren();frames.forEach(f=>{const li=document.createElement('li');
    const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg');
    svg.setAttribute('viewBox','0 0 110 48');svg.setAttribute('aria-hidden','true');
    const track=document.createElementNS(ns,'path');track.setAttribute('d','M5 36 H105');track.setAttribute('stroke','#899eab');
    const block=document.createElementNS(ns,'rect');for(const [k,v] of Object.entries({x:f.x-5,y:12,width:10,height:20,fill:'#3f628f'}))block.setAttribute(k,String(v));
    const identity=document.createElementNS(ns,'text');for(const [k,v] of Object.entries({x:f.x,y:10,'text-anchor':'middle','font-size':10}))identity.setAttribute(k,String(v));identity.textContent=f.identity;
    svg.append(track,block,identity);const caption=document.createElement('span');caption.textContent=label(f);li.append(svg,caption);$('samples').append(li);});
   const omitted=api.sequences[$('sequence').value].filter(f=>!frames.includes(f)).map(f=>'F'+f.index);
   $('summary').textContent=t('当前抽样','Current sample')+` · ${$('sequence').value==='worked'?'W':'E'} · s=${$('stride').value}, o=${$('offset').value} · ${frames.length}/9. `+(new Set(frames.map(f=>f.identity)).size>1?t('所选帧有身份变化。','Identity changes in the selected frames.'):t('所选帧身份相同，不能证明全程一致。','Selected identities match; full continuity is unproved.'));
   $('omitted').textContent=t('遗漏帧：','Omitted frames: ')+(omitted.join(', ')||t('无；仍未知时间戳之间的状态。','None; states between timestamps remain unknown.'));
   $('result').hidden=false;$('error').textContent='';
  }catch(_){$('result').hidden=true;$('samples').replaceChildren();$('summary').textContent='';$('omitted').textContent='';$('error').textContent=t('配置无效；旧结果已清除。点击“重置全部”恢复，或阅读静态参考。','Invalid configuration; old results cleared. Reset all to recover, or read the static reference.');}
 }
 for(const id of ['sequence','stride','offset'])$(id).addEventListener('change',()=>{if(id==='stride'&&Number($('offset').value)>=Number($('stride').value))$('offset').value='0';render();});
 for(const id of ['answer','claim'])$(id).addEventListener('change',()=>{clear();links();});
 $('reset').addEventListener('click',()=>{$('sequence').value='worked';$('stride').value='4';$('offset').value='0';$('answer').value='';$('claim').value='';render();});
 $('check').addEventListener('click',()=>{
  clear();links();
  if($('sequence').value!=='exercise'){$('feedback').textContent=t('请先切换到 E 独立练习序列；W 的断点不是本题答案。','Select exercise sequence E first; the W anomaly is not this answer.');return;}
  try{
   const result=api.check(Number($('stride').value),Number($('offset').value),$('answer').value,$('claim').value);
   const messages={invalid:t('请完整选择帧索引和证据结论，再核对。','Choose both a frame index and an evidence conclusion, then check again.'),missing:t('当前抽样没有包含异常帧；减小间隔或移动起点后再核对。静态参考可帮助定位。','The current sample omits the anomaly. Reduce stride or move the offset and check again; the static reference can help.'),retry:t('还不对。检查 E 的身份标签与时间戳；首尾相同不能证明全程一致。可展开参考后重试。','Not yet. Inspect E identities and timestamps; matching endpoints do not prove continuity. Open the reference and retry.'),correct:t('本次检查正确；以下是所选帧支持的报告，不代表真实视频评测通过。','This check is correct. The report below is supported by the selected frames, not a passed real-video evaluation.')};
   $('feedback').textContent=messages[result];
   if(result==='correct'){
    const frames=api.sample('exercise',Number($('stride').value),Number($('offset').value));
    const omitted=api.sequences.exercise.filter(f=>!frames.includes(f)).map(f=>'F'+f.index);
    $('report-facts').textContent=t('观察事实：原创序列 E；','Observed facts: original sequence E; ')+`s=${$('stride').value}, o=${$('offset').value}. `+frames.map(label).join('; ')+'. '+t('F5 身份 C，不同于所选 A 帧。遗漏帧：','F5 has identity C, unlike selected A frames. Omitted frames: ')+(omitted.join(', ')||t('无','none'))+'.';
    $('report-limits').textContent=t('未证明：遗漏帧及时间戳之间的连续性、物理正确性、真实模型质量。密集抽样只能增加给定帧的覆盖；本数据已明确存在身份变化，不能报告“全程一致”。','Unproved: continuity in omitted frames or between timestamps, physical correctness, or real model quality. Denser sampling only increases coverage of supplied frames. This fixture contains an identity change; do not report full continuity.');
    $('report').hidden=false;
   }
  }catch(_){render();}
 });
 render();
 if($('answer').value||$('claim').value)$('feedback').textContent=t('选项已保留，尚未核对；请重新核对生成报告。','Choices preserved, not checked. Check again to create a report.');
})();
