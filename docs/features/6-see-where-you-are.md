# Feature 6 · Last section: "See where you are"

- Issue: [#6](https://github.com/TheGreatCorrine/Developers_Like_You/issues/6)
- Branch: `feat/6-see-where-you-are`, on top of `feat/4-country-scope` (the pages follow the country switch from #4)
- Status: implemented and checked locally; not pushed

## Goal

End the story by putting the reader into two charts they have already seen, instead of promising a career plan the data cannot give.

## Decisions (agreed 2026-11-26)

| Topic | Decision |
| --- | --- |
| Name | Chapter label `YOUR TURN` (was `NEXT STEP`), heading "See where you are" (was "Make your own career plan"). |
| Pages | Two pages, no new chart types. Page 1: role share bars. Page 2: role × experience heatmap. |
| Roles | The five developer roles of the heatmap, in the heatmap's order, so a role sits in the same row on both pages. Students are not offered: the heatmap has no student row (its first band starts at one year of work). The menu asks for the role you have or want. |
| Input | Each page asks one thing and answers it at once: page 1 a role menu, page 2 an experience menu. Both start at the picked card (Alex: full-stack, 1–5 years). The country comes from the switch. |
| Page 1 | Bars in the same style and scale as Chapter 1. The reader's role is orange with a "You" tag; the others are navy. A sentence gives the share and the rank among the five roles. |
| Page 2 | Heatmap in the same style and colour scale as Chapter 2. The reader's cell is outlined with a "You" tag and the others are dimmed; the share and its base appear below (the old peer-locator sentence). A role with under 30 answers shows "—" and its n. |
| Closing quote | Moves to the start of S13, above the title; the title block moves down about 60 px. |
| S11 | Ends with "→ Where do you stand?" (echoes the S13 title). |
| Timeline | The section grows by about 10 s. New moments: page 1 `?t=143`, page 2 `?t=153`, end `?t=161`. |

## Acceptance

1. S12 shows two pages with the names above; the old "career plan" wording is gone.
2. Changing the role menu moves the orange bar and "You" tag on page 1 and the outlined row on page 2; changing the experience menu moves the outlined cell; the numbers match `data/role_share_2025.csv` and `data/role_experience_2025.csv` for the selected scope.
3. Changing the country switch updates both pages.
4. S13 opens with the quote, then the title block; nothing overlaps.
5. No console errors; all `data/*.csv` requests 200; no text overflows in any of the six scopes.

## Verification (2026-11-26)

Page (local server, built-in browser)
- `?t=143`, `?t=153`, `?t=161`, `?t=135` render page 1, page 2, the end and the S11 arrow as designed; no console errors; all `data/*.csv` requests 200.
- In all six scopes, three role/experience pairs each (front-end 1–5, enterprise 50+, architect 21–30): exactly one orange bar, the outline on the chosen cell, the chosen row label in bold, and the sentences name the right scope. Shares and ranks match `role_share_2025.csv` (e.g. Canada front-end 3.8%, least common; India front-end 6.4%, 3rd) and cell values match `role_experience_2025.csv`.
- Choosing a role through the real menu (India, enterprise / desktop, 2.4%) moves the bar highlight and "You" tag; the tag stays readable on a short bar.
- No text overflows in any scope.

Not checked
- The scroll path between the pages was not watched at full speed (the browser pane was in the background); positions were checked at fixed moments.

## Recovery

Branch `feat/6-see-where-you-are` (parent `feat/4-country-scope`). Page: `python -m http.server 8000`, then `?t=143` / `?t=153` / `?t=161`, optionally `&country=<name>`.
