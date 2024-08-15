"""
Generate fake data for testing purposes.
This script generates fake data for the Gobble Cube application.
"""

import logging
from faker import Faker

fake = Faker()

logging.basicConfig(level=logging.DEBUG)


def generate_sales_csv(filename: str = "sales_data.csv", no_of_entries: int = 10000):
    """
    Generate a CSV file with fake sales data.
    """

    with open(f"{filename}", "w") as f:
        f.write("transaction_id,date,product_id,quantity,revenue\n")
        for i in range(no_of_entries):
            f.write(
                f"{i},"
                f"{fake.date_this_year()},"
                f"{fake.random_int(min=1, max=no_of_entries-1)},"
                f"{fake.random_int(min=1, max=no_of_entries-1)},"
                f"{fake.pydecimal(left_digits=3, right_digits=2, positive=True)}\n"
            )

    logging.info("Sales data generated.You can find the file at: " + filename)


def generate_category_share_data_csv(
    filename: str = "category_share_data.csv", no_of_entries: int = 10000
):
    """
    Generate a CSV file with fake category share data.
    """

    with open(f"{filename}", "w") as f:
        f.write("date,product_id,market_share\n")
        for i in range(no_of_entries):
            f.write(
                f"{fake.date_this_year()},"
                f"{fake.random_int(min=1, max=no_of_entries-1)},"
                f"{fake.pydecimal(left_digits=2, right_digits=2, positive=True)}\n"
            )

    logging.info("Category share data generated. you can find the file at: " + filename)


def generate_product_category_csv(
    filename: str = "product_category.csv", no_of_entries: int = 10000
):
    """
    Generate a CSV file with fake product category data.
    """

    with open(f"{filename}", "w") as f:
        f.write("product_id,category_id\n")
        for i in range(no_of_entries):
            f.write(f"{i}," f"{fake.random_int(min=1, max=no_of_entries-1)}\n")

    logging.info(
        "Product category data generated.You can find the file at: " + filename
    )


if __name__ == "__main__":
    generate_sales_csv()
    generate_category_share_data_csv()
    generate_product_category_csv()
