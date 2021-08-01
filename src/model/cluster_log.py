from typing import Optional, Dict

from pydantic import BaseModel

from src.model.apps import App
from src.model.deploy import DeploymentMethod
from src.model.server import Cluster


class ClusterLog(BaseModel):
    preparation_done: Optional[Dict[DeploymentMethod, bool]]
    cluster: Cluster
    deployed_apps: Optional[Dict[str, App]]
