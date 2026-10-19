# GrantLens Data Dictionary

## Dataset: Public Grant Records

| Field | Type | Description |
|---|---|---|
| grant_id | string | Unique grant identifier |
| recipient | string | Grant recipient organization |
| title | string | Public grant title |
| description | string | Publicly stated grant purpose |
| amount_usd | float | Grant amount in USD |
| program_area | string | Foundation program category |
| start_date | date | Grant start date |
| end_date | date | Grant end date |
| source_url | string | Original grant detail URL |
| retrieved_at | date | Date record was retrieved |

## Data Quality Rules

1. Grant records must have a source URL.
2. Missing amounts must not be replaced with zero.
3. Dates should use YYYY-MM-DD format.
4. Duplicate grant records should be identified.
5. Original raw data must remain unchanged.
6. Generated or inferred information must not be presented as source data.