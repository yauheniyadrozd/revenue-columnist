import pandas as pd

from solution import add_virtual_column


def read_sales(path: str) -> pd.DataFrame:
    return pd.read_csv(path, keep_default_na=False)


def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [column.strip() for column in df.columns]

    df = df[~df["Order ID"].isin(["Order ID", "TOTAL"])]

    for column in df.columns:
        df[column] = df[column].astype(str).str.strip()

    df["Region"] = df["Region"].str.title()

    df["Quantity"] = pd.to_numeric(
        df["Quantity"].str.replace(" ", "", regex=False), errors="coerce"
    )
    df["Unit Price"] = pd.to_numeric(
        df["Unit Price"].str.replace(",", ".", regex=False), errors="coerce"
    )
    df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce").fillna(0)

    df = df.dropna(subset=["Quantity", "Unit Price"])
    df = df.drop_duplicates()

    return df.rename(
        columns={
            "Order ID": "order_id",
            "Region": "region",
            "Product": "product",
            "Quantity": "quantity",
            "Unit Price": "unit_price",
            "Discount": "discount",
            "Order Date": "order_date",
        }
    )


def main() -> None:
    df = clean_sales(read_sales("sales.csv"))
    df = add_virtual_column(df, "quantity * unit_price - discount", "revenue")

    revenue_by_region = (
        df.groupby("region", as_index=False)["revenue"]
        .sum()
        .rename(columns={"region": "Region", "revenue": "Revenue"})
    )
    revenue_by_region["Revenue"] = revenue_by_region["Revenue"].round(2)
    revenue_by_region.to_csv("revenue_by_region.csv", index=False)


if __name__ == "__main__":
    main()
