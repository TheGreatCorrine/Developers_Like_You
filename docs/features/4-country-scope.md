# Feature 4 · Country scope on every chart, one country switch

- Issue: [#4](https://github.com/TheGreatCorrine/Developers_Like_You/issues/4)
- Branch: `feat/4-country-scope` (from `main` at `cdf00fa`)
- Status: implemented and checked locally; not pushed
- Follow-ups that build on this: #6 (last section) uses the same switch.

## Goal

Readers always know whose answers a chart shows, and can look at one country across the whole story.

## Decisions (agreed 2026-11-26)

| Topic | Decision |
| --- | --- |
| Default country | The picked card's country (Alex → Canada). The reader can change it at any time. Before a card is picked (and on `?t=` stills) the default is Alex's, Canada. |
| Country list | All respondents + the current five: Canada, United States, United Kingdom, Germany, India. |
| Crowd of dots (intro, "Who's in the room?") | Stays all 2025 respondents and says so (`ALL RESPONDENTS · 2025 · N = 49,191`). The switch first appears with the Chapter 1 bars. |
| Switch | Top right of the stage, `SHOWING` + a menu, visible from the Chapter 1 bars to the end of S12. On its first appearance a hint underneath says whose country it is (`Alex's country · change it any time`). |
| Scope label | Each chart subtitle starts with its scope in navy: `CANADA · 2025 · N = 1,305`, then the existing measure text in grey. N is that chart's own base. The AI trend shows one N per year. |
| "All respondents" | 13,754 people (28%) gave no country, so the all-scope is called "All respondents", not "All countries". |
| Sentences | Claims are recomputed for the selected scope. Where a claim does not hold in a scope, a prewritten sentence that matches the data is shown instead (see below). |
| Pay chart with All respondents | No chart: pay in USD is not comparable across countries. A note with five country buttons replaces it. |
| Axes and colour scales | Shared by all six scopes so switching is a fair comparison: role bars 0–30.2% (largest full-stack share × 1.017), heatmap colours 0–60%, languages 0–70%, AI 0–100%. Pay is the exception: each country gets its own axis. |
| Switching | Chart values ease to the new scope over about 0.6 s; the frame does not flash. |
| Small groups | A group under 30 answers is faded and shows its n instead of a value (existing rule). First case: India pay, 21+ years, n = 24. |
| Roadmap (S11) | Unchanged and unlabelled: all four milestones hold in all six scopes (checked below). |
| Peer locator (S12) | Uses the global switch; its own location menu is removed. (#6 replaces this section.) |
| Testing aid | `?country=<name>` sets the starting scope, like `?t=`. Example: `?t=88&country=India`. |
| AI use by experience | "Newer developers use AI more" only when the 95% interval of the gap (1–5 years minus 6+ years) is above zero; otherwise "About the same at both career stages". The interval is computed in `scripts/build_data.py`. |

## Claims checked per scope (2025 unless noted)

An independent script (standard pandas, not sharing code with `build_data.py`) recomputed every claim from the hashed raw files.

| Claim | All | CA | US | UK | DE | IN |
| --- | --- | --- | --- | --- | --- | --- |
| Full-stack is the most common role | yes | yes | yes | yes | yes | yes |
| Front-end and full-stack have the two highest 1–5 year shares | yes | yes | yes | yes | yes | yes |
| … and both shares are 25% or more | yes | no (27 / 22) | no (17 / 19) | no (19 / 20) | yes | yes |
| Architects peak later than other roles | 21–30 | 21–30 | 21–30 | 21–30 | 21–30 | 11–15 |
| Median pay peaks before the last band | — | yes | yes | yes | no, growth slows | last band n = 24 |
| 3–5 and 6–10 middle-50% ranges overlap | — | yes | yes | yes | yes | yes |
| Rust and Go: want > use | yes | yes | yes | yes | yes | yes |
| JavaScript, SQL, Python used by over 55% | yes | yes | yes | yes | yes | yes |
| AI use rises every year (2023–2025) | yes | yes | yes | yes | yes | yes |
| AI trust falls every year (2023–2025) | yes | yes | yes | yes | yes | no (59.1 → 60.4) |
| Newer developers use AI more (95% interval above 0) | yes (+5.9) | no (+4.1) | no (+1.3) | no (+3.0) | no (+1.9) | yes (+5.6) |

## Sentence variants

| Place | Holds | Otherwise |
| --- | --- | --- |
| Ch. 2 caption 1 | "These roles have a lot of early-career peers." | "More than in other roles, but most have 6+ years of experience." |
| Ch. 3 pay note | "Median pay rises from ~A to ~B by C years, then levels off." | Peak in last band: "Median pay rises from ~A to ~B. Growth slows after 11–20 years." · Last band under 30: "Median pay rises from ~A to ~B by C years. Too few answers after that." |
| Ch. 5 headline | "…but trust is falling." | "…but trust hasn't kept up." |
| Ch. 5 panel | "Newer developers use AI more." | "About the same at both career stages." |

## Acceptance

1. Every chart from Chapter 1 to S12 shows its scope; the crowd says "All respondents".
2. Changing the switch updates every chart, caption and sentence; values ease, no flash, no console errors.
3. Picking a card sets the switch to that person's country.
4. With All respondents the pay chart shows the note and five buttons; a button sets that country.
5. Data: `build_data.py` run twice gives identical files; every new number matches the independent check; `PROVENANCE.md` and the README table describe the new tables.
6. Layout: no sentence or subtitle overflows in any of the six scopes.

## Verification (2026-11-26)

Data
- Raw files downloaded with `scripts/download_raw.py`; all three SHA-256 hashes match.
- `scripts/build_data.py` run twice: identical CSVs.
- Regression: in every changed table the `All respondents` rows equal the previous file (role experience: only the label changed); US and Canada pay rows unchanged.
- Every per-country number matches the independent check script (results in the table above and in `data/PROVENANCE.md`).

Page (local server, built-in browser; `?t=<s>&country=<name>`)
- All six scopes, chapters 1–5 and S12: subtitles, captions and variant sentences read as listed above; chart values after switching equal the CSVs (bars, heatmap row, pay medians, Rust/Go, AI points, AI by experience).
- No text overflows its box or the stage in any scope.
- Picking Maya sets the switch to India and the hint to "Maya's country"; picking Priya sets United States. Changing the switch by hand hides the hint.
- "All respondents" on the pay chart shows the note; the Germany button sets Germany and the chart returns with its own axis.
- India pay 21+ (n = 24) is faded and labelled `n = 24`; the note stops at 11–20 years.
- Germany AI: the shaded gap starts at 2023; first-year labels do not overlap.
- Console: no errors; all `data/*.csv` requests 200.
- `?t=` stills keep the animation loop, so the switch also eases there.

Not checked
- The 0.6 s ease was confirmed from intermediate values, not watched on screen (the browser pane was in the background, which slows animation frames).
- Screenshots were taken at the pane's small size; layout was measured in stage pixels.
- A browser that cached the old `index.html` or `js/data.js` shows an error until a hard refresh. The local server sends no cache headers.

## Recovery

Everything is on `feat/4-country-scope`. Raw files: `python scripts/download_raw.py` (SHA-256 checked). Data: `python scripts/build_data.py`. Page: `python -m http.server 8000`, then `?t=<seconds>&country=<name>`.
