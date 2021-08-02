from fastapi import APIRouter, UploadFile, File

from src.core import vault

router = APIRouter(prefix="/api/v1/swaddle")


@router.post(
    "/vault", tags=["Vault"],
    summary="Scale applications"
)
async def post(file: UploadFile = File(...)):
    return vault.put(file)
