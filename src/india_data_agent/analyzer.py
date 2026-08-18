import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "gross_enrollment_data.csv"


def load_data():
    return pd.read_csv(DATA_FILE)


def show_country(name):
    df = load_data()

    matches = df[
        df["Countries/States"]
        .astype(str)
        .str.contains(name, case=False, na=False)
    ]

    if matches.empty:
        return f"No data found for {name}."

    output = []

    for _, row in matches.iterrows():
        old = row["1999-2000 (Percentage)"]
        new = row["2009-10 (Percentage)"]

        if pd.isna(old) or pd.isna(new):
            output.append(
                f"{row['Countries/States']}: "
                f"1999-2000={old}, 2009-10={new}"
            )
        else:
            change = new - old
            output.append(
                f"{row['Countries/States']}: "
                f"{old:.1f}% → {new:.1f}% "
                f"(change: {change:+.1f} percentage points)"
            )

    return "\n".join(output)


def highest_improvement():
    df = load_data().copy()

    df["old"] = pd.to_numeric(
        df["1999-2000 (Percentage)"], errors="coerce"
    )
    df["new"] = pd.to_numeric(
        df["2009-10 (Percentage)"], errors="coerce"
    )

    df["change"] = df["new"] - df["old"]

    row = df.loc[df["change"].idxmax()]

    return (
        f"Highest improvement: {row['Countries/States']} "
        f"with an increase of {row['change']:.1f} percentage points."
    )


def world_average():
    df = load_data()

    row = df[
        df["Countries/States"]
        .astype(str)
        .str.contains("World Average", case=False, na=False)
    ]

    if row.empty:
        return "World Average data not found."

    row = row.iloc[0]

    return (
        f"World Average: "
        f"{row['1999-2000 (Percentage)']}% in 1999-2000 → "
        f"{row['2009-10 (Percentage)']}% in 2009-10."
    )