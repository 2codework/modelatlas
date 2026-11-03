/* Original teaching arithmetic, not model parameters. No I/O or dependencies. */
(function (root) {
  'use strict';
  const SCORES = Object.freeze([Object.freeze([0, 2 * Math.log(2), 2 * Math.log(3)]), Object.freeze([2, 0, -2]), Object.freeze([0, 0, 0])]);
  const VALUES = Object.freeze([2, 6, 10]);
  function vector(values) {
    if (!Array.isArray(values) || values.length !== 3 || !values.every(x => typeof x === 'number' && Number.isFinite(x) && Math.abs(x) <= 10000)) throw new Error('values');
  }
  function calculate(scores, values, dimension, query, causal) {
    vector(scores); vector(values);
    if (!Number.isInteger(dimension) || dimension < 1 || dimension > 1024 || !Number.isInteger(query) || query < 0 || query > 2 || typeof causal !== 'boolean') throw new Error('configuration');
    const scaled = scores.map(x => x / Math.sqrt(dimension));
    const allowed = scaled.map((_, j) => !causal || j <= query);
    const max = Math.max(...scaled.filter((_, j) => allowed[j]));
    // Exclude masked positions rather than passing Infinity through public inputs.
    const exponentials = scaled.map((x, j) => allowed[j] ? Math.exp(x - max) : 0);
    const denominator = exponentials.reduce((a, b) => a + b, 0);
    const weights = exponentials.map(x => x / denominator);
    const contributions = weights.map((x, j) => x * values[j]);
    const output = contributions.reduce((a, b) => a + b, 0);
    if (![...weights, output].every(Number.isFinite)) throw new Error('result');
    return {scaled, allowed, max, exponentials, denominator, weights, contributions, output};
  }
  function checkAnswer(raw) {
    if (typeof raw !== 'string' || raw.trim() === '' || !/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/.test(raw.trim())) return 'invalid';
    const n = Number(raw);
    if (!Number.isFinite(n) || Math.abs(n) > 10000) return 'invalid';
    return Math.abs(n - 2) < 0.000001 ? 'correct' : 'retry';
  }
  const api = Object.freeze({SCORES, VALUES, calculate, checkAnswer});
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.AttentionMath = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
