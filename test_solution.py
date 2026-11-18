import pandas as pd

from solution import add_virtual_column


def test_adds_column_without_mutating_input():
    df = pd.DataFrame([[1, 2]], columns=["a", "b"])
    result = add_virtual_column(df, "a + b", "c")
    assert list(df.columns) == ["a", "b"]
    assert list(result.columns) == ["a", "b", "c"]


def test_empty_when_df_column_invalid():
    df = pd.DataFrame([[1, 2]], columns=["a", "b value"])
    assert add_virtual_column(df, "a", "c").empty


def test_empty_when_division_not_supported():
    df = pd.DataFrame([[1, 2]], columns=["a", "b"])
    assert add_virtual_column(df, "a / b", "c").empty


def test_empty_when_missing_operand():
    df = pd.DataFrame([[1, 2]], columns=["a", "b"])
    assert add_virtual_column(df, "a +", "c").empty


def test_empty_when_empty_role():
    df = pd.DataFrame([[1, 2]], columns=["a", "b"])
    assert add_virtual_column(df, "   ", "c").empty


def test_uppercase_labels_are_valid():
    df = pd.DataFrame([[1, 1]], columns=["Left", "Right"])
    result = add_virtual_column(df, "Left + Right", "Sum")
    assert result["Sum"].tolist() == [2]


def test_empty_when_role_column_not_in_df():
    df = pd.DataFrame([[1, 2]], columns=["a", "b"])
    assert add_virtual_column(df, "a + missing", "c").empty


def test_keyword_column_names_are_supported():
    df = pd.DataFrame([[1, 2]], columns=["and", "b"])
    result = add_virtual_column(df, "and + b", "c")
    assert result["c"].tolist() == [3]
