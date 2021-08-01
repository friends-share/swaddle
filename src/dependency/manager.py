from src.core.apps import AppService
from src.core.cluster import ClusterManager
from src.core.command import CommandService

from src.core.group_data import GroupDataManager


class Manager:
    GROUPED_DATA_MANAGER = GroupDataManager()
    APP_MANAGER = AppService(GROUPED_DATA_MANAGER)
    CLUSTER_MANAGER = ClusterManager(GROUPED_DATA_MANAGER)
    COMMAND_SERVICE = CommandService()