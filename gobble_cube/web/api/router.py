from fastapi.routing import APIRouter

from gobble_cube.web.api import (
    docs,
    monitoring,
    sales_transaction,
    category_share,
    product,
)

api_router = APIRouter()
api_router.include_router(monitoring.router)

# business logic
api_router.include_router(sales_transaction.router, prefix="/sales-transaction")
api_router.include_router(category_share.router, prefix="/category-share")
api_router.include_router(product.router, prefix="/product")


# docs
api_router.include_router(docs.router)
