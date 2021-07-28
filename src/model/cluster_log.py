from typing import Optional, List

from pydantic import BaseModel

from src.model.apps import App
from src.model.server import Cluster


class ClusterLog(BaseModel):
    log_id: str
    preparation_done: Optional[bool]
    cluster: Cluster
    deployed_apps: Optional[List[App]]
    init_done: Optional[bool]
    manager: Optional[bool]
    deployed: Optional[dict]
