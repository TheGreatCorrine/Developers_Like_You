/* Loads the aggregated survey tables (built by scripts/build_data.py) with d3.csv
   and shapes them for the story. Every number on the page comes from here.
   Year rule: the AI trend uses 2023–2025; everything else uses 2025.
   Scope rule: every chart table has one block for all respondents and one per country;
   the crowd of dots always uses all respondents. */

const DATA_DIR = 'data/';
const DOT_SIZE = 100;                 // one crowd dot stands for about 100 respondents
const ALL_COUNTRIES = 'All respondents';   // includes the 28% of 2025 respondents who gave no country
const ROOM_ROLES = ['Developer, full-stack', 'Developer, back-end', 'Student', 'Developer, front-end'];   // dot groups; a fifth group holds everyone else
const BAR_ROLES = ['Developer, full-stack', 'Developer, back-end', 'Student'];                            // bars in chapter 1

/* Short forms of long survey answers, used on the story cards. */
const ROLE_SHORT = { 'Developer, desktop or enterprise applications': 'Developer, desktop or enterprise' };
const COUNTRY_SHORT = { 'United States of America': 'United States', 'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom' };
const LEARN = {   // 2025 question: "How did you learn to code in the past year?"  answer -> [card label, sentence]
  'School (i.e., University, College, etc)': ['School', 'learned new coding skills in school this past year'],
  'Online Courses or Certification (includes all media types)': ['Online courses', 'learned new coding skills from online courses this past year'],
  'Books / Physical media': ['Books', 'learned new coding skills from books this past year'],
  'Videos (not associated with specific online course or certification)': ['Videos', 'learned new coding skills from videos this past year']
};

/* One story card = one real 2025 respondent (data/story_cards_2025.csv). Only the name is added. */
function toPersona(c, heatRoles, heatBands, payBands) {
  const langs = String(c.languages).split(';').map(s => s.replace(' (all shells)', ''));
  // the card row holds about 34 characters: show up to three languages, then how many more
  const langLine = k => langs.slice(0, k).join(' · ') + (langs.length > k ? `  +${langs.length - k} more` : '');
  let k = Math.min(3, langs.length);
  while (k > 1 && langLine(k).length > 34) k--;
  const [learnLabel, phrase] = LEARN[c.learn_featured];
  const others = c.learn_selected_n - 1;
  const room = ROOM_ROLES.indexOf(c.dev_type);
  const hr = heatRoles.indexOf(c.heat_role), hb = heatBands.indexOf(c.heat_band);
  return {
    id: '#' + c.response_id, name: c.name,
    kind: c.dev_type === 'Student' ? 'student' : 'developer',
    role: ROLE_SHORT[c.dev_type] || c.dev_type,
    years: String(c.years_code),
    learned: learnLabel + (others > 0 ? ` (+${others} more), past year` : ', past year'),
    phrase,
    langs: langLine(k),
    edu: String(c.ed_level).replace(/\s*\(.*\)$/, '').replace('Some college/university study without earning a degree', 'Some college, no degree'),
    country: COUNTRY_SHORT[c.country] || c.country,
    room: room < 0 ? ROOM_ROLES.length : room,
    bar: BAR_ROLES.indexOf(c.dev_type),
    heat: hr >= 0 && hb >= 0 ? [hr, hb] : null,
    pay: Math.max(0, payBands.indexOf(c.pay_band))
  };
}

function loadData() {
  const num = d => { for (const k in d) { if (d[k] !== '' && !isNaN(+d[k])) d[k] = +d[k]; } return d; };
  return Promise.all([
    d3.csv(DATA_DIR + 'role_share_2025.csv', num),
    d3.csv(DATA_DIR + 'role_experience_2025.csv', num),
    d3.csv(DATA_DIR + 'pay_by_experience_2025.csv', num),
    d3.csv(DATA_DIR + 'languages_2025.csv', num),
    d3.csv(DATA_DIR + 'ai_trends.csv', num),
    d3.csv(DATA_DIR + 'ai_use_by_experience_2025.csv', num),
    d3.csv(DATA_DIR + 'story_cards_2025.csv', num)
  ]).then(([roles, heatAll, pay, langs, ai, aiExp, cards]) => {
    const order = (...keys) => (a, b) => { for (const k of keys) { const c = d3.ascending(a[k], b[k]); if (c) return c; } return 0; };
    heatAll.sort(order('country_order', 'role_order', 'band_order'));
    pay.sort(order('country_order', 'band_order'));
    ai.sort(order('country_order', 'year'));
    const countries = [...new Set(heatAll.map(d => d.country))];      // 'All respondents' first, then the five countries
    const heatRoles = [...new Set(heatAll.map(d => d.role))];
    const heatBands = [...new Set(heatAll.map(d => d.band))];
    const payBands = [...new Set(pay.map(d => d.band))];

    /* --- Crowd of dots: always all respondents, from counts --- */
    const allRoles = roles.filter(d => d.country === ALL_COUNTRIES);
    const countOf = role => (allRoles.find(d => d.role === role) || { n: 0 }).n;
    const respondents = allRoles[0].respondents_n;
    const totalDots = Math.round(respondents / DOT_SIZE);
    const grp = ROOM_ROLES.map(r => Math.round(countOf(r) / DOT_SIZE));
    grp.push(totalDots - d3.sum(grp));              // other roles and people who gave no role

    /* --- One object per scope. Every chart reads the scope the reader has selected. All scopes have the
       same shape (pay is null for all respondents) so the page can ease from one to another. --- */
    const scopes = new Map(countries.map(c => {
      const rs = roles.filter(d => d.country === c);
      const share = role => (rs.find(d => d.role === role) || { pct_of_answered: 0 }).pct_of_answered;
      const [fs, be, st] = BAR_ROLES.map(share);
      const hb = heatAll.filter(d => d.country === c);
      const cell = (r, b) => hb.find(d => d.role === r && d.band === b);
      const roleN = heatRoles.map(r => cell(r, heatBands[0]).role_n);
      const pb = pay.filter(d => d.country === c);
      const lg = langs.filter(d => d.country === c);
      const ay = ai.filter(d => d.country === c);
      const ae = aiExp.filter(d => d.country === c);
      return [c, {
        name: c,
        // chapter 1: % of respondents who reported a role
        bars: { fs, be, st, other: 100 - fs - be - st, n: rs[0].answered_n },
        // chapter 2: within-role % by WorkExp band
        heat: {
          pct: heatRoles.map(r => heatBands.map(b => cell(r, b).pct)),
          cnt: heatRoles.map(r => heatBands.map(b => cell(r, b).n)),
          n: roleN, total: d3.sum(roleN),
          shown: heatRoles.map(r => cell(r, heatBands[0]).displayed === 'True')
        },
        // chapter 3: professional developers, USD; countries only
        pay: pb.length ? pb.map(d => ({ band: d.band, n: d.n, q1: d.q1, median: d.median, q3: d.q3, shown: d.displayed === 'True' })) : null,
        // chapter 4: same base for both points
        langs: lg.map(d => ({ name: d.language, used: d.used_pct, want: d.want_pct })), langN: lg[0].denominator_n,
        // chapter 5: use of those who answered; trust of current users who answered
        ai: { use: ay.map(d => d.adoption_pct), trust: ay.map(d => d.trust_pct), n: ay.map(d => d.use_answered_n) },
        aiExp: ae.map(d => ({ group: d.group, n: d.n, use: d.use_pct })),
        aiGap: { pts: ae[0].gap_pts, lo: ae[0].gap_lo, hi: ae[0].gap_hi }     // 1–5 minus 6+ years, 95% interval
      }];
    }));

    /* --- Story cards --- */
    cards.sort((a, b) => a.card_order - b.card_order);
    const personas = cards.map(c => toPersona(c, heatRoles, heatBands, payBands));

    return {
      roomCounts: grp, totalDots,
      countries, scopes, heatRoles, heatBands, payBands,
      aiYears: [...new Set(ai.map(d => d.year))],
      personas,
      respondents,
      aboutN: Math.round(respondents / 1000) * 1000
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
