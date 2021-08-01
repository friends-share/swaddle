import datetime
import uuid

from src import dependency
from src.core.service import AService, Id
from src.model.server import Cluster, ClusterData


class ClusterManager(AService[Cluster, str]):

    def __init__(self, group_data_manager):
        super().__init__(dependency.cluster_data_store)
        self.group_data_manager = group_data_manager

    def get_id(self, obj: Cluster) -> Id:
        return obj.cluster_id

    def save(self, obj: ClusterData, group: str) -> Cluster:
        cluster = Cluster(cluster_id=uuid.uuid4().hex[:6].upper(), data=obj, created_on=datetime.datetime.now(),
                          group=group)
        if self.save_obj(cluster):
            self.group_data_manager.add_cluster(cluster)
            return cluster
        return None
