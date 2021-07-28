from typing import Tuple, Optional

from src.core.apps import AppService
from src.core.cluster import ClusterManager
from src.core.command import CommandService
from src.core.deploying import Deploying
from src.core.group_data import GroupDataManager
from src.model.deploy import DeployConfig, DeploymentStep, EnrichedDeploymentConfig, EnrichedAppFabric, EnrichedStack, \
    EnrichedClusterFabric, ClusterFabric
from src.model.message import SimpleStatus, MinStatus


class DeploymentConfigValidator(Deploying[DeployConfig, EnrichedDeploymentConfig]):
    app_service: AppService
    cmd_service: CommandService
    cluster_manager: ClusterManager

    def __init__(self, app_service, cmd_service, cluster_manager, group_manager):
        self.app_service = app_service
        self.cmd_service = cmd_service
        self.cluster_manager = cluster_manager
        self.group_manager = group_manager

    def define_process(self, component: DeployConfig) -> Tuple[SimpleStatus, Optional[EnrichedDeploymentConfig]]:
        enriched_stacks = []
        for stack in component.stacks:
            enriched_app_fabrics = []
            for app_fabric in stack.apps:
                app_data = self.app_service.get_by_id(app_fabric.app)
                if app_data is None:
                    return SimpleStatus(status=MinStatus.FAILURE,
                                        errors=[f"No app_fabric defined with name {app_fabric.app}"]), None
                enriched_server_fabric = []
                if app_fabric.fabric is None:
                    clusters = self.group_manager.get_by_id(app_data.group).clusters.values()
                    cluster_fabric_managed = [ClusterFabric(cluster=cluster.cluster_id,preparation=cluster.data.environment_setup) for cluster in clusters]
                    app_fabric.fabric = cluster_fabric_managed
                for cluster_fabric in app_fabric.fabric:
                    cluster_data = self.cluster_manager.get_by_id(cluster_fabric.cluster)
                    if cluster_data is None:
                        return SimpleStatus(status=MinStatus.FAILURE,
                                            errors=[f"No cluster defined with name {cluster_fabric.cluster}"]), None
                    enriched_commands = []
                    if cluster_fabric.preparation:
                        for cmd_name in cluster_fabric.preparation:
                            command_group = self.cmd_service.get_id_components(cmd_name, cluster_data.type)
                            if command_group is None:
                                return SimpleStatus(status=MinStatus.FAILURE,
                                                    errors=[
                                                        f"No command defined with name:{cmd_name} for server type: {cluster_data.data.type}"]), None
                            enriched_commands.append(command_group)
                    enriched_server_fabric.append(
                        EnrichedClusterFabric(cluster=cluster_data, preparation=enriched_commands))
                enriched_app_fabrics.append(EnrichedAppFabric(app=app_data, fabric=enriched_server_fabric))
            enriched_stacks.append(EnrichedStack(apps=enriched_app_fabrics))
        return SimpleStatus(status=MinStatus.SUCCESS), EnrichedDeploymentConfig(name=component.name,
                                                                                stacks=enriched_stacks)

    def deployment_step(self):
        return DeploymentStep.DEPLOY_CONFIG_VALIDITY_0

    def entry_criteria(self, component: DeployConfig) -> Tuple[bool, str]:
        return component is not None, "Deployment Config cannot be empty"
