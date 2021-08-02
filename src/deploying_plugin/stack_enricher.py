from typing import Tuple, Optional

from src.core.apps import AppService
from src.core.command import CommandService
from src.core.group_data import GroupDataManager
from src.model.deploy import DeploymentStep, EnrichedAppFabric, DeployingStack, \
    EnrichedClusterFabric, ClusterFabric, Stack
from src.model.message import SimpleStatus, MinStatus


class DeployingStackBuilder:
    app_service: AppService
    cmd_service: CommandService

    def __init__(self, app_service, cmd_service, group_manager: GroupDataManager):
        self.app_service = app_service
        self.cmd_service = cmd_service
        self.group_manager = group_manager

    def run_step(self, component: Stack, deployment_id) -> Tuple[DeploymentStep, SimpleStatus, Optional[DeployingStack]]:
        result, message = self.entry_criteria(component)
        if result:
            process = self.define_process(component, deployment_id)
            return self.deployment_step(), process[0], process[1]
        return self.deployment_step(), SimpleStatus(status=MinStatus.NOT_STARTED, messages=[message]), None

    def define_process(self, stack: Stack, deployment_id) -> Tuple[SimpleStatus, Optional[DeployingStack]]:
        enriched_app_fabrics = []
        group = stack.group
        for app_fabric in stack.apps:
            app_data = self.group_manager.get_app(group=group, app_name=app_fabric.app)
            if app_data is None:
                return SimpleStatus(status=MinStatus.FAILURE,
                                    errors=[f"No app_fabric defined with name {app_fabric.app}"]), None
            enriched_server_fabric = []
            if app_fabric.clusters is None:
                clusters = self.group_manager.get_clusters(group)
                app_fabric.clusters = [ClusterFabric(cluster=cluster.cluster_id, preparation=[cmd.name for cmd in
                                                                                              cluster.data.environment_setup] if cluster.data.environment_setup else None)
                                       for cluster in clusters]
            for cluster_fabric in app_fabric.clusters:
                cluster_data = self.group_manager.get_cluster(group=group, cluster_name=cluster_fabric.cluster)
                if cluster_data is None:
                    return SimpleStatus(status=MinStatus.FAILURE,
                                        errors=[f"No cluster defined with name {cluster_fabric.cluster}"]), None
                enriched_commands = []
                if cluster_fabric.preparation:
                    for cmd_name in cluster_fabric.preparation:
                        command_group = self.cmd_service.get_obj_components(cmd_name, cluster_data.data.type)
                        if command_group is None:
                            return SimpleStatus(status=MinStatus.FAILURE,
                                                errors=[
                                                    f"No command defined with name:{cmd_name} for server type: {cluster_data.data.type}"]), None
                        else:
                            enriched_commands.append(command_group)
                enriched_server_fabric.append(
                    EnrichedClusterFabric(cluster=cluster_data, preparation=enriched_commands))
            enriched_app_fabrics.append(EnrichedAppFabric(app=app_data, clusters=enriched_server_fabric))
        return SimpleStatus(status=MinStatus.SUCCESS), DeployingStack(deployment_id=deployment_id, name=stack.name,
                                                                      based_on=stack.based_on,
                                                                      apps=enriched_app_fabrics, group=group)

    def deployment_step(self):
        return DeploymentStep.DEPLOY_CONFIG_VALIDITY_0

    def entry_criteria(self, component: Stack) -> Tuple[bool, str]:
        return component is not None, "Deployment Config cannot be empty"
