# Virtual columns in a pandas DataFrame

A small data pipeline that adds a calculated column to a pandas DataFrame and
uses it to clean a sales export and report total revenue per region.

## Setup

Python 3.11+ is recommended.

```bash
pip install -r requirements.txt
```

## Run the pipeline

```bash
python pipeline.py
```

This reads `sales.csv`, cleans it, computes a `revenue` column via
`add_virtual_column`, and writes `revenue_by_region.csv` (total revenue per
region).

## Run the tests

```bash
pytest
```

One command runs all test files: `test_virtual_column.py` (the provided sample
tests), `test_solution.py` (extra Part 1 tests) and `test_pipeline.py` (Part 2
tests).

## Assumptions and decisions

- **Negative quantities are kept as-is.** They are interpreted as returns or
  refunds, so they produce negative revenue instead of being dropped or forced
  positive.
- **`1 762`-style quantities** are interpreted as a space used as a thousands
  separator (`1762`), because all other quantities in the file are small counts.
- **Comma in `Unit Price`** (e.g. `59,00`) is a European decimal separator and
  is converted to a dot (`59.00`).
- **Empty `Discount` means "no discount"** and is treated as `0`.
- **Rows with an empty `Unit Price`** cannot be reconstructed, so they are
  dropped.
- **Exact duplicate rows** are removed, keeping the first occurrence.
- **Column names are renamed to snake_case** (`unit_price`, `order_id`, …)
  because `add_virtual_column` only accepts labels made of letters and
  underscores. The output file keeps readable `Region`/`Revenue` headers.
- **`revenue_by_region.csv`** sums revenue per region and rounds to two decimal
  places (currency).

## Problems found in `sales.csv`

The raw file has 1507 lines. After cleaning, 1496 order lines remain.

| Problem | Rows affected | Handling |
| --- | --- | --- |
| Repeated header row in the middle of the file | 1 | Removed |
| `TOTAL` summary row at the end | 1 | Removed |
| `Region` has inconsistent case / whitespace (`north`, `EAST`, ` South`, …) | 15 | Stripped and normalized to title case |
| `Unit Price` uses a comma decimal separator (`59,00`) | 7 | Comma replaced with a dot |
| `Quantity` uses a space as thousands separator (`1 762`) | 4 | Space removed (value = 1762) |
| `Quantity` is negative | 6 | Kept unchanged (returns/refunds) |
| `Unit Price` is empty | 4 | Dropped (cannot be recovered) |
| `Discount` is empty (no discount) | 962 | Treated as 0 |
| Exact duplicate rows | 5 | Removed, keeping the first occurrence |
