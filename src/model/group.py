from typing import Optional, Dict

from pydantic import BaseModel

from src.model.apps import App
from src.model.server import Cluster


class GroupData(BaseModel):
    name: str
    apps: Optional[Dict[str, App]]
    clusters: Optional[Dict[str, Cluster]]
