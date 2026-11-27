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

## Scope rule

- Every chart table has one block for all respondents and one per country: Canada, United States, United Kingdom, Germany and India (`country`, `country_order`). The page shows the scope the reader picks with the switch at the top right; picking a story card sets it to that person's country.
- "All respondents" includes the 13,754 people (28% of 2025) who gave no country. The country blocks only hold people who named that country. Respondents per country, 2025: Canada 1,305, United States 7,233, United Kingdom 2,042, Germany 3,025, India 2,547 (2023: 3,507, 18,647, 5,552, 7,328, 5,625; 2024: 2,104, 11,095, 3,224, 4,947, 4,231).
- Pay has country blocks only: `ConvertedCompYearly` is in US dollars, and dollar amounts from different countries are not comparable. With "All respondents" the page shows a note instead of the pay chart.
- The crowd of dots ("Who's in the room?") always uses all respondents.
- Axes and colour scales are shared by all scopes, so switching compares like with like: role bars run to 30.2% (largest full-stack share × 1.017), heatmap colours to 60% (largest cell 59.1%), languages 0–70%, AI 0–100%. Pay is the exception: each country has its own y axis.

## General rules

- A missing answer is an empty cell or the text `NA`. Missing answers are left out of the base of that question; they are never counted as "no".
- Each respondent can pick one role (`DevType`). Language and learning questions allow several picks, so those percentages do not add to 100.
- Percentages in the CSVs are 0–100 with full precision. The page rounds for display.
- A group with fewer than 30 answers is flagged `displayed=False`; the page fades it and shows its n instead of a value. One group is that small at present: India pay, 21+ years, 24 answers.
- Each survey year is a different set of volunteers. A change between years is a change between samples, not the same people changing their minds.
- These are voluntary answers. They describe the people who answered, not all developers.

## Tables

All tables are written by `scripts/build_data.py`.

### `role_share_2025.csv` · chapter 1 bars and the dot crowd

- Fields: `DevType`, `Country`, 2025.
- Bars: share of the 43,680 respondents who reported a role (`pct_of_answered`). Full-stack 12,351 (28.3%), back-end 6,453 (14.8%), student 3,008 (6.9%). 5,511 respondents gave no role. Every respondent who named one of the five countries also reported a role.
- Full-stack is the most common role in every scope:

| Scope | Reported a role | Full-stack | Back-end | Student |
| --- | ---: | ---: | ---: | ---: |
| All respondents | 43,680 | 28.3% | 14.8% | 6.9% |
| Canada | 1,305 | 29.7% | 12.1% | 6.0% |
| United States | 7,233 | 28.3% | 11.3% | 5.0% |
| United Kingdom | 2,042 | 29.2% | 15.6% | 4.1% |
| Germany | 3,025 | 28.1% | 12.5% | 7.1% |
| India | 2,547 | 27.3% | 15.0% | 14.1% |

- Dot crowd: one dot per 100 respondents, from the counts, not the percentages. 49,191 respondents give 492 dots: full-stack 124, back-end 65, student 30, front-end 20, and 253 for every other role plus people who gave no role. The page says "about 49,000".
- The published 2025 results site reports different role shares from the public CSV: full-stack 26.96%, back-end 14.17%, student 11.25% of 43,560 (`packages/archive/2025/json/developer-profile.json`). Milestone 6 of the process book quoted those. The site uses the CSV so that every number can be rebuilt. The cause of the difference was not investigated.

### `role_experience_2025.csv` · chapter 2 heatmap and the peer locator

- Fields: `DevType`, `WorkExp`, `Country`, 2025.
- `WorkExp` question: "How many years of professional work experience do you have? ... If your answer is '0', please leave blank." It counts any professional work, not only coding, and it has no "less than one year" answer. The lowest value in the file is 1.
- 2025 has no `YearsCodePro` (professional coding years). 2023 and 2024 have it, but they have no Architect role. So the role-by-experience view with Architect can only be built from 2025 `WorkExp`.
- Five roles: full-stack, back-end, front-end, architect, desktop or enterprise. Bands: 1–5, 6–10, 11–15, 16–20, 21–30, 31–40, 41–50, 50+.
- Each cell is the share of that role's respondents who gave a `WorkExp`. Base sizes for all countries: full-stack 11,982, back-end 6,272, front-end 1,872, architect 2,640, enterprise 1,849.
- The file has one block for all respondents (labelled `All respondents`; `All countries` before 2026-11-26) and one each for Canada, United States, United Kingdom, Germany and India. The smallest country group is front-end in Canada, 48 answers, so single cells there move by about two points per person. The locator prints the base size beside each result.

| Scope | Full-stack | Back-end | Front-end | Architect | Enterprise | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| All respondents | 11,982 | 6,272 | 1,872 | 2,640 | 1,849 | 24,615 |
| Canada | 383 | 157 | 48 | 62 | 81 | 731 |
| United States | 2,032 | 803 | 248 | 435 | 325 | 3,843 |
| United Kingdom | 593 | 318 | 63 | 119 | 92 | 1,185 |
| Germany | 833 | 370 | 114 | 211 | 173 | 1,701 |
| India | 619 | 353 | 147 | 147 | 56 | 1,322 |

- Chapter 2 caption. In every scope front-end and full-stack have the two highest 1–5 year shares. The page says "these roles have a lot of early-career peers" only where both are 25% or more (all respondents, Germany, India). In Canada (27% / 22%), the United States (17% / 19%) and the United Kingdom (19% / 20%) it says "more than in other roles, but most have 6+ years of experience". Architects peak at 21–30 years everywhere except India (11–15 years, still later than the other roles).

### `pay_by_experience_2025.csv` · chapter 3 pay chart

- Fields: `MainBranch`, `Country`, `WorkExp`, `ConvertedCompYearly`, 2025.
- Population: respondents who chose "I am a developer by profession", with a `WorkExp` and a pay value above zero. All five countries are in the file; the chart shows the selected country and no chart for all respondents (see the scope rule).
- `ConvertedCompYearly` is the survey's own conversion of yearly pay to US dollars. Values are nominal and self-reported.
- Bands: 1–2, 3–5, 6–10, 11–20, 21+ years. There is no under-1 band because of the `WorkExp` wording above.
- Each band has the median and the 25th and 75th percentiles (linear interpolation). The interval is the middle half of answers. It is not a confidence interval.
- US base sizes: 220, 471, 969, 1,390, 1,291. Medians: $85,000, $102,000, $150,000, $170,000, $168,000.
- Extreme values stay in. The largest 2025 value is $50,000,000; medians and quartiles are not moved by it.
- Medians (answers) by country. `*` = under 30 answers: faded on the page and labelled with n instead of a value.

| Country | 1–2 | 3–5 | 6–10 | 11–20 | 21+ |
| --- | ---: | ---: | ---: | ---: | ---: |
| Canada | $55K (42) | $66K (102) | $88K (158) | $109K (259) | $101K (208) |
| United States | $85K (220) | $102K (471) | $150K (969) | $170K (1,390) | $168K (1,291) |
| United Kingdom | $48K (72) | $68K (144) | $91K (262) | $109K (419) | $109K (371) |
| Germany | $49K (136) | $63K (266) | $81K (479) | $94K (580) | $99K (301) |
| India | $7K (182) | $12K (251) | $28K (263) | $44K (195) | $48K (24) * |

- The note beside the chart depends on the shape. Canada, United States, United Kingdom: the median peaks at 11–20 years, "then levels off". Germany: the median still rises at 21+, so the note says growth slows after 11–20 years ($81K → $94K → $99K). India: the 21+ band has 24 answers, so the note stops at 11–20 years. In every country the middle-50% ranges of 3–5 and 6–10 years overlap.

### `languages_2025.csv` · chapter 4 dumbbell

- Fields: `LanguageHaveWorkedWith`, `LanguageWantToWorkWith`, 2025.
- Base for both points: the 27,079 respondents who answered both questions. 31,671 answered "worked with"; every person who answered "want" also answered "worked with".
- "Want to work with next year" includes languages a person already uses. It measures interest, not hiring demand.
- In every scope more people want Rust and Go than use them, and JavaScript, SQL and Python are each used by more than 55%:

| Scope | Answered both | Rust used / want | Go used / want |
| --- | ---: | ---: | ---: |
| All respondents | 27,079 | 15.7% / 34.2% | 16.8% / 27.4% |
| Canada | 1,015 | 13.7% / 35.7% | 19.4% / 27.9% |
| United States | 5,602 | 18.4% / 37.6% | 19.4% / 27.4% |
| United Kingdom | 1,547 | 14.6% / 34.0% | 14.9% / 23.2% |
| Germany | 2,395 | 20.9% / 38.4% | 18.0% / 23.5% |
| India | 1,749 | 8.7% / 29.8% | 15.0% / 38.5% |

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

By scope (the same definitions):

| Scope | Use 2023 / 2024 / 2025 | Answered use | Trust 2023 / 2024 / 2025 | Users answering trust |
| --- | --- | --- | --- | --- |
| All respondents | 44.4% / 61.8% / 78.5% | 87,973 / 60,907 / 33,720 | 48.2% / 43.0% / 39.3% | 38,888 / 37,302 / 26,126 |
| Canada | 41.4% / 58.2% / 73.2% | 3,507 / 2,084 / 1,247 | 45.6% / 37.7% / 32.1% | 1,451 / 1,208 / 910 |
| United States | 39.5% / 54.2% / 72.3% | 18,647 / 11,001 / 6,938 | 47.7% / 40.3% / 35.6% | 7,346 / 5,946 / 4,987 |
| United Kingdom | 37.1% / 50.7% / 67.2% | 5,552 / 3,209 / 1,968 | 44.8% / 38.0% / 32.3% | 2,060 / 1,625 / 1,314 |
| Germany | 41.8% / 57.1% / 76.1% | 7,328 / 4,911 / 2,932 | 37.6% / 32.8% / 27.7% | 3,065 / 2,797 / 2,212 |
| India | 46.4% / 67.9% / 86.8% | 5,625 / 4,161 / 2,274 | 63.7% / 59.1% / 60.4% | 2,585 / 2,802 / 1,893 |

Use rises every year in every scope. Trust falls every year except in India, where it went from 59.1% to 60.4% between 2024 and 2025; there the headline says trust "hasn't kept up" instead of "is falling". In Germany use was already above trust in 2023, so the shaded gap starts at 2023.

### `ai_use_by_experience_2025.csv` · chapter 5 bars

- Fields: `MainBranch`, `WorkExp`, `AISelect`, 2025.
- Professional developers who answered the use question and gave a `WorkExp`. 1–5 years: 85.2% of 6,377. 6 or more years: 79.3% of 19,022.
- `gap_pts` is 1–5 minus 6+ years, in points; `gap_lo`/`gap_hi` is its 95% interval (difference of two independent proportions, normal approximation, z = 1.96). The page says "Newer developers use AI more" only when the whole interval is above zero, and "About the same at both career stages" when it includes zero.

| Scope | 1–5 years | 6+ years | Gap (95% interval) | Page says |
| --- | ---: | ---: | ---: | --- |
| All respondents | 85.2% of 6,377 | 79.3% of 19,022 | +5.9 (+4.9 to +7.0) | newer use more |
| Canada | 80.1% of 191 | 76.0% of 757 | +4.1 (−2.3 to +10.6) | about the same |
| United States | 76.4% of 849 | 75.2% of 4,394 | +1.3 (−1.9 to +4.4) | about the same |
| United Kingdom | 72.8% of 268 | 69.8% of 1,258 | +3.0 (−2.9 to +8.9) | about the same |
| Germany | 78.9% of 521 | 76.9% of 1,696 | +1.9 (−2.1 to +6.0) | about the same |
| India | 92.0% of 728 | 86.4% of 823 | +5.6 (+2.6 to +8.7) | newer use more |

### `ai_trust_by_frequency_2025.csv` · draft A, not on the page yet

- Fields: `AISelect`, `AIAcc`, 2025. Respondents who answered both. Five trust answers within each of five use groups, including the two groups that do not use AI.

### `languages_wanted_by_experience_2025.csv` · draft B, not on the page yet

- Fields: `MainBranch`, `WorkExp`, `LanguageWantToWorkWith`, 2025. Professional developers with a `WorkExp` who answered the want question: 5,300 with 1–5 years, 15,331 with 6 or more.

### `story_cards_2025.csv` · the six cards at the start

Each card is one real 2025 respondent. The only thing added is the first name.

Selection: for each card, take every 2025 respondent who fits the rule below and has all six card fields filled in, then keep the lowest `ResponseId`. Nobody was picked by hand after that.

| Name | Role | Country | Work experience | Education starts with | Learning source selected | Fits rule | Chosen |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| Maya | Developer, front-end | India | 3–5 | Bachelor | Online courses | 4 | #26886 |
| Sam | Developer, back-end | Germany | 6–10 | Master | School | 3 | #2733 |
| Priya | Architect | United States | 21–30 | Master | Books | 7 | #421 |
| Alex | Developer, full-stack | Canada | 1–2 | Bachelor | School | 6 | #336 |
| Jordan | Developer, desktop or enterprise | United Kingdom | 11–15 | Bachelor | Videos | 1 | #13635 |
| Lee | Student | Canada | any | any | School | 42 | #553 |

Alex must also be a developer by profession.

What the card shows:

- Years coding: `YearsCode`, which includes years in education.
- Learned from: the 2025 question is "How did you learn to code in the past year?". The card shows the source named in the rule and how many other sources the person ticked. It does not say how the person first learned to code.
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

## What changed for the country switch (2026-11-26, Issue #4)

| Item | Before | Now |
| --- | --- | --- |
| Scope of the charts | all respondents, pay United States only, locator with its own country menu | one switch for every chart: all respondents or one of five countries; starts at the picked person's country |
| All-respondents label | `All countries` | `All respondents` (28% gave no country) |
| Role shares, languages, AI trend, AI by experience | all respondents only | plus five countries |
| Pay | United States and Canada | five countries; none for all respondents |
| AI by experience | two shares | plus the gap and its 95% interval |
| Language axis | 10–70% | 0–70% (India Rust use is 8.7%) |
| Heatmap colours | 0 to the largest all-respondents cell (35.1%) | 0–60% for every scope |
| All-respondents values | — | unchanged; every all-respondents row equals the earlier file |

## Checking

`scripts/build_data.py` run twice on the hashed raw files gives byte-identical CSVs.

On 2026-11-26 a separate pandas script (not sharing code with the build script) recomputed every per-country number above from the raw files: role shares, heatmap bases and peaks, pay medians and quartiles, language shares, AI use and trust per year, and AI use by experience. All values match the CSVs.

A second calculation that shares no code with the build script (Python standard library only, reading the raw CSVs directly) reproduces all nine tables: 344 rows, 1,926 cells, no differences. It re-selects the six story cards from the written rule and compares each field with the raw record.
