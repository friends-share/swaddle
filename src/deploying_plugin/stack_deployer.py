import json
from typing import Tuple, Optional

from src.core.deployment_plugin import Deploying
from src.core.group_data import GroupDataManager
from src.core.ssh import SSH
from src.model.apps import App
from src.model.commands import Command
from src.model.deploy import DeploymentStep, DeployingStack
from src.model.message import SimpleStatus, MinStatus
from src.model.server import Server


class StackDeployer(Deploying):

    def __init__(self, group_manager: GroupDataManager):
        self.group_manager = group_manager

    def define_process(self, stack: DeployingStack) -> Tuple[SimpleStatus, DeployingStack]:
        messages = []
        for app_fabric in stack.apps:
            for cluster_data in app_fabric.clusters:
                messages.append(
                    f"Deployed {app_fabric.app.name} using deployment method:{self._deploy(cluster_data.cluster.data.managers[0], app_fabric.app, stack.deployment_id)}")
        return SimpleStatus(status=MinStatus.RUNNING, messages=messages), stack

    def deployment_step(self) -> DeploymentStep:
        return DeploymentStep.DEPLOYMENT_5

    def entry_criteria(self, component: DeployingStack) -> Tuple[bool, Optional[str]]:
        return True, None

    def _deploy(self, server: Server, app: App, deployment_id: str):
        mechanism = None
        node = SSH.connect_server2(server)
        node.run(Command(command=f"mkdir {deployment_id}"))
        privileged = server.privileged
        if app.git:
            cmd_run = node.run_all(
                [
                    Command(command=f"cd {deployment_id}"),
                    Command(command=f"git clone {app.git.repo} ."),
                    Command(command=f"echo docker-compose -f {app.docker_file} build >{deployment_id}.sh",
                            privileged=privileged),
                    Command(command=f"echo docker stack deploy -c {app.docker_file} {app.name} >>{deployment_id}.sh",
                            privileged=privileged),
                    Command(command=f"echo 'status=$?'>>{deployment_id}.sh", privileged=privileged),
                    Command(command=f"echo 'touch {deployment_id}.$status' >>{deployment_id}.sh",
                            privileged=privileged),
                    Command(command=f"chmod +x {deployment_id}.sh", privileged=privileged),
                    Command(command=f"nohup ./{deployment_id}.sh &", privileged=privileged)
                ])
            if cmd_run == 1:
                raise Exception("Failed to deploy application")
            mechanism = "git"
        elif app.docker_compose:
            if node.run_all(
                    [
                        Command(command=f"cd {deployment_id}"),
                        Command(command=f"echo {json.dumps(app.docker_compose)} >> {app.name}.json"),
                        Command(command=f"docker-compose -f {app.name}.json build", privileged=privileged),
                        Command(command=f"docker stack deploy -c {app.name}.yml {app.name}", privileged=privileged)
                    ]) == 1:
                raise Exception("Failed to deploy application")
            mechanism = "dc"
        return mechanism
