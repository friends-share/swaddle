from src.core.service import AService, Id
from src.model.deploy import DeploymentLog


class DeploymentLogManager(AService[DeploymentLog, str]):

    def __init__(self, cache):
        super().__init__(cache)

    def get_id(self, obj: DeploymentLog) -> Id:
        return obj.deployment_id

    def update_status(self, deployment_id, deployment_step, deployment_status):
        found_data = self.get_by_id(deployment_id, DeploymentLog(deployment_id=deployment_id))
        status = found_data.status or {}
        status[deployment_step] = deployment_status
        found_data.status = status
        self.save_obj(found_data)
