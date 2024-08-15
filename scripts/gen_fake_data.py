"""
This script generates fake data for the Gobble Cube application. It creates 5
categories, 20 products, 100 sales transactions, and 50 category shares. The data is
generated using the Faker library and stored in an SQLite database. The script uses
the Tortoise ORM to interact with the database.
"""

import logging
from faker import Faker
from tortoise import Tortoise, run_async
from gobble_cube.db.models import (
    SalesTransaction,
    Product,
    Category,
    CategoryShare,
    ProductCategory,
)

fake = Faker()

logging.basicConfig(level=logging.INFO)


async def generate_data():
    # Initialize Tortoise ORM
    await Tortoise.init(
        db_url="sqlite://db.sqlite3", modules={"models": ["gobble_cube.db.models"]}
    )
    await Tortoise.generate_schemas()

    # Create Categories
    categories = []
    for _ in range(10000):  # Let's create 5 categories
        category = await Category.create(name=fake.word())
        categories.append(category)

    logging.info(f"{len(categories)} Categories created")

    # Create Products and associate them with Categories
    products = []
    for i in range(10000):  # Let's create 20 products
        category = fake.random_element(categories)
        product = await Product.create(category=category, name=fake.word())
        for _ in range(fake.random_int(min=1, max=3)):
            await ProductCategory.create(
                product_id=product.id, category_id=fake.random_int(min=1, max=10000 - 1)
            )
        products.append(product)

    logging.info(f"{len(products)} Products created")

    # Now, create Sales Transactions and ensure they reference valid Products
    for _ in range(10000):  # Create 100 sales transactions
        product = fake.random_element(products)
        await SalesTransaction.create(
            date=fake.date_this_year(),
            product=product,
            quantity=fake.random_int(min=1, max=10),
            revenue=fake.pydecimal(left_digits=3, right_digits=2, positive=True),
        )

    logging.info("Sales Transactions created")

    # Create Category Shares and ensure they reference valid Products
    for _ in range(5000):  # Create 50 category shares
        product = fake.random_element(products)
        await CategoryShare.create(
            date=fake.date_this_year(),
            product=product,
            market_share=fake.pydecimal(left_digits=2, right_digits=2, positive=True),
        )

    logging.info("Category Shares created")

    # Close the database connections
    await Tortoise.close_connections()


# Run the async function to populate the database
if __name__ == "__main__":
    run_async(generate_data())
