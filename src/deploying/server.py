from typing import Tuple, Optional

from src.core.deploying import Deploying
from src.core.docker import Swarmer
from src.dependency.manager import Manager
from src.model.cluster_log import ClusterLog
from src.model.deploy import DeploymentStep, EnrichedStack, EnrichedClusterFabric, EnrichedDeploymentConfig
from src.model.message import SimpleStatus, MinStatus


class ClusterInit(Deploying[EnrichedDeploymentConfig, EnrichedDeploymentConfig]):

    def __init__(self, cluster_log_manager):
        self.log = cluster_log_manager

    def define_process(self, component: EnrichedDeploymentConfig) -> Tuple[SimpleStatus, Optional[EnrichedDeploymentConfig]]:
        messages = []
        for stack in component.stacks:
            for app_fabric in stack.apps:
                for cluster_fabric in app_fabric.fabric:
                    cluster = cluster_fabric.cluster
                    cluster_data = self.log.get_by_id(cluster.cluster_id, None) or ClusterLog(log_id=cluster.cluster_id, cluster=cluster, preparation_done=False)
                    if not cluster_data.preparation_done:
                        status = Swarmer(cluster).init()
                        if status:
                            cluster_data.preparation_done = True
                            self.log.save_obj(cluster_data)
                            messages.append(f"Cluster {cluster.cluster_id} initialised successfully")
                        else:
                            return SimpleStatus(status=MinStatus.FAILURE, errors=[f"Failed to init {cluster.cluster_id}"], messages=messages), None
                    else:
                        messages.append(f"Cluster {cluster.cluster_id} was already initialised")

        return SimpleStatus(status=MinStatus.SUCCESS, messages=messages), component

    def deployment_step(self) -> DeploymentStep:
        return DeploymentStep.CLUSTER_INIT_4

    def entry_criteria(self, component: EnrichedDeploymentConfig) -> Tuple[bool, Optional[str]]:
        return True, None


class ClusterConfigSearcher(Deploying[EnrichedStack, EnrichedStack]):

    def __init__(self, group_repo):
        self.group_repo = group_repo

    def define_process(self, component: EnrichedStack) -> Tuple[SimpleStatus, Optional[EnrichedStack]]:
        messages = []
        for app_fabric in component.apps:
            if app_fabric.fabric is None or len(app_fabric.fabric) == 0:
                group = app_fabric.app.group
                group_app_cluster = self.group_repo.get_by_id(group, None)
                if group_app_cluster is None or group_app_cluster.clusters is None:
                    return SimpleStatus(status=MinStatus.FAILURE,
                                        errors=[f"No cluster are available for given group {group}"]), None
                data = []
                for cluster in group_app_cluster.clusters.values():
                    data.append(
                        EnrichedClusterFabric(cluster=cluster, preparation=cluster.data.environment_setup))
                app_fabric.fabric = data
                messages.append(f"Cluster data for {app_fabric.app.name} is populated by system pending infra check")
        return SimpleStatus(status=MinStatus.SUCCESS, messages=messages), component

    def deployment_step(self) -> DeploymentStep:
        return DeploymentStep.CLUSTER_CONFIG_SEARCH_2

    def entry_criteria(self, component: EnrichedStack) -> Tuple[bool, str]:
        return component is not None and len(component.apps) > 0, "No apps are defined to deploy"
