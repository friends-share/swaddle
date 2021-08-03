from time import sleep

from fastapi import BackgroundTasks

from src.core.group_data import GroupDataManager
from src.core.ssh import SSH
from src.deploying_plugin.plugins import DeploymentAccessory
from src.deploying_plugin.stack_enricher import DeployingStackBuilder
from src.model.commands import Command
from src.model.deploy import DeploymentLog, Stack, DeploymentStep
from src.model.message import MinStatus, SimpleStatus
from loguru import logger


class Deployer:

    def __init__(self, app_service, cmd_service, grouped_data_manager: GroupDataManager):
        self.grouped_data_manager = grouped_data_manager
        self.stack_builder = DeployingStackBuilder(app_service, cmd_service, grouped_data_manager)

    def verify_deployment(self, group: str, deployment_id: str):
        deployment_log = self.grouped_data_manager.get_deployment_log(group, deployment_id)
        logger.info("Deployment watch triggered for {}", deployment_id)
        message = []
        errors = []
        break_run = False
        cluster_count = 0
        while not break_run:
            sleep(30)
            cluster_count = 0
            for app in deployment_log.config.apps:
                for cluster in app.clusters:
                    cluster_count = cluster_count + 1
                    manager_server = cluster.cluster.data.managers[0]
                    status = SSH.connect_server(manager_server).run(
                        Command(command=f"ls {deployment_id} | grep {deployment_id} | grep -v sh")
                    )
                    if f"{deployment_id}.0" in status.out and status.status == 0:
                        message.append(f"Successful deployment in {cluster.cluster.cluster_id}")
                    elif f"{deployment_id}." in status.out and status.status == 0:
                        errors.append(f"Successful deployment in {cluster.cluster.cluster_id}")
            break_run = len(message) + len(errors) == cluster_count
        success = len(message) == cluster_count
        self.grouped_data_manager.update_deployment_status(deployment_id, group,
                                                           deployment_step=DeploymentStep.DEPLOYMENT_5,
                                                           status=SimpleStatus(
                                                               status=MinStatus.SUCCESS if success else MinStatus.FAILURE,
                                                               errors=errors, messages=message))

    def deploy(self, stack: Stack, deployment_id, background_tasks: BackgroundTasks):
        step, status, starter = self.stack_builder.run_step(stack, deployment_id)
        if status.status == MinStatus.FAILURE:
            raise Exception(status.errors)
        self.grouped_data_manager.add_deployment(
            DeploymentLog(deployment_id=deployment_id, config=starter, group=stack.group, status={step: status}))
        for each in DeploymentAccessory.PLUGINS:
            try:
                step, status, starter = each.run_step(starter)
                self.grouped_data_manager.update_deployment_status(deployment_id=deployment_id, group=stack.group,
                                                                   deployment_step=step, status=status)
                if status.status == MinStatus.FAILURE:
                    break
            except Exception as e:
                self.grouped_data_manager.update_deployment_status(deployment_id=deployment_id, group=stack.group,
                                                                   deployment_step=each.deployment_step(),
                                                                   status=SimpleStatus(status=MinStatus.FAILURE,
                                                                                       errors=[str(e)]))
                break
        if status == MinStatus.RUNNING:
            background_tasks.add_task(self.verify_deployment, stack.group, deployment_id)
            logger.info("{} deployment watch added to background", deployment_id)
        else:
            logger.info("No deployment watch added")
        return self.grouped_data_manager.get_deployment_log(stack.group, deployment_id)
