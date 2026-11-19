/* Loads the aggregated survey tables (built by scripts/build_data.py) with d3.csv
   and shapes them for the story. Every number on the page comes from here. */

const DATA_DIR = 'data/';

function loadData() {
  const num = d => { for (const k in d) { if (k !== 'year' && d[k] !== '' && !isNaN(+d[k])) d[k] = +d[k]; } d.year = +d.year || d.year; return d; };
  return Promise.all([
    d3.csv(DATA_DIR + 'role_share.csv', num),
    d3.csv(DATA_DIR + 'role_experience_2025.csv', num),
    d3.csv(DATA_DIR + 'pay_by_experience_2024.csv', num),
    d3.csv(DATA_DIR + 'languages_2025.csv', num),
    d3.csv(DATA_DIR + 'ai_trends.csv', num),
    d3.csv(DATA_DIR + 'ai_use_by_experience_2024.csv', num)
  ]).then(([roles, heat, pay, langs, ai, aiExp]) => {
    /* --- Chapter 1: role shares (2025, % of respondents who answered DevType) --- */
    const r25 = roles.filter(d => d.year === 2025);
    const share = role => (r25.find(d => d.role === role) || { pct_of_answered: 0 }).pct_of_answered;
    const fs = share('Developer, full-stack'), be = share('Developer, back-end'),
          st = share('Student'), fe = share('Developer, front-end');
    // 650 dots ≈ 2024 respondents / 100; grouped by 2025 role shares
    const N = 650, grp = [fs, be, st, fe].map(p => Math.round(N * p / 100));
    grp.push(N - d3.sum(grp));

    /* --- Chapter 2: role × experience heatmap --- */
    heat.sort((a, b) => d3.ascending(a.role_order, b.role_order) || d3.ascending(a.band_order, b.band_order));
    const heatRoles = [...new Set(heat.map(d => d.role))];
    const heatBands = [...new Set(heat.map(d => d.band))];
    const heatPct = d3.rollup(heat, v => v[0].pct, d => d.role, d => d.band);

    /* --- Chapter 3: pay, US professional developers 2024 --- */
    const payUS = pay.filter(d => d.country === 'United States').sort((a, b) => a.band_order - b.band_order);

    /* --- Chapter 5: AI --- */
    ai.sort((a, b) => a.year - b.year);
    const n2024 = ai.find(d => d.year === 2024).respondents_n;

    return {
      share: { fs, be, st, fe, other: 100 - fs - be - st },
      roomCounts: grp,
      heat, heatRoles, heatBands, heatPct,
      payUS,
      langs: langs.map(d => [d.language, d.used_pct, d.want_pct]),
      ai, aiUse: ai.map(d => d.adoption_pct), aiTrust: ai.map(d => d.trust_pct),
      aiExp,
      respondents2024: n2024,
      aboutN: Math.round(n2024 / 1000) * 1000
    };
  });
}

function showDataError(err) {
  console.error(err);
  const box = document.createElement('div');
  box.style.cssText = 'position:fixed;inset:auto 16px 16px 16px;z-index:99;background:#1f2944;color:#fff;font:15px/1.5 Inter,sans-serif;padding:14px 18px;border-radius:8px';
  box.innerHTML = location.protocol === 'file:'
    ? 'The charts load their data with <code>d3.csv</code>, which browsers block on <code>file://</code>. From this folder run <code>python -m http.server</code> and open <code>http://localhost:8000</code>.'
    : 'Could not load the survey data files in <code>data/</code>: ' + err.message;
  document.body.appendChild(box);
}
