import uuid

from fastapi import APIRouter, BackgroundTasks

from src.dependency.deployers import DEPLOYER
from src.model.deploy import DeploymentLog, Stack

router = APIRouter(prefix="/api/v1/swaddle")
manager = DEPLOYER


@router.post(
    "/start", tags=["Deployer"],
    summary="Deploy docker containers"
)
async def start(request: Stack, background_tasks: BackgroundTasks):
    deployment_id = uuid.uuid4().hex[:6].upper()
    background_tasks.add_task(manager.deploy, request, deployment_id, background_tasks)
    return {"deployment_id": deployment_id, "status": "STARTED"}


@router.get(
    "/status", tags=["Deployer"],
    summary="Status of deployment",
    response_model=DeploymentLog
)
async def status(group: str, deployment_id: str):
    return manager.grouped_data_manager.get_deployment_log(group, deployment_id)


@router.post(
    "/stop", tags=["Deployer"],
    summary="Stop docker containers"
)
async def stop(name: str):
    pass
