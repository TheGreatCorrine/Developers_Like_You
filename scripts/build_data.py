"""Build the aggregated CSVs used by the website from the raw Stack Overflow survey files.

Input : data/raw/results_{2023,2024,2025}.csv  (official StackExchange/Survey archive, commit 32a1145)
Output: data/*.csv  (small, chart-ready tables loaded by the site with d3.csv)

Run from the prototype folder:  python scripts/build_data.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data"
PRO = "I am a developer by profession"


def load(year, cols):
    return pd.read_csv(RAW / f"results_{year}.csv", usecols=cols, low_memory=False)


def years_to_num(s):
    """YearsCodePro / WorkExp come as text ('Less than 1 year', 'More than 50 years') or numbers."""
    s = s.replace({"Less than 1 year": 0.5, "More than 50 years": 51})
    return pd.to_numeric(s, errors="coerce")


def split_multi(s):
    return s.dropna().str.split(";")


# ---------------------------------------------------------------- 1. role shares
def role_shares():
    rows = []
    for year in (2024, 2025):
        d = load(year, ["DevType"])
        n_all = len(d)
        ans = d["DevType"].dropna()
        vc = ans.value_counts()
        for role, n in vc.items():
            rows.append(dict(year=year, role=role, n=int(n), answered_n=len(ans), respondents_n=n_all,
                             pct_of_answered=100 * n / len(ans), pct_of_all=100 * n / n_all))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "role_share.csv", index=False)
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
    d = load(2025, ["DevType", "WorkExp"])
    d = d[d["DevType"].isin(ROLE_MAP)].copy()
    d["exp"] = years_to_num(d["WorkExp"])
    d = d.dropna(subset=["exp"])
    d["band"] = d["exp"].apply(band_of)
    d["role"] = d["DevType"].map(ROLE_MAP)
    rows = []
    for r_i, role in enumerate(ROLE_MAP.values()):
        sub = d[d.role == role]
        for b_i, (_, _, lab) in enumerate(BANDS):
            n = int((sub.band == lab).sum())
            rows.append(dict(role=role, role_order=r_i, band=lab, band_order=b_i, n=n,
                             role_n=len(sub), pct=100 * n / len(sub)))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "role_experience_2025.csv", index=False)
    return df


# ---------------------------------------------------------------- 3. pay by experience (US, 2024)
PAY_BANDS = [(-1, 0.99, "<1"), (0.99, 2, "1–2"), (2, 5, "3–5"), (5, 10, "6–10"), (10, 20, "11–20"), (20, 1e9, "21+")]


def pay():
    d = load(2024, ["MainBranch", "Country", "YearsCodePro", "ConvertedCompYearly"])
    d = d[(d.MainBranch == PRO)].copy()
    d["exp"] = years_to_num(d["YearsCodePro"])
    rows = []
    for country in ["United States of America", "Canada"]:
        c = d[(d.Country == country)].dropna(subset=["exp", "ConvertedCompYearly"])
        for i, (lo, hi, lab) in enumerate(PAY_BANDS):
            v = c[(c.exp > lo) & (c.exp <= hi)]["ConvertedCompYearly"]
            q1, med, q3 = np.percentile(v, [25, 50, 75]) if len(v) else (np.nan,) * 3
            rows.append(dict(country="United States" if country.startswith("United") else country,
                             band=lab, band_order=i, n=len(v), q1=q1, median=med, q3=q3,
                             displayed=len(v) >= 30))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "pay_by_experience_2024.csv", index=False)
    return df


# ---------------------------------------------------------------- 4. languages: used vs wanted (2025)
LANGS = ["Python", "SQL", "HTML/CSS", "JavaScript", "TypeScript", "Rust", "Bash/Shell (all shells)", "Go"]


def languages():
    d = load(2025, ["LanguageHaveWorkedWith", "LanguageWantToWorkWith"])
    base = d[d.LanguageHaveWorkedWith.notna() | d.LanguageWantToWorkWith.notna()]
    used = split_multi(base.LanguageHaveWorkedWith).explode().value_counts()
    want = split_multi(base.LanguageWantToWorkWith).explode().value_counts()
    rows = [dict(language=l.replace(" (all shells)", ""), used_pct=100 * used.get(l, 0) / len(base),
                 want_pct=100 * want.get(l, 0) / len(base), denominator_n=len(base)) for l in LANGS]
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "languages_2025.csv", index=False)
    return df


# ---------------------------------------------------------------- 5. AI adoption + trust (2023-2025)
TRUST_FIELD = {2023: "AIBen", 2024: "AIAcc", 2025: "AIAcc"}


def ai_trends():
    rows = []
    for year in (2023, 2024, 2025):
        f = TRUST_FIELD[year]
        d = load(year, ["AISelect", f])
        ans = d[d.AISelect.notna()]
        users = ans[ans.AISelect.str.startswith("Yes")]
        t = users[f].dropna()
        trust = t.isin(["Somewhat trust", "Highly trust"]).sum()
        rows.append(dict(year=year, respondents_n=len(d), use_answered_n=len(ans), users_n=len(users),
                         adoption_pct=100 * len(users) / len(ans), trust_answered_n=len(t),
                         trust_pct=100 * trust / len(t), trust_field=f))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "ai_trends.csv", index=False)
    return df


def ai_by_experience():
    d = load(2024, ["MainBranch", "YearsCodePro", "AISelect"])
    d = d[(d.MainBranch == PRO) & d.AISelect.notna()].copy()
    d["exp"] = years_to_num(d["YearsCodePro"])
    d = d.dropna(subset=["exp"])
    rows = []
    for lab, m in [("0–5 years", d.exp <= 5), ("6+ years", d.exp > 5)]:
        s = d[m]
        rows.append(dict(group=lab, n=len(s), use_pct=100 * s.AISelect.str.startswith("Yes").mean()))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "ai_use_by_experience_2024.csv", index=False)
    return df


TRUST_ORDER = ["Highly distrust", "Somewhat distrust", "Neither trust nor distrust", "Somewhat trust", "Highly trust"]
FREQ = {"Yes, I use AI tools daily": "Daily", "Yes, I use AI tools weekly": "Weekly",
        "Yes, I use AI tools monthly or infrequently": "Monthly or less",
        "No, but I plan to soon": "Not yet, planning", "No, and I don't plan to": "No plans"}


def trust_by_frequency():
    d = load(2025, ["AISelect", "AIAcc"]).dropna()
    rows = []
    for i, (k, lab) in enumerate(FREQ.items()):
        s = d[d.AISelect == k]
        for j, t in enumerate(TRUST_ORDER):
            rows.append(dict(frequency=lab, freq_order=i, trust=t, trust_order=j,
                             n=int((s.AIAcc == t).sum()), group_n=len(s), pct=100 * (s.AIAcc == t).mean()))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "ai_trust_by_frequency_2025.csv", index=False)
    return df


# ---------------------------------------------------------------- 7. wanted languages by experience (2024, draft B)
def languages_by_experience():
    d = load(2024, ["MainBranch", "YearsCodePro", "LanguageWantToWorkWith"])
    d = d[d.MainBranch == PRO].copy()
    d["exp"] = years_to_num(d["YearsCodePro"])
    d = d.dropna(subset=["exp"])
    rows = []
    for lab, m in [("0–5 years", d.exp <= 5), ("6+ years", d.exp > 5)]:
        base = d[m & d.LanguageWantToWorkWith.notna()]
        vc = split_multi(base.LanguageWantToWorkWith).explode().value_counts()
        for l in ["Python", "JavaScript", "TypeScript", "SQL", "HTML/CSS", "Rust", "Go", "Java", "C#"]:
            rows.append(dict(group=lab, language=l, want_pct=100 * vc.get(l, 0) / len(base), n=len(base)))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "languages_wanted_by_experience_2024.csv", index=False)
    return df


if __name__ == "__main__":
    pd.set_option("display.width", 160)
    for fn in [role_shares, heatmap, pay, languages, ai_trends, ai_by_experience, trust_by_frequency, languages_by_experience]:
        df = fn()
        print(f"\n== {fn.__name__}: {len(df)} rows")
        if fn is role_shares:
            print(df[df.year == 2025].head(8).round(2).to_string(index=False))
            print(df[df.year == 2024].head(8).round(2).to_string(index=False))
        elif fn is heatmap:
            print(df.pivot(index="role", columns="band", values="pct")[[b[2] for b in BANDS]].round(0).to_string())
        else:
            print(df.round(1).to_string(index=False))
