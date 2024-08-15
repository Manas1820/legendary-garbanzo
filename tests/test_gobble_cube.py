import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


@pytest.mark.anyio
async def test_health(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Checks the health endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("health_check")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_category_share_upload_csv(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Checks the category share upload CSV endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("category_share_upload_csv")
    response = await client.post(url, files={"file": ("category_share.csv", "data")})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

