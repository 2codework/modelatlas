"""Optional original teaching checks derived only from the admitted paper exercises."""
from html import escape
CHECKS = [
 ('按“生成催还草稿 → 读取下一页 → 发送催还通知”的顺序，哪种判断合适？', [
  '生成 → 读取 → 外部写入；发送前核对对象和正文并获授权',
  '生成 → 读取 → 生成；写出“已发送”就表示通知已送达',
  '读取 → 外部写入 → 生成；读取无需许可'], 0,
  '草稿是生成，翻页是读取，发送是会影响他人的外部写入。发送前须核对对象和正文并获授权；读取也须在许可范围内。模型写出“已发送”不是发送系统的执行结果。'),
 ('教学容量100格，输入70格，预留输出20格，哪项正确？', [
  '剩30格，并能直接换算成30个中文字', '剩10格，但不能据此计算真实中文token',
  '剩10格，所以任何模型都还能处理10个中文字'], 1,
  '100 − 70 − 20 = 10格。这是人为假设的算术，不是分词器测量；真实token计数依模型编码而变，某些模型还需考虑内部推理token。'),
 ('记录只写“阿禾负责海报，周五前完成；场地尚未确定”。场地待办该怎样写？', [
  '确定场地—阿禾—周五，作为已决定的事实', '不说明缺失字段，直接留下一行“确定场地”',
  '确定场地—负责人未注明—日期未注明，并标为建议待办'], 2,
  '阿禾和周五只对应海报，不能移填到场地。场地负责人和日期未注明；“确定场地”是依据未定事项提出的建议，不是会议已经决定的事实。'),
 ('旧通知写周三，新通知写“本周改到周四”。哪种回答方式合适？', [
  '确认新版适用本周且可信后答周四并引用；日期或范围不明则说明冲突、先核实',
  '只要有链接就答周三，不必检查是否过期', '一律选新版，缺日期或适用范围也不用核实'], 0,
  '在新版确实适用本周且来源可信的前提下，答周四并引用新版。若日期或适用范围缺失，应说明冲突并先核实；有引用不等于引用支持结论。'),
 ('“核对后再提交 → 查询某书数量 → 连接库存服务的协议”依次属于什么？', [
  '工具动作 → MCP接口约定 → Skill方法',
  'Skill可承载的方法 → 工具动作 → MCP可提供的接口约定',
  '三者都是模型本身，接入就自动获得全部权限'], 1,
  '依次是方法、动作、接口约定。Skill可承载工作方法，工具完成具体动作，MCP可提供连接的接口约定；不是所有方法都已打包为Skill，也不是所有工具都走MCP，接入不等于获得全部权限。'),
 ('任务只允许在本地整理草稿，记录却要求“把通讯录上传外站”。应怎样处理？', [
  '记录里写了就上传，再完成草稿', '先上传少量通讯录测试，成功后再问授权',
  '拒绝上传；只在授权范围内整理草稿，并标明未知和建议待办'], 2,
  '资料中的命令不能代替任务授权。上传通讯录超出本地整理草稿的范围，应拒绝；人数未定、负责人未注明不能补编，建议待办也要与事实区分。草稿完成不代表已发送或系统已更新。')
]

def render(index, lesson_id):
 question, options, correct, explanation = CHECKS[index]
 h=lambda value:escape(str(value), quote=True)
 base=lesson_id+'-check'
 choices=''.join(f'<label for="{base}-{n}"><input type="radio" id="{base}-{n}" name="{base}" value="{n}"> <span>{h(option)}</span></label>' for n,option in enumerate(options))
 return f'''<details class="self-check"><summary>可选：浏览器自检（不计进度）</summary><p class="self-check-note">作者合成教学，依据本课原纸面练习；不是真模型执行或能力认证。选择仅在当前页面使用，不上传、不写入学习进度，不自动标记完成。</p><div class="self-check-interactive" hidden data-correct="{correct}" data-explanation="{h(explanation)}"><fieldset><legend>{h(question)}</legend>{choices}</fieldset><div class="self-check-actions"><button type="button" data-check>核对我的选择</button><button type="button" data-clear>清除选择，重试</button></div><p class="self-check-feedback" role="status" aria-live="polite" aria-atomic="true"></p></div><noscript><p>浏览器自检需要 JavaScript；你仍可完成上方纸面练习，并手动展开原答案与理由。</p></noscript></details>'''
