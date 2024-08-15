import csv
from io import StringIO
from faker import Faker
from tortoise.transactions import in_transaction

from gobble_cube.db.models import Product, Category, ProductCategory

ALLOWED_FIELDS_IN_PRODUCT_CSV = [
    "product_id",
    "category_id",
]


async def bulk_upload_products_from_csv(data):
    """
    Bulk upload products from a CSV file.
    If the category_id does not exist, a placeholder category is created.
    """

    # Use StringIO to treat the string as a file object
    csv_reader = csv.DictReader(StringIO(data))

    # Ensure field names are stripped of any whitespace
    csv_reader.fieldnames = [field.strip() for field in csv_reader.fieldnames]

    # Check if all required fields are present in the CSV
    if not all(
        field in csv_reader.fieldnames for field in ALLOWED_FIELDS_IN_PRODUCT_CSV
    ):
        raise ValueError(
            "Invalid CSV file. Please make sure the file contains the "
            "following columns: name, category_id."
        )

    product_ids = set()
    category_ids = set()

    product_category_relations = []

    async with in_transaction():
        for row in csv_reader:
            product_id = int(row["product_id"])
            category_id = int(row["category_id"])

            product_ids.add(product_id)
            category_ids.add(category_id)

            product_category_relations.append(
                ProductCategory(product_id=product_id, category_id=category_id)
            )

        await upsert_product(list(product_ids))
        await upsert_category(list(category_ids))

        await ProductCategory.bulk_create(
            product_category_relations, ignore_conflicts=True
        )


faker = Faker()


async def upsert_product(product_ids: list[int]):
    """
    Upsert products.
    If the products do not exist, they are created.

    :param product_ids: list of product IDs.

    """

    # Get existing products and categories
    existing_products = await Product.filter(id__in=product_ids).all()

    existing_product_ids = {prod.id for prod in existing_products}

    # Create new products and categories if they don't exist
    new_products = [
        Product(id=pid, name=faker.name())
        for pid in product_ids
        if pid not in existing_product_ids
    ]

    if new_products:
        await Product.bulk_create(new_products)


async def upsert_category(category_ids: list[int]):
    """
    Upsert categories.
    If the categories do not exist, they are created.

    :param category_ids: list of category IDs.

    """

    existing_categories = await Category.filter(id__in=category_ids).all()
    existing_category_ids = {cat.id for cat in existing_categories}

    new_categories = [
        Category(id=cid, name=faker.name())
        for cid in category_ids
        if cid not in existing_category_ids
    ]

    if new_categories:
        await Category.bulk_create(new_categories)
