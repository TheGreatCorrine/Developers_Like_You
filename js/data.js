/* Loads the aggregated survey tables (built by scripts/build_data.py) with d3.csv
   and shapes them for the story. Every number on the page comes from here.
   Year rule: the AI trend uses 2023–2025; everything else uses 2025. */

const DATA_DIR = 'data/';
const DOT_SIZE = 100;                 // one crowd dot stands for about 100 respondents
const ALL_COUNTRIES = 'All countries';
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

/* Which six cards a reader sees. Alex (slot 3, the centre card) is always there. The other five slots each
   draw one person from that slot's pool in data/story_cards_2025.csv (20 real respondents per role, 4 per
   country); the five countries are shuffled across the five slots, so every draw spans all five countries.
   The draw is kept for 15 minutes in localStorage, so a refresh or a new tab shows the same cards.
   ?seed=<number> fixes the draw (for screenshots). */
const CARD_KEY = 'dly-cards', CARD_TTL = 15 * 60 * 1000;
function cardSeed() {
  const q = new URLSearchParams(location.search).get('seed');
  if (q !== null && /^\d+$/.test(q)) return Number(q) >>> 0;
  try {
    const s = JSON.parse(localStorage.getItem(CARD_KEY) || 'null');
    if (s && Number.isInteger(s.seed) && Date.now() - s.at >= 0 && Date.now() - s.at < CARD_TTL) return s.seed;
  } catch (e) { /* storage blocked or unreadable: draw again */ }
  const seed = Math.floor(Math.random() * 2 ** 32);
  try { localStorage.setItem(CARD_KEY, JSON.stringify({ seed, at: Date.now() })); } catch (e) { /* not stored: next visit draws again */ }
  return seed;
}
function mulberry32(a) {                // small seeded random number generator, 0 <= x < 1
  return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}
function drawCards(rows, seed) {
  const rnd = mulberry32(seed);
  const pool = rows.filter(d => d.pool === 1);
  const slots = [...new Set(pool.map(d => d.slot))].sort((a, b) => a - b);
  const countries = [...new Set(pool.map(d => d.country))];
  for (let i = countries.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [countries[i], countries[j]] = [countries[j], countries[i]]; }
  const drawn = slots.map((s, i) => { const cell = pool.filter(d => d.slot === s && d.country === countries[i]); return cell[Math.floor(rnd() * cell.length)]; });
  return rows.filter(d => d.pool === 0).concat(drawn).sort((a, b) => a.slot - b.slot);
}

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
    /* --- Chapter 1: role shares (% of respondents who reported a role) and the dot crowd (counts) --- */
    const row = role => roles.find(d => d.role === role) || { n: 0, pct_of_answered: 0 };
    const [fs, be, st] = BAR_ROLES.map(r => row(r).pct_of_answered);
    const respondents = roles[0].respondents_n;
    const totalDots = Math.round(respondents / DOT_SIZE);
    const grp = ROOM_ROLES.map(r => Math.round(row(r).n / DOT_SIZE));
    grp.push(totalDots - d3.sum(grp));              // other roles and people who gave no role

    /* --- Chapter 2: role × experience heatmap, plus one block per country for the peer locator --- */
    heatAll.sort((a, b) => d3.ascending(a.country_order, b.country_order) || d3.ascending(a.role_order, b.role_order) || d3.ascending(a.band_order, b.band_order));
    const heat = heatAll.filter(d => d.country === ALL_COUNTRIES);
    const heatRoles = [...new Set(heat.map(d => d.role))];
    const heatBands = [...new Set(heat.map(d => d.band))];
    const heatPct = d3.rollup(heat, v => v[0].pct, d => d.role, d => d.band);
    const countries = [...new Set(heatAll.map(d => d.country))];
    const heatByCountry = new Map(countries.map(c => {
      const block = heatAll.filter(d => d.country === c);
      const cell = (r, b) => block.find(d => d.role === r && d.band === b);
      return [c, {
        pct: heatRoles.map(r => heatBands.map(b => Math.round(cell(r, b).pct))),
        n: heatRoles.map(r => cell(r, heatBands[0]).role_n),
        shown: heatRoles.map(r => cell(r, heatBands[0]).displayed === 'True')
      }];
    }));

    /* --- Chapter 3: pay, US professional developers --- */
    const payUS = pay.filter(d => d.country === 'United States').sort((a, b) => a.band_order - b.band_order);

    /* --- Chapter 5: AI --- */
    ai.sort((a, b) => a.year - b.year);

    /* --- Story cards: Alex plus one drawn person for each other slot --- */
    const seed = cardSeed();
    const personas = drawCards(cards, seed).map(c => toPersona(c, heatRoles, heatBands, payUS.map(d => d.band)));

    return {
      share: { fs, be, st, other: 100 - fs - be - st },
      roomCounts: grp, totalDots,
      heat, heatRoles, heatBands, heatPct, heatByCountry, countries,
      payUS,
      langs: langs.map(d => [d.language, d.used_pct, d.want_pct]),
      ai, aiUse: ai.map(d => d.adoption_pct), aiTrust: ai.map(d => d.trust_pct),
      aiExp,
      personas, cardSeed: seed,
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
