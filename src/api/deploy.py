import uuid

from fastapi import APIRouter

from src.dependency.driver import Deployers
from src.dependency.manager import Manager
from src.model.deploy import DeployConfig, DeploymentLog

router = APIRouter(prefix="/api/v1/swaddle")
deployer = Deployers.SWARM_DEPLOYER
manager = Manager.DEPLOYMENT_LOG_MANAGER


@router.post(
    "/start", tags=["Deployer"],
    summary="Deploy docker containers"
)
async def start(request: DeployConfig):
    return deployer.deploy(request, uuid.uuid4().hex[:6].upper())


@router.get(
    "/status", tags=["Deployer"],
    summary="Status of deployment",
    response_model=DeploymentLog
)
async def status(deployment_id: str):
    return manager.get_by_id(deployment_id)


@router.post(
    "/stop", tags=["Deployer"],
    summary="Stop docker containers"
)
async def stop(name: str):
    pass
