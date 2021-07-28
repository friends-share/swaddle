from typing import Tuple

from src.core.deploying import Deploying, Component, Result
from src.dependency.manager import Manager
from src.model.deploy import DeploymentStep, EnrichedStack, EnrichedDeploymentConfig
from src.model.message import SimpleStatus, MinStatus


class AppDeployment(Deploying[EnrichedDeploymentConfig, EnrichedDeploymentConfig]):

    def define_process(self, component: EnrichedDeploymentConfig) -> Tuple[SimpleStatus, EnrichedDeploymentConfig]:

        pass

    def deployment_step(self) -> DeploymentStep:
        return DeploymentStep.DEPLOYMENT_5

    def entry_criteria(self, component: EnrichedDeploymentConfig) -> Tuple[bool, str]:
        pass


class AppConfigSearcher(Deploying[EnrichedStack, EnrichedStack]):

    def __init__(self, app_log_manager):
        self.log = app_log_manager

    def define_process(self, component: EnrichedStack) -> Tuple[SimpleStatus, EnrichedStack]:
        messages = []
        for app_fabric in component.apps:
            name = app_fabric.app.name
            app_log = self.log.get_by_id(name)
            if app_log is not None and app_log.deployments is not None and app_log.deployments.deployed_in is not None:
                messages.append(f"App: {name} already deployed")
        return SimpleStatus(status=MinStatus.SUCCESS, messages=messages), component

    def deployment_step(self) -> DeploymentStep:
        return DeploymentStep.APP_CONFIG_SEARCH_1

    def entry_criteria(self, component: EnrichedStack) -> Tuple[bool, str]:
        return component is not None and len(component.apps) > 0, "No apps are defined to deploy"
