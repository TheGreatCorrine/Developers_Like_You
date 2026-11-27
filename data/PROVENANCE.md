# Data provenance

Notes on where every number on the site comes from. The page itself only carries short labels; the detail is here.

Last checked: 2026-11-26.

## Source

Stack Overflow Annual Developer Survey, public respondent-level files, from the official archive `github.com/StackExchange/Survey`, pinned to commit `32a114542da67e3759479637343718502742adfd`.

| Year | File | Rows | Bytes | SHA-256 |
| --- | --- | ---: | ---: | --- |
| 2023 | `packages/archive/2023/results.csv` | 89,184 | 158,626,799 | `828874a3cf0fa1bbb4c3da6a87e5822b8563bbc04b21f9869479480dbcff410c` |
| 2024 | `packages/archive/2024/results.csv` | 65,437 | 159,525,875 | `7f2c2dbf6989d00b80a7351de4bb3af4b52b21cc52d5c947891bbc4f4e5cbe49` |
| 2025 | `packages/archive/2025/results.csv` | 49,191 | 140,893,245 | `2d1f65308877282edfb4470520eabbc08cb499118432a3dcec6a66c086aa2baa` |

`scripts/download_raw.py` downloads the three files and checks these hashes. The same hashes are recorded in the archive's Git LFS pointers at the pinned commit and at the later commit `9dd5c163` linked in the process book, so both links point at identical data.

Licence: database ODbL 1.0, contents DbCL 1.0. Attribution: Stack Overflow Developer Survey, Stack Exchange Inc.

## Year rule

- AI trend: 2023, 2024 and 2025.
- Everything else: 2025 only, the most recent complete year.

2026 is not used. The archive published 2026 results on 2026-10-13 (`packages/archive/2026/survey_results_public.csv`, 122,407,316 bytes). The team decided on 2026-11-19 to stay with 2025; the reason given was that the 2026 file held only about 30,000 respondents at that point. That count is the team's reading and was not rechecked here.

## General rules

- A missing answer is an empty cell or the text `NA`. Missing answers are left out of the base of that question; they are never counted as "no".
- Each respondent can pick one role (`DevType`). Language and learning questions allow several picks, so those percentages do not add to 100.
- Percentages in the CSVs are 0–100 with full precision. The page rounds for display.
- A group with fewer than 30 answers is flagged `displayed=False`. No group on the site is that small at present.
- Each survey year is a different set of volunteers. A change between years is a change between samples, not the same people changing their minds.
- These are voluntary answers. They describe the people who answered, not all developers.

## Tables

All tables are written by `scripts/build_data.py`.

### `role_share_2025.csv` · chapter 1 bars and the dot crowd

- Field: `DevType`, 2025.
- Bars: share of the 43,680 respondents who reported a role (`pct_of_answered`). Full-stack 12,351 (28.3%), back-end 6,453 (14.8%), student 3,008 (6.9%). 5,511 respondents gave no role.
- Dot crowd: one dot per 100 respondents, from the counts, not the percentages. 49,191 respondents give 492 dots: full-stack 124, back-end 65, student 30, front-end 20, and 253 for every other role plus people who gave no role. The page says "about 49,000".
- The published 2025 results site reports different role shares from the public CSV: full-stack 26.96%, back-end 14.17%, student 11.25% of 43,560 (`packages/archive/2025/json/developer-profile.json`). Milestone 6 of the process book quoted those. The site uses the CSV so that every number can be rebuilt. The cause of the difference was not investigated.

### `role_experience_2025.csv` · chapter 2 heatmap and the peer locator

- Fields: `DevType`, `WorkExp`, `Country`, 2025.
- `WorkExp` question: "How many years of professional work experience do you have? ... If your answer is '0', please leave blank." It counts any professional work, not only coding, and it has no "less than one year" answer. The lowest value in the file is 1.
- 2025 has no `YearsCodePro` (professional coding years). 2023 and 2024 have it, but they have no Architect role. So the role-by-experience view with Architect can only be built from 2025 `WorkExp`.
- Five roles: full-stack, back-end, front-end, architect, desktop or enterprise. Bands: 1–5, 6–10, 11–15, 16–20, 21–30, 31–40, 41–50, 50+.
- Each cell is the share of that role's respondents who gave a `WorkExp`. Base sizes for all countries: full-stack 11,982, back-end 6,272, front-end 1,872, architect 2,640, enterprise 1,849.
- The file has one block for all respondents and one each for Canada, United States, United Kingdom, Germany and India. 13,754 respondents (28%) gave no country; they are in the all-respondents block only. The smallest country group is front-end in Canada, 48 answers, so single cells there move by about two points per person. The locator prints the base size beside each result.

### `pay_by_experience_2025.csv` · chapter 3 pay chart

- Fields: `MainBranch`, `Country`, `WorkExp`, `ConvertedCompYearly`, 2025.
- Population: respondents who chose "I am a developer by profession", with a `WorkExp` and a pay value above zero. United States and Canada are in the file; the chart shows the United States.
- `ConvertedCompYearly` is the survey's own conversion of yearly pay to US dollars. Values are nominal and self-reported.
- Bands: 1–2, 3–5, 6–10, 11–20, 21+ years. There is no under-1 band because of the `WorkExp` wording above.
- Each band has the median and the 25th and 75th percentiles (linear interpolation). The interval is the middle half of answers. It is not a confidence interval.
- US base sizes: 220, 471, 969, 1,390, 1,291. Medians: $85,000, $102,000, $150,000, $170,000, $168,000.
- Extreme values stay in. The largest 2025 value is $50,000,000; medians and quartiles are not moved by it.

### `languages_2025.csv` · chapter 4 dumbbell

- Fields: `LanguageHaveWorkedWith`, `LanguageWantToWorkWith`, 2025.
- Base for both points: the 27,079 respondents who answered both questions. 31,671 answered "worked with"; every person who answered "want" also answered "worked with".
- "Want to work with next year" includes languages a person already uses. It measures interest, not hiring demand.

### `ai_trends.csv` · chapter 5 lines

- Fields: `AISelect` for use; trust is `AIBen` in 2023 and `AIAcc` in 2024 and 2025. The trust question has the same wording in all three years ("How much do you trust the accuracy of the output from AI tools as part of your development workflow?"); only the column name changed.
- Use line: answers starting with "Yes", out of respondents who answered `AISelect`. 2025 splits "Yes" into daily, weekly and monthly; these are added together.
- Trust line: "Somewhat trust" plus "Highly trust", out of current users who answered the trust question.
- The two lines have different bases. The chart subtitle says so.

| Year | Respondents | Answered use | Skipped use | Current users | Use | Users answering trust | Trust |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023 | 89,184 | 87,973 | 1.4% | 39,042 | 44.4% | 38,888 | 48.2% |
| 2024 | 65,437 | 60,907 | 6.9% | 37,662 | 61.8% | 37,302 | 43.0% |
| 2025 | 49,191 | 33,720 | 31.5% | 26,469 | 78.5% | 26,126 | 39.3% |

Far more people skipped the use question in 2025. If skipped answers were counted in the base, 2025 use would be 53.8%. The rise from 2024 to 2025 may be partly an effect of who stayed to answer.

### `ai_use_by_experience_2025.csv` · chapter 5 bars

- Fields: `MainBranch`, `WorkExp`, `AISelect`, 2025.
- Professional developers who answered the use question and gave a `WorkExp`. 1–5 years: 85.2% of 6,377. 6 or more years: 79.3% of 19,022.

### `ai_trust_by_frequency_2025.csv` · draft A, not on the page yet

- Fields: `AISelect`, `AIAcc`, 2025. Respondents who answered both. Five trust answers within each of five use groups, including the two groups that do not use AI.

### `languages_wanted_by_experience_2025.csv` · draft B, not on the page yet

- Fields: `MainBranch`, `WorkExp`, `LanguageWantToWorkWith`, 2025. Professional developers with a `WorkExp` who answered the want question: 5,300 with 1–5 years, 15,331 with 6 or more.

### `story_cards_2025.csv` · the cards at the start

Each card is one real 2025 respondent. The only thing added is the first name. The file holds Alex plus a pool of 100 people; each reader sees Alex and five people drawn from the pool.

Alex, the story's main person, is always the centre card (`slot` 3, `pool` 0): the lowest `ResponseId` among respondents with all six card fields who fit this rule.

| Name | Role | Country | Work experience | Education starts with | Learning source selected | Developer by profession | Fits rule | Chosen |
| --- | --- | --- | --- | --- | --- | --- | ---: | --- |
| Alex | Developer, full-stack | Canada | 1–2 | Bachelor | School | yes | 6 | #336 |

The pool (`pool` 1) has one slot per card position: front-end (slot 0), back-end (1), architect (2), desktop or enterprise (4), student (5). For each slot and each of the five countries it holds the four lowest `ResponseId`s among respondents who:

- have that role and country, and all six card fields filled in;
- selected at least one of four past-year learning sources: school, online courses, books, videos;
- for the four developer slots: chose "I am a developer by profession" and gave a `WorkExp`.

That is 5 slots × 5 countries × 4 = 100 people. Nobody was picked by hand. People who fit each slot and country (`candidates_n`):

| Slot | Canada | United States | United Kingdom | Germany | India |
| --- | ---: | ---: | ---: | ---: | ---: |
| Front-end | 23 | 111 | 29 | 46 | 61 |
| Back-end | 67 | 322 | 122 | 150 | 170 |
| Architect | 25 | 169 | 42 | 86 | 60 |
| Desktop or enterprise | 33 | 134 | 38 | 84 | 33 |
| Student | 56 | 247 | 55 | 145 | 227 |

The draw happens in the reader's browser (`js/data.js`). The five countries are shuffled across the five slots, then one of the four people in each slot-and-country cell is chosen, so every set of cards covers all five countries. The draw is kept in the browser's `localStorage` for 15 minutes, so a refresh or a new tab shows the same cards; after that the next visit draws again. `?seed=<number>` always gives the same draw (for screenshots). In a check of 5,000 draws every draw was valid and all 100 people appeared, each 223–279 times.

Names: a fixed list of 100 short first names, not matched to countries, given in pool order; Alex keeps the same name. No two cards in one draw share a name.

What the card shows:

- Years coding: `YearsCode`, which includes years in education.
- Learned from: the 2025 question is "How did you learn to code in the past year?". The card shows one source the person selected (Alex: school; pool: the first of school, online courses, books, videos that the person ticked) and how many other sources the person ticked. It does not say how the person first learned to code.
- Languages: the first few from `LanguageHaveWorkedWith` in the survey's own order, with a count of the rest. The order is not a ranking.
- The marker that follows the chosen person through the heatmap and the pay chart uses that person's own role and `WorkExp` (columns `heat_role`, `heat_band`, `pay_band`).

## What changed from Prototype 1

| Item | Prototype 1 | Now |
| --- | --- | --- |
| Crowd size | 2024, about 65,000, grouped by 2025 shares | 2025, about 49,000, grouped by 2025 counts |
| Story cards | invented profiles with real-looking IDs | six real 2025 respondents, chosen by rule |
| Pay chart | 2024, `YearsCodePro`, six bands from under 1; US medians $65K to $172K | 2025, `WorkExp`, five bands from 1–2; US medians $85K to $168K |
| Language "want" base | 31,671 (answered either question) | 27,079 (answered both) |
| Language values, used / want | Python 58.1 / 39.2, Rust 14.9 / 29.2, Go 16.5 / 23.4 | Python 58.6 / 45.9, Rust 15.7 / 34.2, Go 16.8 / 27.4 |
| AI use by experience | 2024, coding years 0–5 vs 6+: 70.7% vs 57.6% | 2025, work years 1–5 vs 6+: 85.2% vs 79.3% |
| Wanted languages by experience | 2024 | 2025 |
| Peer locator country menu | listed five countries, changed nothing | all countries plus five, changes the result and shows the base |
| Role shares, heatmap, AI trend | 2025; 2023–2025 | same values |

## What changed for the card pool (2026-11-26, Issue #5)

| Item | Before | Now |
| --- | --- | --- |
| Cards a reader sees | the same six for everyone: Maya #26886, Sam #2733, Priya #421, Alex #336, Jordan #13635, Lee #553 | Alex #336 in the centre plus five drawn from a pool of 100, one per role, all five countries |
| Selection rule | one written rule per card (role, country, experience, education, learning source) | Alex unchanged; pool: role, country, complete card fields, a learning source, professional developers with `WorkExp` |
| Columns | `card_order` | `slot`, `pool` (0 = Alex, 1 = pool) |

## Checking

`scripts/build_data.py` run twice on the hashed raw files gives byte-identical CSVs.

A second calculation that shares no code with the build script (Python standard library only, reading the raw CSVs directly) reproduces all nine tables: 344 rows, 1,926 cells, no differences. It re-selects the six story cards from the written rule and compares each field with the raw record. (That check was run on 2026-11-19, before the card pool. The pool's candidate counts were recomputed separately on 2026-11-26 and match the table above.)
