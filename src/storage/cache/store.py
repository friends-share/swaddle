from src.model.apps import App, AppLog
from src.model.cluster_log import ClusterLog
from src.model.commands import CommandGroup
from src.model.deploy import DeployConfig, DeploymentLog
from src.model.group import GroupData
from src.model.server import Server, Cluster
from src.storage.cache.definition import Cache


class ServerDetailsStore(Cache[Server]):
    def data_prefix(self) -> str:
        return "server-defn-store-"


class AppStore(Cache[App]):
    def data_prefix(self) -> str:
        return "app-store-"


class DeploymentConfigStore(Cache[DeployConfig]):
    def data_prefix(self) -> str:
        return "deployment-cfg-"


class CommandStore(Cache[CommandGroup]):
    def data_prefix(self) -> str:
        return "cmd-data-"


class ClusterLogStore(Cache[ClusterLog]):
    def data_prefix(self) -> str:
        return "cluster-log-"


class DeploymentLogStore(Cache[DeploymentLog]):
    def data_prefix(self) -> str:
        return "deploy-log-store"


class GroupedDataStore(Cache[GroupData]):
    def data_prefix(self) -> str:
        return "deploy-log-store"


class ClusterDataStore(Cache[Cluster]):
    def data_prefix(self) -> str:
        return "cluster-data-store"


class AppLogStore(Cache[AppLog]):
    def data_prefix(self) -> str:
        return "cluster-data-store"
