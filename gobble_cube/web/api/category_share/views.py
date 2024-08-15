from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.params import File
from starlette import status

from gobble_cube.services.category_share import (
    bulk_upload_category_share_from_csv,
    get_significant_category_shares_for_period,
)

router = APIRouter()


@router.post("/csv")
async def category_share_upload_csv(file: UploadFile = File(...)):
    """
    Upload sales transactions from a CSV file.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Please upload a CSV file.",
        )

    try:
        # Read and decode the file contents
        contents = await file.read()
        decoded = contents.decode("utf-8")

        await bulk_upload_category_share_from_csv(decoded)

        return {
            "status": "success",
            "detail": f"Category Shares were successfully uploaded.",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/significant")
async def get_significant_category_shares(
    start_date: str, end_date: str, limit: int = 10
):
    """
    Get significant category shares.
    """

    if not start_date or not end_date:
        raise ValueError("Start date and End date are required")

    significant_category_shares = await get_significant_category_shares_for_period(
        start_date, end_date, limit
    )
    return {
        "status": "success",
        "significant_category_shares": significant_category_shares,
    }
