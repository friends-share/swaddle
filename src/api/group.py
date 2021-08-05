from fastapi import APIRouter

from src.dependency.manager import Manager
from src.model.group import GroupData

router = APIRouter(prefix="/api/v1/swaddle")
manager = Manager.GROUPED_DATA_MANAGER


@router.get(
    "/status", tags=["Group"],
    summary="Status of Group",
    response_model=GroupData
)
async def status(group: str):
    return manager.get_by_id(group)
