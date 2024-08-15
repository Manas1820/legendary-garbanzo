import csv
from io import StringIO

from tortoise.expressions import Subquery, F, Q
from tortoise.functions import Sum
from tortoise.transactions import in_transaction

from gobble_cube.db.dao.category_share import fetch_category_share_data_for_period
from gobble_cube.db.models import CategoryShare, Category

ALLOWED_FIELDS_IN_CATEGORY_SHARE_CSV = ["market_share", "product_id", "date"]


async def bulk_upload_category_share_from_csv(data) -> None:
    """
    Upload category share from a CSV file.

    :param data: data from the CSV file.
    """

    # Use StringIO to treat the string as a file object
    csv_reader = csv.DictReader(StringIO(data))

    csv_reader.fieldnames = [field.strip() for field in csv_reader.fieldnames]

    if not all(
        field in csv_reader.fieldnames for field in ALLOWED_FIELDS_IN_CATEGORY_SHARE_CSV
    ):
        raise ValueError(
            "Invalid CSV file. Please make sure the file contains the "
            "following columns: market_share, product_id, date.",
        )

    category_shares = []
    async with in_transaction():
        for row in csv_reader:
            product_id = int(row["product_id"])
            market_share = float(row["market_share"])
            date = row["date"]

            category_share = CategoryShare(
                product_id=product_id, market_share=market_share, date=date
            )
            category_shares.append(category_share)

        await CategoryShare.bulk_create(category_shares)

    return


async def get_significant_category_shares_for_period(
    start_date: str, end_date: str, limit: int = 10
):
    """
    Get significant category shares for a given period.

    :param start_date: start date.
    :param end_date: end date.

    :return: significant category shares.
    """

    market_share_changes = await fetch_category_share_data_for_period(
        start_date, end_date, limit
    )

    return market_share_changes
