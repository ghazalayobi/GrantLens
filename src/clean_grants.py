
from pathlib import Path

import pandas as pd


INPUT_FILE = Path("data/processed/grants_before_dedup.csv")
OUTPUT_FILE = Path("data/processed/grants_cleaned.csv")
REPORT_FILE = Path("docs/data_quality_report.md")


def clean_text(value):
    """Trim leading/trailing whitespace and standardize missing text."""
    if pd.isna(value):
        return pd.NA

    value = str(value).strip()

    return value if value else pd.NA


def main():
    # 1. Load the extracted dataset.
    df = pd.read_csv(INPUT_FILE, dtype={"grant_id": "string"})

    original_rows = len(df)

    # 2. Clean text columns without changing the raw input file.
    text_columns = [
        "grant_id",
        "title",
        "recipient",
        "location",
        "program_area",
        "grant_period",
        "program_initiative",
        "source_url",
        "retrieved_at",
    ]

    for column in text_columns:
        df[column] = df[column].map(clean_text).astype("string")

    # 3. Convert amounts to numeric values.
    df["amount_usd"] = pd.to_numeric(
        df["amount_usd"],
        errors="coerce",
    )

    # 4. Identify duplicate IDs, preserving every row.
    df["duplicate_grant_id"] = df["grant_id"].duplicated(
        keep=False
    )

    # 5. Validate required fields.
    required_columns = [
        "grant_id",
        "title",
        "recipient",
        "source_url",
    ]

    df["missing_required_fields"] = df[
        required_columns
    ].isna().any(axis=1)

    # 6. Validate amount values.
    df["invalid_amount"] = (
        df["amount_usd"].isna()
        | (df["amount_usd"] < 0)
    )

    # 7. Check basic URL structure.
    df["invalid_source_url"] = ~df["source_url"].str.match(
        r"^https://www\.mott\.org/grants/[^/\s]+/?$",
        na=False,
    )

    # 8. Save all records, including duplicate source listings.
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    # 9. Summarize data quality.
    duplicate_rows = int(df["duplicate_grant_id"].sum())
    duplicate_ids = int(
        df.loc[df["duplicate_grant_id"], "grant_id"].nunique()
    )

    missing_by_column = df[text_columns + ["amount_usd"]].isna().sum()

    report = f"""# GrantLens Data Quality Report

## Dataset summary

- Input file: `{INPUT_FILE}`
- Output file: `{OUTPUT_FILE}`
- Rows read: {original_rows}
- Rows written: {len(df)}
- Rows removed during cleaning: {original_rows - len(df)}
- Distinct grant IDs: {df["grant_id"].nunique()}
- Rows with duplicate grant IDs: {duplicate_rows}
- Distinct IDs appearing more than once: {duplicate_ids}

## Validation results

- Rows missing required fields: {int(df["missing_required_fields"].sum())}
- Rows with missing or negative amounts: {int(df["invalid_amount"].sum())}
- Rows with invalid source URL structure: {int(df["invalid_source_url"].sum())}

## Missing values by field

{missing_by_column.to_string()}

## Duplicate handling

Duplicate grant IDs are flagged, not removed.
The source website was observed to list three grant IDs
more than once in the sample. These occurrences are
preserved for traceability and will be documented in
subsequent analysis.

## Limitations

Structural checks do not prove that every field matches
the original webpage. Source-level verification is still
required for factual accuracy.
"""

    REPORT_FILE.write_text(report, encoding="utf-8")

    print("CLEANING SUMMARY")
    print("--------------------")
    print(f"Rows read: {original_rows}")
    print(f"Rows written: {len(df)}")
    print(f"Distinct grant IDs: {df['grant_id'].nunique()}")
    print(f"Rows flagged as duplicates: {duplicate_rows}")
    print(f"Duplicate IDs: {duplicate_ids}")
    print(
        "Rows missing required fields:",
        int(df["missing_required_fields"].sum()),
    )
    print(
        "Rows with invalid amounts:",
        int(df["invalid_amount"].sum()),
    )
    print(
        "Rows with invalid URL structure:",
        int(df["invalid_source_url"].sum()),
    )
    print(f"\nCleaned data saved to: {OUTPUT_FILE}")
    print(f"Quality report saved to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
