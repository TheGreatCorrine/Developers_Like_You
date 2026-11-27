# Feature 5 · More randomness on the "Pick one" page

- Issue: [#5](https://github.com/TheGreatCorrine/Developers_Like_You/issues/5) (P2, raised by Andy)
- Branch: `feat/5-card-pool` (from `main` at `cdf00fa`; independent of #4 and #6)
- Status: implemented and checked locally; not pushed

## Goal

Readers should not all see the same six cards, while every card stays a real 2025 respondent chosen by a written rule.

## Decisions (agreed 2026-11-26)

| Topic | Decision |
| --- | --- |
| Alex | Fixed as the centre card (#336, same rule as before). The story, the `?t=` stills and the default persona stay the same. |
| Pool | 100 people: 5 roles (front-end, back-end, architect, desktop or enterprise, student) × 5 countries (Canada, United States, United Kingdom, Germany, India) × the 4 lowest `ResponseId`s that have all six card fields, selected one of four learning sources, and (developer roles) are developers by profession with a `WorkExp`. |
| Draw | One person per role slot, so the fan always shows six roles. The five countries are shuffled across the five slots, so every draw covers all five countries. |
| Learning source shown | The first the person selected of school, online courses, books, videos. |
| Names | A fixed list of 100 short names (6 letters or fewer), not matched to countries, unique within a draw. |
| Keeping the draw | `localStorage`, 15 minutes from the draw: a refresh or new tab shows the same cards; afterwards the next visit draws again. If storage is blocked, each visit draws again. `?seed=<number>` fixes the draw for screenshots and does not touch storage. |
| "Every card is a real person" | Still true: each pool row is a real 2025 record; only the name is added. Rule, counts and draw are in `data/PROVENANCE.md`. |

## Acceptance

1. `build_data.py` writes Alex plus 100 pool rows (20 per slot, 4 per slot and country) and gives identical output on a second run; no other table changes.
2. Each visit shows Alex in the centre and five pool members from five different countries; reloading within 15 minutes shows the same cards; after 15 minutes a new draw.
3. `?seed=42` always shows the same six cards.
4. Every drawn card shows the respondent's real fields; no console errors.

## Verification (2026-11-26)

Data
- `build_data.py` run twice: identical CSVs; `git diff data/` shows only `story_cards_2025.csv`.
- Pool: 101 rows (Alex + 20 per slot, 4 per slot and country); 101 different names; Alex is still #336 (6 people fit his rule).
- The candidate counts per slot and country match the separate check script run before the change (for example front-end in Canada: 23).

Page (local server, built-in browser)
- First visit with empty storage drew Alex + five cards from five countries (#2882 Germany, #132 United States, #1761 Canada, #1799 India, #1010 United Kingdom); a reload showed the same six.
- `cardSeed()`: a stored draw 14 minutes old is reused; one 16 minutes old is replaced by a new draw.
- `?seed=42` showed exactly `drawCards(rows, 42)` and left the stored draw untouched.
- 5,000 seeds: every draw valid (Alex centre, slots 0–5, five countries, six different names); all 100 pool members appear, 223–279 times each.
- The six personas of a draw build correctly (role, country, years, learning source sentence, languages, education, heatmap cell, bar, crowd group).
- No console errors; all `data/*.csv` requests 200.

Not checked
- Picking a drawn card by scrolling and clicking through the story: the browser pane ran in the background and the story did not reach the card moment in time. The click handler is unchanged from `main`; the personas it uses were checked directly.

## Recovery

Branch `feat/5-card-pool`. Rebuild the data with `python scripts/build_data.py`; see the cards with `?t=11`, or fixed with `?t=11&seed=42`. Clear `localStorage` key `dly-cards` to force a new draw.

## Merging with #4

#4 also changes `scripts/build_data.py`, `js/data.js`, `data/PROVENANCE.md` and the README. Whichever merges second resolves the overlap by merging `main` into its branch (no rebase of pushed history) and running `build_data.py` again.
