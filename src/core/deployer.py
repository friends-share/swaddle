from src.core.group_data import GroupDataManager
from src.deploying_plugin.plugins import DeploymentAccessory
from src.deploying_plugin.stack_enricher import DeployingStackBuilder
from src.model.deploy import DeploymentLog, Stack
from src.model.message import MinStatus


class Deployer:

    def __init__(self, app_service, cmd_service, grouped_data_manager: GroupDataManager):
        self.grouped_data_manager = grouped_data_manager
        self.stack_builder = DeployingStackBuilder(app_service, cmd_service, grouped_data_manager)

    def deploy(self, stack: Stack, deployment_id):
        step, status, starter = self.stack_builder.run_step(stack, deployment_id)
        if status.status == MinStatus.FAILURE:
            raise Exception(status.errors)
        self.grouped_data_manager.add_deployment(
            DeploymentLog(deployment_id=deployment_id, config=starter, group=stack.group, status={step: status}))
        for each in DeploymentAccessory.PLUGINS:
            step, status, starter = each.run_step(starter)
            self.grouped_data_manager.update_deployment_status(deployment_id=deployment_id, group=stack.group, deployment_step=step, status=status)
            if status.status == MinStatus.FAILURE:
                break
        return self.grouped_data_manager.get_deployment_log(stack.group, deployment_id)
