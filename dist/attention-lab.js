(function () {
  'use strict';
  const en = document.documentElement.lang === 'en';
  const $ = id => document.getElementById(id);
  const math = window.AttentionMath;
  // Locale state is URL-only; no storage, network, or submitted-answer status.
  const params = new URLSearchParams(location.search || '');
  const state = new URLSearchParams((location.hash || '').replace(/^#/, ''));
  const unique = name => state.getAll(name).length === 1 ? state.get(name) : null;
  const candidate = params.getAll('region').length === 1 ? params.get('region') : null;
  const region = ['unknown', 'CN', 'US', 'GB', 'SG', 'international'].includes(candidate) ? candidate : 'unknown';
  const validAnswer = raw => typeof raw === 'string' && raw.length <= 64 && math.checkAnswer(raw) !== 'invalid';
  $('query').value = ['0', '1', '2'].includes(unique('query')) ? unique('query') : '0';
  $('causal').checked = unique('mask') === '1';
  const restoredAnswer = unique('answer');
  $('answer').value = validAnswer(restoredAnswer) ? restoredAnswer.trim() : '';
  function updateLinks() {
    document.querySelectorAll('a[href]').forEach(link => {
      const href = link.getAttribute('href') || '';
      if (/^(?:academy|attention-lab)(?:-en)?\.html(?:[?#]|$)/.test(href)) {
        const [path, hash] = href.split('#');
        let search = '?region=' + encodeURIComponent(region);
        let fragment = hash ? '#' + hash : '';
        if (/^attention-lab(?:-en)?\.html/.test(path)) {
          fragment = '#query=' + (['0', '1', '2'].includes($('query').value) ? $('query').value : '0');
          fragment += '&mask=' + ($('causal').checked ? '1' : '0');
          if (validAnswer($('answer').value)) fragment += '&answer=' + encodeURIComponent($('answer').value.trim());
        }
        link.setAttribute('href', path.split('?')[0] + search + fragment);
      }
    });
  }
  const fmt = n => n.toFixed(6);
  const t = (zh, english) => en ? english : zh;
  function render() {
    updateLinks();
    try {
      const query = Number($('query').value), causal = $('causal').checked;
      const scores = math.SCORES[query];
      const result = math.calculate(scores, math.VALUES, 4, query, causal);
      $('rows').replaceChildren();
      result.weights.forEach((weight, j) => {
        const row = document.createElement('tr');
        const cells = [`T${j + 1}`, fmt(scores[j]), fmt(result.scaled[j]), result.allowed[j] ? t('可见', 'Visible') : t('遮罩（−∞）', 'Masked (−∞)'), fmt(result.exponentials[j]), fmt(weight), String(math.VALUES[j]), fmt(result.contributions[j])];
        cells.forEach(value => { const cell = document.createElement('td'); cell.textContent = value; row.append(cell); });
        $('rows').append(row);
      });
      $('result').hidden = false;
      $('error').textContent = '';
      $('summary').textContent = t('输出', 'Output') + ` = ${fmt(result.output)} · ` + t('权重和', 'Weight sum') + ` = ${fmt(result.weights.reduce((a,b)=>a+b,0))}`;
      $('normalizer').textContent = `m = ${fmt(result.max)}; Σ exp(sⱼ − m) = ${fmt(result.denominator)}. ` + t('屏蔽位置贡献为 0；计算使用完整精度，显示保留六位小数。', 'Masked positions contribute 0; calculations use full precision, displayed numbers have six decimals.');
    } catch (_) {
      $('result').hidden = true;
      $('rows').replaceChildren();
      $('summary').textContent = '';
      $('error').textContent = t('无法计算：输入必须为三个有限数值，配置必须有效。请点“重置实验”恢复；未保留旧结果。', 'Cannot calculate: three finite numbers and a valid configuration are required. Select Reset experiment to recover; stale results were cleared.');
    }
  }
  if ($('answer').value !== '') $('feedback').textContent = t('已保留数值答案，但尚未在此语言页面核对；请点“核对答案”。', 'Numeric answer preserved, but not checked on this language page. Select Check answer.');
  $('answer').addEventListener('input', () => { $('feedback').textContent = ''; updateLinks(); });
  $('query').addEventListener('change', render);
  $('causal').addEventListener('change', render);
  $('reset').addEventListener('click', () => { $('query').value = '0'; $('causal').checked = false; $('answer').value = ''; $('feedback').textContent = ''; render(); });
  $('check').addEventListener('click', () => {
    const state = math.checkAnswer($('answer').value);
    const messages = {
      invalid: t('请输入 −10000 到 10000 内的有限十进制数；不能为空。可清空后重新输入。', 'Enter a finite decimal number from −10000 to 10000; blank input is not valid. Clear it and try again.'),
      correct: t('正确：T1 只能看到自己，权重为 [1, 0, 0]，输出为 2。切换查询位置，观察可见集合怎样变化。', 'Correct: T1 can see only itself, so weights are [1, 0, 0] and the output is 2. Switch query positions and observe the visible set.'),
      retry: t('还不对。先选择 T1 并开启因果遮罩：哪些位置仍然可见？只对可见位置归一化，再乘对应 V。可以重试或展开解答。', 'Not yet. Select T1 and enable the causal mask: which positions remain visible? Normalize only those positions, then multiply by V. Retry or open the explanation.')
    };
    $('feedback').textContent = messages[state];
  });
  render();
})();
