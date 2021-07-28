from src.core.deployment_log import DeploymentLogManager
from src.dependency.deployers import DeploymentConfigProcessors
from src.model.deploy import DeploymentLog, DeployConfig
from src.model.message import MinStatus


class Deployer:

    def __init__(self, deployment_log_manager: DeploymentLogManager):
        self.deployment_log_manager = deployment_log_manager

    _processors = [
        DeploymentConfigProcessors.STEP_0,
        DeploymentConfigProcessors.STEP_1,
        DeploymentConfigProcessors.STEP_2,
        DeploymentConfigProcessors.STEP_3,
        DeploymentConfigProcessors.STEP_4,
        DeploymentConfigProcessors.STEP_5
    ]

    def deploy(self, deploy_config: DeployConfig, deployment_id):
        step, status, starter = None, None, deploy_config
        self.deployment_log_manager.save_obj(DeploymentLog(deployment_id=deployment_id, config=deploy_config))
        for each in self._processors:
            step, status, starter = each.run_step(starter)
            self.deployment_log_manager.update_status(deployment_id, step, status)
            if status.status == MinStatus.FAILURE:
                break
        return self.deployment_log_manager.get_by_id(deployment_id)
