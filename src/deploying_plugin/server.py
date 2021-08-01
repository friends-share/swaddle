from typing import Tuple, Optional

from src.core.deployment_plugin import Deploying
from src.core.docker import Swarmer
from src.core.group_data import GroupDataManager
from src.model.cluster_log import ClusterLog
from src.model.deploy import DeploymentStep, EnrichedClusterFabric, DeployingStack
from src.model.message import SimpleStatus, MinStatus


class ClusterInit(Deploying):

    def __init__(self, grouped_data_manager: GroupDataManager, command_service):
        self.grouped_data_manager = grouped_data_manager
        self.command_service = command_service

    def define_process(self, stack: DeployingStack) -> Tuple[SimpleStatus, Optional[DeployingStack]]:
        messages = []
        method = stack.based_on
        for app_fabric in stack.apps:
            for cluster_fabric in app_fabric.clusters:
                cluster = cluster_fabric.cluster
                cluster_data = self.grouped_data_manager.get_by_id(cluster.cluster_id,
                                                                   ClusterLog(cluster=cluster, preparation_done={}))
                if not cluster_data.preparation_done:
                    if cluster_fabric.preparation:
                        self.command_service.process(cluster_data.cluster, cluster_fabric.preparation)
                    status = Swarmer(cluster).init()
                    if status:
                        cluster_data.preparation_done = True
                        self.grouped_data_manager.save_obj(cluster_data)
                        messages.append(f"Cluster {cluster.cluster_id} initialised successfully")
                    else:
                        return SimpleStatus(status=MinStatus.FAILURE, errors=[f"Failed to init {cluster.cluster_id}"], messages=messages), None
                else:
                    messages.append(f"Cluster {cluster.cluster_id} was already initialised")
            return SimpleStatus(status=MinStatus.SUCCESS, messages=messages), stack

    def deployment_step(self) -> DeploymentStep:
        return DeploymentStep.CLUSTER_INIT_4

    def entry_criteria(self, component: DeployingStack) -> Tuple[bool, Optional[str]]:
        return True, None


class ClusterConfigValidator(Deploying):

    def __init__(self, group_repo):
        self.group_repo = group_repo

    def define_process(self, component: DeployingStack) -> Tuple[SimpleStatus, Optional[DeployingStack]]:
        messages = []
        for app_fabric in component.apps:
            if app_fabric.clusters is None or len(app_fabric.clusters) == 0:
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
                messages.append(
                    f"Cluster data for {app_fabric.app.name} is populated by system pending infra check")
        return SimpleStatus(status=MinStatus.SUCCESS, messages=messages), component

    def deployment_step(self) -> DeploymentStep:
        return DeploymentStep.CLUSTER_CONFIG_VALIDATOR_2

    def entry_criteria(self, component: DeployingStack) -> Tuple[bool, str]:
        return component is not None and len(component.apps) > 0, "No apps are defined to deploy"
