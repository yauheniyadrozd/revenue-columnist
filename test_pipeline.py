import shutil
from pathlib import Path

import pandas as pd
import pytest

from pipeline import clean_sales, read_sales
from solution import add_virtual_column

DATA = Path(__file__).parent / "sales.csv"


def test_read_sales_keeps_raw_column_names():
    df = read_sales(str(DATA))
    assert "Quantity " in df.columns


def test_clean_removes_structural_rows():
    df = clean_sales(read_sales(str(DATA)))
    assert "TOTAL" not in set(df["order_id"])
    assert "Order ID" not in set(df["order_id"])


def test_clean_normalizes_region():
    df = clean_sales(read_sales(str(DATA)))
    assert set(df["region"]) == {"North", "South", "East", "West", "Central"}


def test_clean_fixes_comma_unit_price():
    df = clean_sales(read_sales(str(DATA)))
    assert df[df["order_id"] == "SO-10137"]["unit_price"].iloc[0] == 59.0


def test_clean_fixes_quantity_thousands_separator():
    df = clean_sales(read_sales(str(DATA)))
    assert df[df["order_id"] == "SO-10251"]["quantity"].iloc[0] == 1762


def test_clean_keeps_negative_quantity():
    df = clean_sales(read_sales(str(DATA)))
    assert df[df["order_id"] == "SO-10421"]["quantity"].iloc[0] == -2


def test_clean_fills_empty_discount_with_zero():
    df = clean_sales(read_sales(str(DATA)))
    assert df[df["order_id"] == "SO-10002"]["discount"].iloc[0] == 0.0


def test_clean_drops_missing_unit_price():
    df = clean_sales(read_sales(str(DATA)))
    assert not df["unit_price"].isna().any()
    for order_id in ("SO-10610", "SO-11099", "SO-11350", "SO-11477"):
        assert order_id not in set(df["order_id"])


def test_clean_deduplicates_rows():
    df = clean_sales(read_sales(str(DATA)))
    assert not df["order_id"].duplicated().any()


def test_revenue_calculation():
    df = clean_sales(read_sales(str(DATA)))
    df = add_virtual_column(df, "quantity * unit_price - discount", "revenue")
    assert df[df["order_id"] == "SO-10001"]["revenue"].iloc[0] == pytest.approx(
        32 * 249.0 - 398.40
    )


def test_pipeline_writes_expected_file(tmp_path, monkeypatch):
    shutil.copy(str(DATA), str(tmp_path / "sales.csv"))
    monkeypatch.chdir(tmp_path)

    from pipeline import main

    main()

    out = pd.read_csv(tmp_path / "revenue_by_region.csv")
    assert list(out.columns) == ["Region", "Revenue"]
    assert len(out) == 5
