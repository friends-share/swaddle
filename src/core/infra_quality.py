from typing import List, Callable

from src.core.group_data import GroupDataManager
from src.dependency.manager import Manager
from src.model.apps import App
from src.model.deploy import EnrichedClusterFabric


class InfraMatcher:

    log: GroupDataManager

    def __init__(self):
        self.log = Manager.GROUPED_DATA_MANAGER

    def match(self, clusters: List[EnrichedClusterFabric], app: App):
        perfect_match: Callable[[EnrichedClusterFabric], bool] = lambda x: x.cluster.data.qualities.match(app.qualities) and self._deployment_check(x)
        filtered_list = list(filter(perfect_match, clusters))
        return filtered_list[0:app.availability] if len(filtered_list) >= app.availability else None

    def _deployment_check(self, x: EnrichedClusterFabric):
        cluster_log = self.log.get_cluster_log(group=x.cluster.group, cluster_id=x.cluster.cluster_id)
        return cluster_log is None or x.cluster.data.max_deployments > len(cluster_log.deployed_apps)