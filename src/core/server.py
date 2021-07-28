from typing import List, Tuple

from src.core.deploying import Deploying
from src.core.service import AService, Id
from src.model.deploy import DeploymentStep, EnrichedDeploymentConfig
from src.model.message import ProcessStatus, Status, SimpleStatus
from src.model.server import Server
from src.storage.cache.store import ServerDetailsStore


class ServerManager(AService[Server, str]):

    def __init__(self, store: ServerDetailsStore):
        super().__init__(store)

    def get_id(self, obj: Server) -> Id:
        return obj.server_id

    def save_all(self, servers: List[Server]) -> ProcessStatus:
        return ProcessStatus(status=Status.SUCCESS) if sum([self.save_obj(obj=server) for server in servers]) == len(
            servers) else ProcessStatus(status=Status.FAILURE)


class ServerDeployer(Deploying[EnrichedDeploymentConfig, EnrichedDeploymentConfig]):

    def define_process(self, component: EnrichedDeploymentConfig) -> Tuple[SimpleStatus, EnrichedDeploymentConfig]:
        pass

    def deployment_step(self) -> DeploymentStep:
        return DeploymentStep.APP_CONFIG_SEARCH_1

    def entry_criteria(self, component: EnrichedDeploymentConfig) -> Tuple[bool, str]:
        pass
