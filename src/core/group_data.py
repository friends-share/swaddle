from src.core.service import AService, Id
from src.dependency import grouped_data_store
from src.model.apps import App, AppLog
from src.model.cluster_log import ClusterLog
from src.model.deploy import DeploymentLog, DeploymentMethod, DeploymentStep
from src.model.group import GroupData
from src.model.message import SimpleStatus
from src.model.server import Cluster


class GroupDataManager(AService[GroupData, str]):

    def __init__(self):
        super().__init__(grouped_data_store)

    def is_cluster_ready(self, cluster: Cluster, method: DeploymentMethod):
        group = cluster.group
        cluster = (self.get_by_id(group, GroupData(name=group)).clusters or {}).get(cluster.cluster_id)
        return (cluster.preparation_done or {}).get(method, False) if cluster else False

    def set_cluster_ready(self, cluster: Cluster, method: DeploymentMethod):
        group = cluster.group
        cluster_id = cluster.cluster_id
        saved_data = self.get_by_id(group, GroupData(name=group))
        cluster_log = (saved_data.clusters or {})
        cluster = cluster_log.get(cluster_id, None)
        if cluster:
            prep = cluster.preparation_done or {}
            prep[method] = True
            cluster.preparation_done = prep
            cluster_log[cluster_id] = cluster
            saved_data.clusters = cluster_log
            self.save_obj(saved_data)
            return True
        raise Exception("No cluster information found against group")

    def add_cluster(self, cluster: Cluster):
        saved_data = self.get_by_id(cluster.group, GroupData(name=cluster.group))
        clusters = saved_data.clusters or {}
        clusters[cluster.cluster_id] = ClusterLog(cluster=cluster)
        saved_data.clusters = clusters
        self.save_obj(saved_data)

    def get_clusters(self, group: str):
        return [clusters.cluster for clusters in
                self.get_by_id(group, GroupData(name=group, clusters={})).clusters.values()]

    def get_clusters_envt(self, group: str):
        return [clusters.cluster.data.environment_setup for clusters in
                self.get_by_id(group, GroupData(name=group, clusters={})).clusters.values()]

    def get_app_log(self, group: str, app_name: str):
        return self.get_by_id(group, GroupData(name=group, apps={})).apps.get(app_name, None)

    def get_cluster_log(self, group: str, cluster_id: str):
        return self.get_by_id(group, GroupData(name=group, clusters={})).clusters.get(cluster_id, None)

    def add_app(self, app: App):
        saved_data = self.get_by_id(app.group, GroupData(name=app.group))
        saved_apps = saved_data.apps or {}
        saved_apps[app.name] = AppLog(app=app)
        saved_data.apps = saved_apps
        self.save_obj(saved_data)

    def get_app(self, group: str, app_name: str):
        apps = self.get_by_id(group, GroupData(name=group)).apps
        if apps and apps.get(app_name, None):
            return apps.get(app_name).app
        return None

    def get_cluster(self, group: str, cluster_name: str):
        clusters = self.get_by_id(group, GroupData(name=group)).clusters
        if clusters and clusters.get(cluster_name, None):
            return clusters.get(cluster_name).cluster
        return None

    def get_deployment_log(self, group: str, deployment_id: str):
        return self.get_by_id(group, GroupData(name=group, deployment_details={})).deployment_details.get(deployment_id)

    def add_deployment(self, deployment_log: DeploymentLog):
        saved_data = self.get_by_id(deployment_log.group, GroupData(name=deployment_log.group))
        deployment_details = saved_data.deployment_details or {}
        deployment_details[deployment_log.deployment_id] = deployment_log
        saved_data.deployment_details = deployment_details
        saved_data = self._save_cluster_log(deployment_log, saved_data)
        saved_data = self._save_app_log(deployment_log, saved_data)
        self.save_obj(saved_data)

    def update_deployment_status(self, deployment_id:str, group: str, deployment_step: DeploymentStep, status: SimpleStatus):
        saved_data = self.get_by_id(group, GroupData(name=group))
        deployment_details = saved_data.deployment_details[deployment_id]
        deployment_details.status[deployment_step] = status
        saved_data.deployment_details[deployment_id] = deployment_details
        self.save_obj(saved_data)

    def _save_cluster_log(self, deployment_log: DeploymentLog, grouped_data: GroupData):
        config = deployment_log.config
        for app_fabric in config.apps:
            for cluster_fabric in app_fabric.clusters:
                cluster_log = grouped_data.clusters.get(cluster_fabric.cluster.cluster_id,
                                                        ClusterLog(cluster=cluster_fabric.cluster))
                plugged = cluster_log.deployed_apps or {}
                plugged[app_fabric.app.name] = app_fabric.app
                cluster_log.deployed_apps = plugged
                grouped_data.clusters[cluster_fabric.cluster.cluster_id] = cluster_log
        return grouped_data

    def _save_app_log(self, deployment_log: DeploymentLog, grouped_data: GroupData):
        for app_fabric in deployment_log.config.apps:
            app_log = grouped_data.apps.get(app_fabric.app.name, AppLog(app=app_fabric.app))
            for cluster_fabric in app_fabric.clusters:
                plugged = app_log.deployments or {}
                app_deployments = plugged.get(str(cluster_fabric.cluster.cluster_id), [])
                app_deployments.append(deployment_log.deployment_id)
                plugged[cluster_fabric.cluster.cluster_id] = app_deployments
                app_log.deployments = plugged
                grouped_data.apps[app_fabric.app.name] = app_log
        return grouped_data

    def get_id(self, obj: GroupData) -> Id:
        return obj.name
