import csv
from io import StringIO
from typing import List

from tortoise.functions import Sum
from tortoise.transactions import in_transaction

from gobble_cube.db.models import SalesTransaction

AVAILABLE_DIMENTIONS = ["category", "product", "quantity", "revenue", "date"]

AVAILABLE_DIMENTIONS_TO_MODELS_MAP = {
    "category": "product__product_categories__category_id",
    "product": "product__id",
    "quantity": "quantity",
    "revenue": "revenue",
    "date": "date",
}

ALLOWED_FIELDS_IN_SALES_TRANSACTION_CSV = ["product_id", "quantity", "revenue", "date"]


async def bulk_upload_sales_transactions_from_csv(data) -> None:
    """
    Upload sales transactions from a CSV file.

    :param data: data from the CSV file.
    """

    # Use StringIO to treat the string as a file object
    csv_reader = csv.DictReader(StringIO(data))

    csv_reader.fieldnames = [field.strip() for field in csv_reader.fieldnames]
    if not all(
        field in csv_reader.fieldnames
        for field in ALLOWED_FIELDS_IN_SALES_TRANSACTION_CSV
    ):
        raise ValueError(
            "Invalid CSV file. Please make sure the file contains the "
            "following columns: product_id, quantity, revenue, date.",
        )

    transactions = []
    async with in_transaction():
        for row in csv_reader:
            product_id = int(row["product_id"])
            quantity = int(row["quantity"])
            revenue = float(row["revenue"])
            date = row["date"]

            transaction = SalesTransaction(
                product_id=product_id, quantity=quantity, revenue=revenue, date=date
            )
            transactions.append(transaction)

        await SalesTransaction.bulk_create(transactions)


async def get_total_revenue_for_period(start_date: str, end_date: str) -> int:
    """
    Get total revenue for a given period.

    :param start_date: start date.

    :param end_date: end date.

    :return: total revenue.
    """
    result = (
        await SalesTransaction.filter(date__range=(start_date, end_date))
        .annotate(total_revenue=Sum("revenue"))
        .values("total_revenue")
    )
    return result[0]["total_revenue"] if result else 0


async def get_sales_data_by_dimensions(dimensions: list) -> List:
    """
    Get sales data by dimensions.

    :param dimensions: list of dimensions.

    :return: sales data.
    """

    for dimension in dimensions:
        if dimension not in AVAILABLE_DIMENTIONS:
            raise ValueError(
                f"Invalid dimension: {dimension}. Available dimensions "
                f"are: {AVAILABLE_DIMENTIONS}"
            )

    mapped_dimensions = [
        AVAILABLE_DIMENTIONS_TO_MODELS_MAP[dimension] for dimension in dimensions
    ]

    query = SalesTransaction.annotate(total_revenue=Sum("revenue"))

    # Apply related fetching conditionally
    if "category" in dimensions or "product" in dimensions:
        query = query.prefetch_related("product__product_categories__category")

    # Group by dimensions and retrieve values
    result = await query.group_by(*mapped_dimensions).values(
        *mapped_dimensions, "total_revenue"
    )

    return result

    # if "category" in dimensions or "product" in dimensions:
    #     return (
    #         await SalesTransaction.all()
    #         .annotate(total_revenue=Sum("revenue"))
    #         .prefetch_related("product")
    #         .group_by(*mapped_dimensions)
    #         .values(*mapped_dimensions, "total_revenue")
    #     )
    #
    # return (
    #     await SalesTransaction.annotate(total_revenue=Sum("revenue"))
    #     .group_by(*mapped_dimensions)
    #     .values(*mapped_dimensions, "total_revenue")
    # )
