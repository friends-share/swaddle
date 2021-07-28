from fastapi import APIRouter

from src.model.scale import ScaleRequest

router = APIRouter(prefix="/api/v1/swaddle")


@router.post(
    "/scale", tags=["Scaler"],
    summary="Scale applications"
)
async def scale(request: ScaleRequest):
    pass


@router.get(
    "/scale", tags=["Scaler"],
    summary="Current application status"
)
async def status(name: str):
    pass
