import click
import matplotlib.pyplot as plt
import pandas as pd


def _read_csv(file: str) -> pd.DataFrame:
    return pd.read_csv(file)


def _time_series_figure(df: pd.DataFrame, filename: str, title: str) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    df.plot(ax=ax, linewidth=2)

    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Values")

    plt.legend(loc="upper right")
    plt.margins(x=0, y=0.1)
    plt.tight_layout()

    plt.savefig(filename)


def _bar_plot_figure(
    df: pd.DataFrame, x_column: str, y_column: str, filename: str, title: str
) -> None:
    fig, _ = plt.subplots(figsize=(12, 6))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    plt.bar(df[x_column], df[y_column])

    plt.title(title)
    plt.xlabel(x_column)
    plt.ylabel(y_column)

    plt.legend(loc="upper right")
    plt.margins(x=0, y=0.1)
    plt.tight_layout()

    plt.savefig(filename)


def _data_aggregrates(df: pd.DataFrame) -> None:
    num_unique_products = df["product"].nunique()
    num_unique_providers = df["provider"].nunique()

    print(
        f"Number of unique products: {num_unique_products}, Number of unique providers: {num_unique_providers}"
    )

    print("Total revenue and order count by product")
    product_stats = (
        df.groupby("product")
        .agg({"revenue": "sum", "order_count": "sum"})
        .reset_index()
    )
    _bar_plot_figure(
        product_stats,
        "product",
        "revenue",
        "data/total_revenue_product.png",
        "Total revenue for product",
    )
    _bar_plot_figure(
        product_stats,
        "product",
        "order_count",
        "data/total_order_count_product.png",
        "Total order count for product",
    )

    print("Total revenue and order count by provider")
    provider_stats = (
        df.groupby("provider")
        .agg({"revenue": "sum", "order_count": "sum"})
        .reset_index()
    )
    _bar_plot_figure(
        provider_stats,
        "provider",
        "revenue",
        "data/total_revenue_provider.png",
        "Total revenue for provider",
    )
    _bar_plot_figure(
        provider_stats,
        "provider",
        "order_count",
        "data/total_order_count_provider.png",
        "Total order count for provider",
    )


def _data_average(df: pd.DataFrame) -> None:
    # Remove rows where order_count is zero and revenue is not zero
    df = df[~((df["order_count"] == 0) & (df["revenue"] != 0))]

    # Calculate average order value by product
    df["avg_order_value"] = df["revenue"] / df["order_count"]
    avg_order_value_by_product = (
        df.groupby("product")["avg_order_value"].mean().reset_index()
    )
    _bar_plot_figure(
        avg_order_value_by_product,
        "product",
        "avg_order_value",
        "data/average_revenue_product.png",
        "Average revenue for product",
    )

    # Calculate average order value by provider
    df["avg_order_value"] = df["revenue"] / df["order_count"]
    avg_order_value_by_provider = (
        df.groupby("provider")["avg_order_value"].mean().reset_index()
    )
    _bar_plot_figure(
        avg_order_value_by_provider,
        "provider",
        "avg_order_value",
        "data/average_revenue_provider.png",
        "Average revenue for provider",
    )


def _sales_trend(df: pd.DataFrame) -> None:
    df["week"] = df["order_date"].dt.to_period("W")

    # Calculate the weekly revenue for each product
    sales_trend_by_week_product = (
        df.groupby(["week", "product"])["revenue"].sum().reset_index()
    )
    pivot_df_product = sales_trend_by_week_product.pivot_table(
        index="week", columns="product", values="revenue"
    )

    _time_series_figure(
        pivot_df_product,
        "data/weekly_trend_products.png",
        "Product weekly trend: Revenue",
    )

    # Calculate the weekly revenue for each provider
    sales_trend_by_week_provider = (
        df.groupby(["week", "provider"])["revenue"].sum().reset_index()
    )
    pivot_df_provider = sales_trend_by_week_provider.pivot_table(
        index="week", columns="provider", values="revenue"
    )

    _time_series_figure(
        pivot_df_provider,
        "data/weekly_trend_provider.png",
        "Provider weekly trend: Revenue",
    )


def _calculate_commission(row: pd.Series) -> int:
    provider = int(row["provider"])
    order_count = int(row["order_count"])

    if provider == "tom_jerry":
        return 8000
    elif provider == "roadrunner":
        return 50 * order_count
    elif provider == "micky_mouse":
        if order_count <= 500:
            return 10000
        else:
            return 10000 + 10 * (order_count - 500)
    elif provider == "donald_duck":
        if order_count <= 200:
            return 50 * order_count
        elif order_count <= 400:
            return 50 * 200 + 40 * (order_count - 200)
        else:
            return 50 * 200 + 40 * 200 + 30 * (order_count - 400)
    else:
        raise ValueError("Providers not supported")


def _monthly_commision(df: pd.DataFrame) -> None:
    df["month"] = df["order_date"].dt.to_period("M")

    monthly_revenue_product = (
        df.groupby(["month", "provider", "product"])["revenue"].sum().reset_index()
    )
    monthly_orders_product = (
        df.groupby(["month", "provider", "product"])["order_count"].sum().reset_index()
    )

    merged_monthly_orders = pd.merge(
        monthly_orders_product,
        monthly_revenue_product,
        how="inner",
        on=["month", "provider", "product"],
    )
    merged_monthly_orders["commission"] = merged_monthly_orders.apply(
        _calculate_commission, axis=1
    )

    merged_monthly_orders["gross_margin"] = (
        merged_monthly_orders["revenue"] - merged_monthly_orders["commission"]
    )
    mg = merged_monthly_orders.groupby(["month", "product"]).sum().reset_index()

    print(mg[["month", "product", "revenue", "commission", "gross_margin"]])


@click.command()
@click.option(
    "--file-name",
    type=str,
    help="Name of csv file in data folder.",
    required=True,
)
def eda_data(file_name: str) -> None:
    data = _read_csv(file_name)

    data["revenue"] = data["revenue"].str.replace(",", "").astype(float)

    data["order_date"] = pd.to_datetime(data["order_date"])

    print("Data Aggregrates")
    _data_aggregrates(data)

    print("Data Average")
    _data_average(data)

    print("Sales trends")
    _sales_trend(data)

    print("Commission")
    _monthly_commision(data)


if __name__ == "__main__":
    eda_data()
