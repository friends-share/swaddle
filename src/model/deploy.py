from enum import Enum
from typing import Optional, List, Dict

from pydantic import BaseModel

from src.model.apps import App
from src.model.commands import CommandGroup
from src.model.message import SimpleStatus
from src.model.server import Cluster


class ClusterFabric(BaseModel):
    cluster: str
    preparation: Optional[List[str]]


class AppFabric(BaseModel):
    app: str
    fabric: Optional[List[ClusterFabric]]


class DeploymentMethod(Enum):
    DOCKER = "DOCKER"


class Stack(BaseModel):
    name: str
    based_on: DeploymentMethod
    apps: List[AppFabric]


class DeployConfig(BaseModel):
    name: str
    stacks: List[Stack]


class DeploymentStepSpec(BaseModel):
    name: str
    step_no: int


class DeploymentStep(Enum):
    DEPLOY_CONFIG_VALIDITY_0 = DeploymentStepSpec(name="DEPLOY_CONFIG_VALIDITY", step_no=0)
    APP_CONFIG_SEARCH_1 = DeploymentStepSpec(name="APP_CONFIG_SEARCH", step_no=1)
    CLUSTER_CONFIG_SEARCH_2 = DeploymentStepSpec(name="CLUSTER_CONFIG_SEARCH", step_no=2)
    INFRA_REQUIREMENT_MATCH_3 = DeploymentStepSpec(name="INFRA_REQUIREMENT_MATCH", step_no=3)
    CLUSTER_INIT_4 = DeploymentStepSpec(name="CLUSTER_INIT", step_no=5)
    DEPLOYMENT_5 = DeploymentStepSpec(name="DEPLOYMENT", step_no=6)


class DeploymentLog(BaseModel):
    deployment_id: str
    config: DeployConfig
    status: Optional[Dict[DeploymentStep, SimpleStatus]]


class EnrichedClusterFabric(ClusterFabric):
    cluster: Cluster
    preparation: Optional[List[CommandGroup]]
    post_preparation: Optional[List[CommandGroup]]


class EnrichedAppFabric(AppFabric):
    app: App
    fabric: List[EnrichedClusterFabric]


class EnrichedStack(Stack):
    apps: List[EnrichedAppFabric]


class EnrichedDeploymentConfig(DeployConfig):
    name: str
    stacks: List[EnrichedStack]
