import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "gross_enrollment_data.csv"


def load_data():
    return pd.read_csv(DATA_FILE)

def get_entity(name):
    df = load_data()

    name = name.strip().lower()

    column = df["Countries/States"].astype(str)
    normalized = column.str.lower()

    # Prefer an exact match.
    exact = df[normalized == name]

    if not exact.empty:
        return exact

    # Otherwise allow partial matching.
    matches = df[normalized.str.contains(name, na=False)]

    return matches

def get_change(name):
    matches = get_entity(name)

    if matches.empty:
        return None

    results = []

    for _, row in matches.iterrows():
        old = pd.to_numeric(
            row["1999-2000 (Percentage)"],
            errors="coerce"
        )

        new = pd.to_numeric(
            row["2009-10 (Percentage)"],
            errors="coerce"
        )

        if pd.isna(old) or pd.isna(new):
            continue

        results.append({
            "entity": row["Countries/States"],
            "old_value": float(old),
            "new_value": float(new),
            "change": float(new - old),
        })

    return results


def get_highest_improvement():
    df = load_data().copy()

    df["old"] = pd.to_numeric(
        df["1999-2000 (Percentage)"],
        errors="coerce"
    )

    df["new"] = pd.to_numeric(
        df["2009-10 (Percentage)"],
        errors="coerce"
    )

    df["change"] = df["new"] - df["old"]

    df = df.dropna(subset=["change"])

    row = df.loc[df["change"].idxmax()]

    return {
        "entity": row["Countries/States"],
        "old_value": float(row["old"]),
        "new_value": float(row["new"]),
        "change": float(row["change"]),
    }

def compare_entities(name1, name2):
    first = get_change(name1)
    second = get_change(name2)

    if not first:
        return f"No data found for {name1}."

    if not second:
        return f"No data found for {name2}."

    a = first[0]
    b = second[0]

    difference_old = a["old_value"] - b["old_value"]
    difference_new = a["new_value"] - b["new_value"]

    return {
        "first": a,
        "second": b,
        "difference_1999": difference_old,
        "difference_2009": difference_new,
    }


def rank_entities():
    df = load_data().copy()

    df["old"] = pd.to_numeric(
        df["1999-2000 (Percentage)"],
        errors="coerce"
    )

    df["new"] = pd.to_numeric(
        df["2009-10 (Percentage)"],
        errors="coerce"
    )

    df = df.dropna(subset=["old", "new"])

    df["change"] = df["new"] - df["old"]

    return df.sort_values("new", ascending=False)[
        [
            "Countries/States",
            "old",
            "new",
            "change",
        ]
    ].to_dict("records")

def get_value_for_year(name, year):
    matches = get_entity(name)

    if matches.empty:
        return None

    if year == "1999-2000":
        column = "1999-2000 (Percentage)"
    elif year == "2009-10":
        column = "2009-10 (Percentage)"
    else:
        return None

    results = []

    for _, row in matches.iterrows():
        value = pd.to_numeric(row[column], errors="coerce")

        if pd.isna(value):
            continue

        results.append({
            "entity": row["Countries/States"],
            "year": year,
            "value": float(value),
        })

    return results

