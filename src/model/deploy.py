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
    clusters: Optional[List[ClusterFabric]]


class DeploymentMethod(Enum):
    DOCKER = "DOCKER"


class Stack(BaseModel):
    name: str
    based_on: DeploymentMethod
    apps: List[AppFabric]
    group: str


class DeploymentStepSpec(BaseModel):
    name: str
    step_no: int


class DeploymentStep(Enum):
    DEPLOY_CONFIG_VALIDITY_0 = "DEPLOY_CONFIG_VALIDITY"
    APP_CONFIG_SEARCH_1 = "APP_CONFIG_SEARCH"
    CLUSTER_CONFIG_VALIDATOR_2 = "CLUSTER_CONFIG_VALIDATOR"
    INFRA_REQUIREMENT_MATCH_3 = "INFRA_REQUIREMENT_MATCH"
    CLUSTER_INIT_4 = "CLUSTER_INIT"
    DEPLOYMENT_5 = "DEPLOYMENT"


class EnrichedClusterFabric(ClusterFabric):
    cluster: Cluster
    preparation: Optional[List[CommandGroup]]
    post_preparation: Optional[List[CommandGroup]]


class EnrichedAppFabric(AppFabric):
    app: App
    clusters: List[EnrichedClusterFabric]


class DeployingStack(Stack):
    deployment_id: str
    apps: List[EnrichedAppFabric]


class DeploymentLog(BaseModel):
    deployment_id: str
    config: Optional[DeployingStack]
    status: Optional[Dict[DeploymentStep, SimpleStatus]]
    group: str
