from typing import Tuple, Optional

from src.core.deploying import Deploying
from src.core.infra_quality import InfraMatcher
from src.model.deploy import EnrichedDeploymentConfig, DeploymentStep
from src.model.message import SimpleStatus, MinStatus


class InfraRequirementMatcher(Deploying[EnrichedDeploymentConfig, EnrichedDeploymentConfig]):

    def __init__(self):
        self.infra_matcher = InfraMatcher()

    def define_process(self, component: EnrichedDeploymentConfig) -> Tuple[SimpleStatus, Optional[EnrichedDeploymentConfig]]:
        for deploy_config in component.stacks:
            for app_fabric in deploy_config.apps:
                matched_servers = self.infra_matcher.match(app_fabric.fabric, app_fabric.app)
                if not matched_servers or len(matched_servers) < 1:
                    return SimpleStatus(status=MinStatus.FAILURE, errors=[f"No infra match found for app: {app_fabric.app.name}"]), None
                app_fabric.fabric = matched_servers
        return SimpleStatus(status=MinStatus.SUCCESS, messages=[f"Infra requirements were matched successfully for "
                                                                f"apps in stack"]), component

    def deployment_step(self) -> DeploymentStep:
        return DeploymentStep.INFRA_REQUIREMENT_MATCH_3

    def entry_criteria(self, component: EnrichedDeploymentConfig) -> Tuple[bool, Optional[str]]:
        for stack in component.stacks:
            for app_fabric in stack.apps:
                if app_fabric.fabric is None or len(app_fabric.fabric) < 1:
                    return False, f"No cluster found for {app_fabric.app.name}"
        return True, None
