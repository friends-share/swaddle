from typing import Tuple, Optional

from src.core.deployment_plugin import Deploying
from src.core.infra_quality import InfraMatcher
from src.model.deploy import DeploymentStep, DeployingStack
from src.model.message import SimpleStatus, MinStatus


class InfraRequirementMatcher(Deploying):

    def __init__(self):
        self.infra_matcher = InfraMatcher()

    def define_process(self, component: DeployingStack) -> Tuple[SimpleStatus, Optional[DeployingStack]]:
        for app_fabric in component.apps:
            matched_servers = self.infra_matcher.match(app_fabric.clusters, app_fabric.app)
            if matched_servers is None or len(matched_servers) < 1:
                return SimpleStatus(status=MinStatus.FAILURE,
                                    errors=[f"No infra match found for app: {app_fabric.app.name}"]), None
            app_fabric.clusters = matched_servers
        return SimpleStatus(status=MinStatus.SUCCESS,
                            messages=[
                                f"Infra requirements were matched successfully for stack: {component.name}"]), component

    def deployment_step(self) -> DeploymentStep:
        return DeploymentStep.INFRA_REQUIREMENT_MATCH_3

    def entry_criteria(self, component: DeployingStack) -> Tuple[bool, Optional[str]]:
        for app_fabric in component.apps:
            if app_fabric.clusters is None or len(app_fabric.clusters) < 1:
                return False, f"No cluster found for {app_fabric.app.name}"
        return True, None
