from fastapi import APIRouter

from src.core.scaler import get_scale, scale_app
from src.model.scale import ScaleRequest

router = APIRouter(prefix="/api/v1/swaddle")


@router.post(
    "/scale", tags=["Scaler"],
    summary="Scale applications"
)
async def scale(request: ScaleRequest):
    return scale_app(request.group, request.app_name, request.count)


@router.get(
    "/scale", tags=["Scaler"],
    summary="Current application status"
)
async def status(group: str, app_name: str):
    return get_scale(group, app_name)
