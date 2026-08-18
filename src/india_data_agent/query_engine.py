import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "gross_enrollment_data.csv"


def load_data():
    with DATA_FILE.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def find_country_or_state(name):
    rows = load_data()
    name = name.lower().strip(" ?.,!")

    matches = [
        row for row in rows
        if name in row["Countries/States"].lower()
    ]

    return matches


def compare(name):
    matches = find_country_or_state(name)

    if not matches:
        return f"No data found for {name}."

    results = []

    for row in matches:
        old = row["1999-2000 (Percentage)"]
        new = row["2009-10 (Percentage)"]

        try:
            old_value = float(old)
            new_value = float(new)
            change = new_value - old_value

            results.append(
                f"{row['Countries/States']}: "
                f"{old_value}% → {new_value}% "
                f"(change: {change:+.1f} percentage points)"
            )
        except ValueError:
            results.append(
                f"{row['Countries/States']}: "
                f"1999-2000={old}, 2009-10={new}"
            )

    return "\n".join(results)


if __name__ == "__main__":
    print(compare("India"))