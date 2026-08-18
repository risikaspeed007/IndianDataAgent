import csv
from pathlib import Path
import xlrd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT_ROOT / "Countries_Gross_Enrollment_Data (1).xls"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT = OUTPUT_DIR / "gross_enrollment_data.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

workbook = xlrd.open_workbook(SOURCE)
sheet = workbook.sheet_by_index(0)

rows = [sheet.row_values(i) for i in range(sheet.nrows)]

with OUTPUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"Created: {OUTPUT}")
print(f"Rows written: {len(rows) - 1}")