# Where Do We Stand? — Prototype 1 (CSC316, Fall 2026)

Corrine Xiang · Andy Chen · Clovis Zhu

A scroll-driven data story that follows Alex, one survey respondent, from a single file to a career roadmap.

## Run it
The page loads its data with `d3.csv`, which browsers block on `file://`. From this folder:

    python -m http.server 8000
    # open http://localhost:8000

Add `?t=64` to the URL to jump to a moment on the story timeline (in seconds).

## Folder layout
    index.html                 story page (layout, scroll timeline, all scenes)
    js/data.js                 loads data/*.csv with d3.csv and shapes it for the scenes
    js/vendor/d3.v7.9.0.min.js D3 v7.9.0 (bundled so the page works offline)
    data/*.csv                 aggregated, chart-ready tables (output of the pipeline)
    data/PROVENANCE.md         where each number comes from: source, base, caveats
    data/raw/                  raw survey results (not included in the zip; see below)
    scripts/download_raw.py    downloads the 2023–2025 raw results and checks SHA-256
    scripts/build_data.py      cleans the raw results and writes data/*.csv

## Data pipeline
    python scripts/download_raw.py   # ~460 MB, official StackExchange/Survey archive
    python scripts/build_data.py     # needs pandas + numpy

Year rule: the AI trend uses 2023–2025. Every other table uses 2025, the most recent complete year.

| Output | Used by | Definition |
| --- | --- | --- |
| role_share_2025.csv | Ch. 1 bars, dot crowd | DevType, 2025; bars are % of respondents who reported a role, dots are counts (1 dot per 100 respondents) |
| role_experience_2025.csv | Ch. 2 heatmap (D3), peer locator | Within-role % by WorkExp band, 5 roles, 2025; all respondents plus 5 countries |
| pay_by_experience_2025.csv | Ch. 3 pay chart (D3) | ConvertedCompYearly Q1/median/Q3 by WorkExp band; professional developers; US and Canada |
| languages_2025.csv | Ch. 4 dumbbell | % using / wanting each language among respondents who answered both language questions |
| ai_trends.csv | Ch. 5 lines | Adoption = "Yes" in AISelect / answered; trust = Somewhat+Highly trust among current users (AIBen 2023, AIAcc 2024–25) |
| ai_use_by_experience_2025.csv | Ch. 5 bars | AI adoption, professional developers, WorkExp 1–5 vs 6+ |
| story_cards_2025.csv | Opening cards | Alex (lowest ResponseId that fits a written rule) plus a pool of 100 real 2025 respondents: 5 roles × 5 countries × the 4 lowest ResponseIds; each reader sees Alex and 5 drawn cards (kept 15 minutes; `?seed=` fixes the draw) |
| ai_trust_by_frequency_2025.csv | draft A (process book) | Trust distribution by AI-use frequency, 2025 |
| languages_wanted_by_experience_2025.csv | draft B (process book) | Wanted languages, professional developers, WorkExp 1–5 vs 6+ |

Sources, question wording, bases, sample sizes and caveats for each table are in [data/PROVENANCE.md](data/PROVENANCE.md).

Data: Stack Overflow Annual Developer Survey, Stack Exchange Inc., ODbL 1.0 / DbCL 1.0.
