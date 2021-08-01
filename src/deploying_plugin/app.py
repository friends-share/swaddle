from typing import Tuple

from src.core.deployment_plugin import Deploying
from src.core.group_data import GroupDataManager
from src.model.deploy import DeploymentStep, DeployingStack
from src.model.message import SimpleStatus, MinStatus


class AppConfigSearcher(Deploying):

    def __init__(self, group_manager: GroupDataManager):
        self.group_manager = group_manager

    def define_process(self, component: DeployingStack) -> Tuple[SimpleStatus, DeployingStack]:
        messages = []
        for app_fabric in component.apps:
            name = app_fabric.app.name
            app_log = self.group_manager.get_app_log(app_fabric.app.group, name)
            if app_log is not None and app_log.deployments is not None and len(app_log.deployments) > 0:
                messages.append(f"App: {name} already deployed")
        return SimpleStatus(status=MinStatus.SUCCESS, messages=messages), component

    def deployment_step(self) -> DeploymentStep:
        return DeploymentStep.APP_CONFIG_SEARCH_1

    def entry_criteria(self, component: DeployingStack) -> Tuple[bool, str]:
        return component is not None and len(component.apps) > 0, "No stacks are defined to deploy"
