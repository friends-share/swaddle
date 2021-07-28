from src.core.apps import AppService, AppLogManager
from src.core.cluster import ClusterManager, ClusterLogManager
from src.core.command import CommandService
from src.core.deployment_log import DeploymentLogManager

from src.core.group_data import GroupDataManager
from src.core.server import ServerManager
from src.dependency import server_details_store, deployment_log_store
from src.deploying.deploy import DeploymentConfigValidator


class Manager:
    GROUPED_DATA_MANAGER = GroupDataManager()
    APP_MANAGER = AppService(GROUPED_DATA_MANAGER)
    CLUSTER_MANAGER = ClusterManager(GROUPED_DATA_MANAGER)
    COMMAND_SERVICE = CommandService()
    CLUSTER_LOG_MANAGER = ClusterLogManager()
    SERVER_MANAGER = ServerManager(server_details_store)
    DEPLOYMENT_MANAGER = DeploymentConfigValidator(APP_MANAGER, COMMAND_SERVICE, SERVER_MANAGER, GROUPED_DATA_MANAGER)
    APP_LOG_MANAGER = AppLogManager()
    DEPLOYMENT_LOG_MANAGER = DeploymentLogManager(deployment_log_store)