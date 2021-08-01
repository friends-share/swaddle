import uuid

from fastapi import APIRouter

from src.dependency.deployers import DEPLOYER
from src.model.deploy import DeploymentLog, Stack

router = APIRouter(prefix="/api/v1/swaddle")
manager = DEPLOYER


@router.post(
    "/start", tags=["Deployer"],
    summary="Deploy docker containers"
)
async def start(request: Stack):
    return manager.deploy(request, uuid.uuid4().hex[:6].upper())


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
