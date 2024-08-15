from tortoise import fields, models


class Category(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    class Meta:
        table = "categories"


class Product(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    class Meta:
        table = "products"


class ProductCategory(models.Model):
    product = fields.ForeignKeyField(
        "models.Product", related_name="product_categories"
    )
    category = fields.ForeignKeyField(
        "models.Category", related_name="product_categories"
    )

    class Meta:
        table = "product_categories"


class SalesTransaction(models.Model):
    id = fields.IntField(pk=True)
    date = fields.DateField()
    product = fields.ForeignKeyField(
        "models.Product", related_name="sales_transactions"
    )
    quantity = fields.IntField()
    revenue = fields.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table = "sales_transactions"


class CategoryShare(models.Model):
    id = fields.IntField(pk=True)
    date = fields.DateField()
    product = fields.ForeignKeyField("models.Product", related_name="category_shares")
    market_share = fields.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        table = "category_shares"
