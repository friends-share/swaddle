from typing import Optional, Dict

from pydantic import BaseModel

from src.model.apps import AppLog
from src.model.cluster_log import ClusterLog
from src.model.deploy import DeploymentLog


class GroupData(BaseModel):
    name: str
    apps: Optional[Dict[str, AppLog]]
    clusters: Optional[Dict[str, ClusterLog]]
    deployment_details: Optional[Dict[str, DeploymentLog]]
