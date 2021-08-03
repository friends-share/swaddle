from fastapi import APIRouter

from src.core.scaler import get_scale
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
async def status(group: str, app_name: str):
    return get_scale(group, app_name)
