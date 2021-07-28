import json
from typing import Tuple, Optional

from src.core.deploying import Deploying, Component
from src.core.ssh import SSH
from src.model.apps import App, AppStack
from src.model.commands import Command
from src.model.deploy import EnrichedDeploymentConfig, DeploymentStep
from src.model.message import SimpleStatus, MinStatus
from src.model.server import Server


class StackDeployer(Deploying[EnrichedDeploymentConfig, EnrichedDeploymentConfig]):

    def __init__(self, cluster_manager, cluster_log_manager, app_log_manager):
        self.cluster_manager = cluster_manager
        self.cluster_log_manager = cluster_log_manager
        self.app_log_manager = app_log_manager

    def define_process(self, component: EnrichedDeploymentConfig) -> Tuple[SimpleStatus, EnrichedDeploymentConfig]:
        for stack in component.stacks:
            for app_fabric in stack.apps:
                for cluster_fabric in app_fabric.fabric:
                    cluster_data = self.cluster_manager.get_by_id(cluster_fabric.cluster.cluster_id)
                    self._deploy(cluster_data.data.managers[0],
                                 app_fabric.app)
                    self.add_app_log(app_fabric, cluster_data, stack)
                    self.add_cluster_log(app_fabric, cluster_data)
        return SimpleStatus(status=MinStatus.SUCCESS), component

    def add_cluster_log(self, app_fabric, cluster_data):
        cluster_log = self.cluster_log_manager.get_by_id(cluster_data.cluster_id)
        data = cluster_log.deployed_apps or []
        cluster_log.deployed_apps = data.append(app_fabric.app)
        self.cluster_log_manager.save_obj(cluster_log)

    def add_app_log(self, app_fabric, cluster_data, stack):
        app_log = self.app_log_manager.get_by_id(app_fabric.app.name)
        data = app_log.deployments or []
        data.append(AppStack(stack_name=stack.name, deployed_in=cluster_data.data))
        app_log.deployments = data
        self.app_log_manager.save_obj(app_log)

    def deployment_step(self) -> DeploymentStep:
        return DeploymentStep.DEPLOYMENT_5

    def entry_criteria(self, component: Component) -> Tuple[bool, Optional[str]]:
        return True, None

    def _deploy(self, server: Server, app: App):
        mechanism = None
        node = SSH.connect_server(server)
        if app.git:
            if len(node.run_safe([Command(f"git clone {app.git.repo}"),
                                  Command(f"docker-compose build", True),
                                  Command(f"docker stack -c docker-compose.yml {app.name}")])) < 3:
                raise Exception("Failed to deploy application")
            mechanism = "git"
        elif app.docker_compose:
            if len(node.run_safe([Command(f"echo {json.dumps(app.docker_compose)} >> {app.name}.json"),
                                  Command(f"docker-compose -f {app.name}.json build", True),
                                  Command(f"docker stack -c {app.name}.yml {app.name}")])) < 3:
                raise Exception("Failed to deploy application")
            mechanism = "dc"
        return mechanism
