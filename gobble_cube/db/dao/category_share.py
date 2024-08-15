from typing import List

from tortoise import Tortoise


async def fetch_category_share_data_for_period(
    start_date: str, end_date: str, limit: int = 10
) -> List:
    """
    Custom query to fetch category share data for a given period.

    :param start_date: start date.
    :param end_date: end date.
    :param limit: limit the number of results.

    :return: category share data.
    """

    query = f"""
        SELECT
            c.category_id AS category_id,
            MAX(cs.market_share) - MIN(cs.market_share) AS market_share_change
        FROM
            product_categories c
        JOIN
            category_shares cs ON cs.product_id = c.product_id
        WHERE
            cs.date BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY
            c.category_id
        ORDER BY
            market_share_change DESC
    """

    if limit:
        query += f" LIMIT {limit};"

    """

    query if you want to fetch the category names as well

    query =
        SELECT
            c.id AS category_id,
            c.name AS category_name,
            MAX(cs.market_share) - MIN(cs.market_share) AS market_share_change
        FROM
            categories c
        JOIN
            product_categories p ON p.category_id = c.id
        JOIN
            category_shares cs ON cs.product_id = p.product_id
        WHERE
            cs.date BETWEEN '2024-01-01' AND '2024-12-31'
        GROUP BY
            c.id, c.name
        ORDER BY
            market_share_change DESC
        LIMIT 5;
    """

    category_shares = await Tortoise.get_connection("default").execute_query_dict(query)

    return category_shares
