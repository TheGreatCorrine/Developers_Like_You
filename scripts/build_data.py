"""Build the aggregated CSVs used by the website from the raw Stack Overflow survey files.

Input : data/raw/results_{2023,2024,2025}.csv  (official StackExchange/Survey archive, commit 32a1145)
Output: data/*.csv  (small, chart-ready tables loaded by the site with d3.csv)

Year rule: the AI trend uses 2023-2025. Every other table uses 2025 only.
Scope rule: the tables behind the story charts have one block for all respondents and one per country in
COUNTRIES (pay: countries only, because pay in USD is not comparable across countries).
Definitions, denominators and caveats for each table are in data/PROVENANCE.md.

Run from the prototype folder:  python scripts/build_data.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data"
YEAR = 2025
TREND_YEARS = (2023, 2024, 2025)
PRO = "I am a developer by profession"
MIN_N = 30          # groups smaller than this are flagged displayed=False

# long survey labels -> short labels used on the page
COUNTRIES = {
    "Canada": "Canada",
    "United States of America": "United States",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "Germany": "Germany",
    "India": "India",
}
ALL_COUNTRIES = "All respondents"   # includes the 28% of 2025 respondents who gave no country
Z95 = 1.96                          # two-sided 95% normal interval


def load(year, cols):
    return pd.read_csv(RAW / f"results_{year}.csv", usecols=cols, low_memory=False)


def scopes(d):
    """(order, label, rows): all respondents first, then one block per country in COUNTRIES order."""
    yield 0, ALL_COUNTRIES, d
    for i, (full, short) in enumerate(COUNTRIES.items(), start=1):
        yield i, short, d[d.Country == full]


def work_years(s):
    """2025 WorkExp: whole years of professional work experience. Blank means no answer or zero years."""
    return pd.to_numeric(s, errors="coerce")


def split_multi(s):
    return s.dropna().str.split(";")


# ---------------------------------------------------------------- 1. role shares (2025)
def role_shares():
    d = load(YEAR, ["DevType", "Country"])
    rows = []
    for c_i, country, s in scopes(d):
        ans = s["DevType"].dropna()
        rows += [dict(country=country, country_order=c_i, year=YEAR, role=role, n=int(n), answered_n=len(ans),
                      respondents_n=len(s), pct_of_answered=100 * n / len(ans), pct_of_all=100 * n / len(s))
                 for role, n in ans.value_counts().items()]
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "role_share_2025.csv", index=False)
    return df


# ---------------------------------------------------------------- 2. role x experience heatmap (2025)
ROLE_MAP = {
    "Developer, full-stack": "Full-stack",
    "Developer, back-end": "Back-end",
    "Developer, front-end": "Front-end",
    "Architect, software or solutions": "Architect",
    "Developer, desktop or enterprise applications": "Enterprise / desktop",
}
BANDS = [(0, 5, "1–5"), (5, 10, "6–10"), (10, 15, "11–15"), (15, 20, "16–20"),
         (20, 30, "21–30"), (30, 40, "31–40"), (40, 50, "41–50"), (50, 1e9, "50+")]


def band_of(x):
    for lo, hi, lab in BANDS:
        if lo < x <= hi:
            return lab
    return None


def heatmap():
    """Within each role, the share of respondents in each WorkExp band. One block for all
    respondents and one per country."""
    d = load(YEAR, ["DevType", "WorkExp", "Country"])
    d = d[d["DevType"].isin(ROLE_MAP)].copy()
    d["exp"] = work_years(d["WorkExp"])
    d = d.dropna(subset=["exp"])
    d["band"] = d["exp"].apply(band_of)
    d["role"] = d["DevType"].map(ROLE_MAP)
    rows = []
    for c_i, country, block in scopes(d):
        for r_i, role in enumerate(ROLE_MAP.values()):
            sub = block[block.role == role]
            for b_i, (_, _, lab) in enumerate(BANDS):
                n = int((sub.band == lab).sum())
                rows.append(dict(country=country, country_order=c_i, role=role, role_order=r_i, band=lab, band_order=b_i,
                                 n=n, role_n=len(sub), pct=100 * n / len(sub), displayed=len(sub) >= MIN_N))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "role_experience_2025.csv", index=False)
    return df


# ---------------------------------------------------------------- 3. pay by experience (2025)
# 2025 has no "less than 1 year" answer, so the first band starts at 1.
PAY_BANDS = [(0, 2, "1–2"), (2, 5, "3–5"), (5, 10, "6–10"), (10, 20, "11–20"), (20, 1e9, "21+")]


def pay():
    d = load(YEAR, ["MainBranch", "Country", "WorkExp", "ConvertedCompYearly"])
    d = d[d.MainBranch == PRO].copy()
    d["exp"] = work_years(d["WorkExp"])
    d = d.dropna(subset=["exp", "ConvertedCompYearly"])
    d = d[d.ConvertedCompYearly > 0]
    rows = []
    for c_i, country, c in list(scopes(d))[1:]:          # countries only: USD pay is not comparable across countries
        for i, (lo, hi, lab) in enumerate(PAY_BANDS):
            v = c[(c.exp > lo) & (c.exp <= hi)]["ConvertedCompYearly"]
            q1, med, q3 = np.percentile(v, [25, 50, 75]) if len(v) else (np.nan,) * 3
            rows.append(dict(country=country, country_order=c_i, band=lab, band_order=i, n=len(v), q1=q1, median=med,
                             q3=q3, displayed=len(v) >= MIN_N))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "pay_by_experience_2025.csv", index=False)
    return df


# ---------------------------------------------------------------- 4. languages: used vs wanted (2025)
LANGS = ["Python", "SQL", "HTML/CSS", "JavaScript", "TypeScript", "Rust", "Bash/Shell (all shells)", "Go"]


def languages():
    """Both percentages use the same people: respondents who answered both language questions."""
    d = load(YEAR, ["LanguageHaveWorkedWith", "LanguageWantToWorkWith", "Country"])
    both = d[d.LanguageHaveWorkedWith.notna() & d.LanguageWantToWorkWith.notna()]
    rows = []
    for c_i, country, base in scopes(both):
        used = split_multi(base.LanguageHaveWorkedWith).explode().value_counts()
        want = split_multi(base.LanguageWantToWorkWith).explode().value_counts()
        rows += [dict(country=country, country_order=c_i, language=l.replace(" (all shells)", ""),
                      used_n=int(used.get(l, 0)), want_n=int(want.get(l, 0)),
                      used_pct=100 * used.get(l, 0) / len(base), want_pct=100 * want.get(l, 0) / len(base),
                      denominator_n=len(base)) for l in LANGS]
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "languages_2025.csv", index=False)
    return df


# ---------------------------------------------------------------- 5. AI adoption + trust (2023-2025)
TRUST_FIELD = {2023: "AIBen", 2024: "AIAcc", 2025: "AIAcc"}   # same question, column renamed after 2023


def ai_trends():
    rows = []
    for year in TREND_YEARS:
        f = TRUST_FIELD[year]
        for c_i, country, d in scopes(load(year, ["AISelect", f, "Country"])):
            ans = d[d.AISelect.notna()]
            users = ans[ans.AISelect.str.startswith("Yes")]
            t = users[f].dropna()
            trust = t.isin(["Somewhat trust", "Highly trust"]).sum()
            rows.append(dict(country=country, country_order=c_i, year=year, respondents_n=len(d),
                             use_answered_n=len(ans), users_n=len(users), adoption_pct=100 * len(users) / len(ans),
                             trust_answered_n=len(t), trust_pct=100 * trust / len(t), trust_field=f))
    df = pd.DataFrame(rows).sort_values(["country_order", "year"])
    df.to_csv(OUT / "ai_trends.csv", index=False)
    return df


# ---------------------------------------------------------------- 6. AI use by experience (2025)
def ai_by_experience():
    """AI use, 1-5 vs 6+ years of work. gap_* is the difference (1-5 minus 6+) in points with a 95% interval
    (difference of two independent proportions, normal approximation); the page only says one group uses AI
    more when the interval does not include zero."""
    d = load(YEAR, ["MainBranch", "WorkExp", "AISelect", "Country"])
    d = d[(d.MainBranch == PRO) & d.AISelect.notna()].copy()
    d["exp"] = work_years(d["WorkExp"])
    d = d.dropna(subset=["exp"])
    rows = []
    for c_i, country, s in scopes(d):
        groups = [(lab, s[m]) for lab, m in [("1–5 years", s.exp <= 5), ("6+ years", s.exp > 5)]]
        p = [g.AISelect.str.startswith("Yes").mean() for _, g in groups]
        n = [len(g) for _, g in groups]
        gap = 100 * (p[0] - p[1])
        half = 100 * Z95 * np.sqrt(p[0] * (1 - p[0]) / n[0] + p[1] * (1 - p[1]) / n[1])
        for (lab, _), n_i, p_i in zip(groups, n, p):
            rows.append(dict(country=country, country_order=c_i, group=lab, n=n_i, use_pct=100 * p_i,
                             gap_pts=gap, gap_lo=gap - half, gap_hi=gap + half))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "ai_use_by_experience_2025.csv", index=False)
    return df


# ---------------------------------------------------------------- 7. trust by AI-use frequency (2025, draft A)
TRUST_ORDER = ["Highly distrust", "Somewhat distrust", "Neither trust nor distrust", "Somewhat trust", "Highly trust"]
FREQ = {"Yes, I use AI tools daily": "Daily", "Yes, I use AI tools weekly": "Weekly",
        "Yes, I use AI tools monthly or infrequently": "Monthly or less",
        "No, but I plan to soon": "Not yet, planning", "No, and I don't plan to": "No plans"}


def trust_by_frequency():
    d = load(YEAR, ["AISelect", "AIAcc"]).dropna()
    rows = []
    for i, (k, lab) in enumerate(FREQ.items()):
        s = d[d.AISelect == k]
        for j, t in enumerate(TRUST_ORDER):
            rows.append(dict(frequency=lab, freq_order=i, trust=t, trust_order=j,
                             n=int((s.AIAcc == t).sum()), group_n=len(s), pct=100 * (s.AIAcc == t).mean()))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "ai_trust_by_frequency_2025.csv", index=False)
    return df


# ---------------------------------------------------------------- 8. wanted languages by experience (2025, draft B)
def languages_by_experience():
    d = load(YEAR, ["MainBranch", "WorkExp", "LanguageWantToWorkWith"])
    d = d[d.MainBranch == PRO].copy()
    d["exp"] = work_years(d["WorkExp"])
    d = d.dropna(subset=["exp"])
    rows = []
    for lab, m in [("1–5 years", d.exp <= 5), ("6+ years", d.exp > 5)]:
        base = d[m & d.LanguageWantToWorkWith.notna()]
        vc = split_multi(base.LanguageWantToWorkWith).explode().value_counts()
        for l in ["Python", "JavaScript", "TypeScript", "SQL", "HTML/CSS", "Rust", "Go", "Java", "C#"]:
            rows.append(dict(group=lab, language=l, want_pct=100 * vc.get(l, 0) / len(base), n=len(base)))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "languages_wanted_by_experience_2025.csv", index=False)
    return df


# ---------------------------------------------------------------- 9. story cards: six real respondents (2025)
SCHOOL = "School (i.e., University, College, etc)"
COURSES = "Online Courses or Certification (includes all media types)"
BOOKS = "Books / Physical media"
VIDEOS = "Videos (not associated with specific online course or certification)"
# Each card is the lowest ResponseId that fits its rule. Only the name is added by us.
#   exp  = WorkExp range, inclusive (None = not required)
#   edu  = start of the EdLevel answer (None = any)
#   learn = a learning source the respondent selected for the past year; it is the one shown on the card
STORY_CARDS = [
    dict(name="Maya", role="Developer, front-end", country="India", exp=(3, 5), edu="Bachelor", learn=COURSES, main=None),
    dict(name="Sam", role="Developer, back-end", country="Germany", exp=(6, 10), edu="Master", learn=SCHOOL, main=None),
    dict(name="Priya", role="Architect, software or solutions", country="United States of America", exp=(21, 30), edu="Master", learn=BOOKS, main=None),
    dict(name="Alex", role="Developer, full-stack", country="Canada", exp=(1, 2), edu="Bachelor", learn=SCHOOL, main=PRO),
    dict(name="Jordan", role="Developer, desktop or enterprise applications", country="United Kingdom of Great Britain and Northern Ireland", exp=(11, 15), edu="Bachelor", learn=VIDEOS, main=None),
    dict(name="Lee", role="Student", country="Canada", exp=None, edu=None, learn=SCHOOL, main=None),
]
CARD_FIELDS = ["DevType", "YearsCode", "LearnCode", "LanguageHaveWorkedWith", "EdLevel", "Country"]


def story_cards():
    d = load(YEAR, ["ResponseId", "MainBranch", "WorkExp"] + CARD_FIELDS)
    d["exp"] = work_years(d["WorkExp"])
    complete = d.dropna(subset=CARD_FIELDS)
    rows = []
    for i, c in enumerate(STORY_CARDS):
        m = (complete.DevType == c["role"]) & (complete.Country == c["country"])
        m &= complete.LearnCode.str.split(";").apply(lambda picks: c["learn"] in picks)
        if c["exp"]:
            m &= complete.exp.between(*c["exp"])
        if c["edu"]:
            m &= complete.EdLevel.str.startswith(c["edu"])
        if c["main"]:
            m &= complete.MainBranch == c["main"]
        found = complete[m].sort_values("ResponseId")
        r = found.iloc[0]
        has_exp = not pd.isna(r.exp)
        rows.append(dict(card_order=i, name=c["name"], response_id=int(r.ResponseId), candidates_n=len(found),
                         main_branch=r.MainBranch, dev_type=r.DevType,
                         work_exp=int(r.exp) if has_exp else "", years_code=int(float(r.YearsCode)),
                         learn_featured=c["learn"], learn_selected_n=len(r.LearnCode.split(";")),
                         languages=r.LanguageHaveWorkedWith, ed_level=r.EdLevel, country=r.Country,
                         # where this person sits in the heatmap and the pay chart (same bands as those tables)
                         heat_role=ROLE_MAP.get(r.DevType, ""), heat_band=band_of(r.exp) if has_exp else "",
                         pay_band=next((lab for lo, hi, lab in PAY_BANDS if lo < r.exp <= hi), "") if has_exp else ""))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "story_cards_2025.csv", index=False)
    return df


if __name__ == "__main__":
    pd.set_option("display.width", 200)
    for fn in [role_shares, heatmap, pay, languages, ai_trends, ai_by_experience, trust_by_frequency,
               languages_by_experience, story_cards]:
        df = fn()
        print(f"\n== {fn.__name__}: {len(df)} rows")
        if fn is role_shares:
            print(df.head(8).round(2).to_string(index=False))
        elif fn is heatmap:
            top = df[df.country == ALL_COUNTRIES]
            print(top.pivot(index="role", columns="band", values="pct")[[b[2] for b in BANDS]].round(0).to_string())
        else:
            print(df.round(1).to_string(index=False))
