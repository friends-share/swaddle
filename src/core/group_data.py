from src.core.service import AService, Id
from src.dependency import grouped_data_store
from src.model.apps import App
from src.model.group import GroupData
from src.model.server import Cluster


class GroupDataManager(AService[GroupData, str]):

    def __init__(self):
        super().__init__(grouped_data_store)

    def add_cluster(self, cluster: Cluster):
        saved_data = self.get_by_id(cluster.group, GroupData(name=cluster.group))
        clusters = saved_data.clusters or {}
        clusters[cluster.cluster_id] = cluster
        saved_data.clusters = clusters
        self.save_obj(saved_data)

    def add_app(self, app: App):
        saved_data = self.get_by_id(app.group,  GroupData(name=app.group))
        saved_apps = saved_data.apps or {}
        saved_apps[app.name] = app
        saved_data.apps = saved_apps
        self.save_obj(saved_data)

    def get_id(self, obj: GroupData) -> Id:
        return obj.name
