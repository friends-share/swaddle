import os

from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/api/v1/swaddle")


@router.post(
    "/vault", tags=["Vault"],
    summary="Scale applications"
)
async def post(file: UploadFile = File(...)):
    filename = file.filename
    with open(filename, "wb+") as file_object:
        file_object.write(file.file.read())
    return filename
