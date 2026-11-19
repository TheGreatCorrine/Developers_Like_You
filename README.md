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
    data/raw/                  raw survey results (not included in the zip; see below)
    scripts/download_raw.py    downloads the 2023–2025 raw results and checks SHA-256
    scripts/build_data.py      cleans the raw results and writes data/*.csv

## Data pipeline
    python scripts/download_raw.py   # ~460 MB, official StackExchange/Survey archive
    python scripts/build_data.py     # needs pandas + numpy

| Output | Used by | Definition |
| --- | --- | --- |
| role_share.csv | Ch. 1 bars, dot clusters | DevType shares, 2024 and 2025; % of respondents who answered DevType |
| role_experience_2025.csv | Ch. 2 heatmap (D3) | Within-role % by WorkExp band, 5 roles, 2025 |
| pay_by_experience_2024.csv | Ch. 3 pay chart (D3) | ConvertedCompYearly Q1/median/Q3 by YearsCodePro band; professional developers; US and Canada |
| languages_2025.csv | Ch. 4 dumbbell | % using / wanting each language among respondents who answered either language question |
| ai_trends.csv | Ch. 5 lines | Adoption = "Yes" in AISelect / answered; trust = Somewhat+Highly trust among current users (AIBen 2023, AIAcc 2024–25) |
| ai_use_by_experience_2024.csv | Ch. 5 bars | AI adoption, professional developers, YearsCodePro 0–5 vs 6+ |
| ai_trust_by_frequency_2025.csv | draft A (process book) | Trust distribution by AI-use frequency, 2025 |
| languages_wanted_by_experience_2024.csv | draft B (process book) | Wanted languages, professional developers 0–5 vs 6+ years |

Data: Stack Overflow Annual Developer Survey, Stack Exchange Inc., ODbL 1.0 / DbCL 1.0.
