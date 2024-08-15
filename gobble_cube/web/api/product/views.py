from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.params import File
from starlette import status

from gobble_cube.services.product import bulk_upload_products_from_csv

router = APIRouter()


@router.post("/csv")
async def get_product_upload_csv(file: UploadFile = File(...)):
    """
    Upload products from a CSV file.
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

        await bulk_upload_products_from_csv(decoded)

        return {
            "status": "success",
            "detail": f"Products were successfully uploaded.",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
