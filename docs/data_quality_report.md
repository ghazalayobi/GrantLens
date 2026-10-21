# GrantLens Data Quality Report

## Dataset summary

- Input file: `data/processed/grants_before_dedup.csv`
- Output file: `data/processed/grants_cleaned.csv`
- Rows read: 30
- Rows written: 30
- Rows removed during cleaning: 0
- Distinct grant IDs: 27
- Rows with duplicate grant IDs: 6
- Distinct IDs appearing more than once: 3

## Validation results

- Rows missing required fields: 0
- Rows with missing or negative amounts: 0
- Rows with invalid source URL structure: 0

## Missing values by field

grant_id              0
title                 0
recipient             0
location              0
program_area          0
grant_period          0
program_initiative    0
source_url            0
retrieved_at          0
amount_usd            0

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
