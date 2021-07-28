from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from src.model import Credential, InfraCharacteristic, Grouped
from src.model.commands import CommandGroup


class AServer(BaseModel):
    server_id: str
    type: str
    ip_address: str


class Server(AServer):
    credential: Optional[Credential]
    ssh_port: int


class ServersRequest(BaseModel):
    servers: List[Server]


class ClusterDataRequest(BaseModel):
    managers: List[Server]
    workers: Optional[List[Server]]
    type: str
    qualities: InfraCharacteristic
    max_deployments: int
    environment_setup: Optional[List[str]]

    def to_cluster_data(self, command_manager):
        return ClusterData(managers=self.managers, workers=self.workers, type=self.type, qualities=self.qualities,
                           max_deployments=self.max_deployments,
                           environment_setup=[command_manager.get_by_id(command_manager.get_id_components(x, self.type)) for
                                              x in self.environment_setup])


class ClusterData(BaseModel):
    managers: List[Server]
    workers: Optional[List[Server]]
    type: str
    qualities: InfraCharacteristic
    max_deployments: int
    environment_setup: Optional[List[CommandGroup]]


class Cluster(Grouped):
    cluster_id: str
    data: ClusterData
    created_on: datetime
