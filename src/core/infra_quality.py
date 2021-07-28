from typing import List, Callable

from src.dependency.manager import Manager
from src.model.apps import App
from src.model.deploy import EnrichedClusterFabric


class InfraMatcher:

    def __init__(self):
        self.log = Manager.CLUSTER_LOG_MANAGER

    def match(self, clusters: List[EnrichedClusterFabric], app: App):
        perfect_match: Callable[[EnrichedClusterFabric], bool] = lambda x: x.cluster.data.qualities.match(app.qualities) and \
                                                            self._deployment_check(x)
        return list(filter(perfect_match, clusters))

    def _deployment_check(self, x: EnrichedClusterFabric):
        return self.log.get(x.cluster.cluster_id, None) is None or \
                         x.cluster.data.max_deployments > len(self.log.get(x.cluster.cluster_id).deployed)
