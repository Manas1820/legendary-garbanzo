import logging

from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.params import File
from starlette import status
from starlette.status import HTTP_400_BAD_REQUEST

from gobble_cube.services.service_transaction import (
    get_total_revenue_for_period,
    get_sales_data_by_dimensions,
    bulk_upload_sales_transactions_from_csv,
)

router = APIRouter()


@router.post("/csv")
async def sales_transaction_upload_csv(file: UploadFile = File(...)):
    """
    Upload sales transactions from a CSV file.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Please upload a CSV file.",
        )

    try:
        # Read and decode the file contents
        contents = await file.read()
        decoded = contents.decode("utf-8")

        await bulk_upload_sales_transactions_from_csv(decoded)

        return {
            "status": "success",
            "detail": f"Transactions were successfully uploaded.",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/total")
async def get_total_sales(start_date: str, end_date: str):
    """
    Get total sales for a given period.

    param start_date: start date.
    param end_date: end date.
    """

    if not start_date or not end_date:
        raise ValueError("Start date and End date are required")

    total_sales = await get_total_revenue_for_period(start_date, end_date)
    return {"status": "success", "total_sales": total_sales}


@router.get("/dimentions")
async def get_sales_dimensions(dimensions: str):
    """
    Get sales distribution.

    Takes in a list of dimensions and returns sales of each dimensions.

    AVAILABLE_DIMENTIONS = ["category", "product", "quantity", "revenue", "date"]
    """

    dimensions = dimensions.split(",")
    cleaned_dimensions = list(set([dimension.strip() for dimension in dimensions]))

    if len(dimensions) != len(cleaned_dimensions):
        logging.warning("Duplicate dimensions found in the query")

    sales_by_dimensions = await get_sales_data_by_dimensions(dimensions)
    return {"status": "success", "sales_by_dimensions": sales_by_dimensions}
