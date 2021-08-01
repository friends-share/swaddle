from fastapi import APIRouter

from src.dependency.manager import Manager
from src.model.apps import AppsRequest
from src.model.message import *

router = APIRouter(prefix="/api/v1/swaddle")
app_manager = Manager.APP_MANAGER


@router.post(
    "/apps", tags=["Apps"],
    summary="Add apps information"
)
async def add_apps(request: AppsRequest, response: Response):
    errors = app_manager.add_new(request)
    return response_body("add_apps", response=response,
                         prcs_status=ProcessStatus(status=Status.SUCCESS if not errors else Status.FAILURE, errors=errors))


@router.get(
    "/apps", tags=["Apps"],
    summary="Get App information"
)
async def get_apps(app_name: str, response: Response):
    apps_data = app_manager.get_by_id(app_name)
    return response_body("get_apps", response=response, prcs_status=ProcessStatus(status=Status.SUCCESS, data=apps_data))


@router.put(
    "/apps", tags=["Apps"],
    summary="Upsert App information"
)
async def upsert_apps(request: AppsRequest, response: Response):
    data = app_manager.upsert(request)
    return response_body("upsert_apps", response=response, prcs_status=ProcessStatus(status=Status.SUCCESS, data=data))
