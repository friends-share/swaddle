import abc
from typing import Tuple, Optional

from src.model.deploy import DeploymentStep, DeployingStack
from src.model.message import SimpleStatus, MinStatus


class Deploying(abc.ABC):

    def run_step(self, component: DeployingStack) -> Tuple[DeploymentStep, SimpleStatus, Optional[DeployingStack]]:
        result, message = self.entry_criteria(component)
        if result:
            process = self.define_process(component)
            return self.deployment_step(), process[0], process[1]
        return self.deployment_step(), SimpleStatus(status=MinStatus.NOT_STARTED, messages=[message]), None

    @abc.abstractmethod
    def define_process(self, component: DeployingStack) -> Tuple[SimpleStatus, Optional[DeployingStack]]:
        pass

    @abc.abstractmethod
    def deployment_step(self) -> DeploymentStep:
        pass

    @abc.abstractmethod
    def entry_criteria(self, component: DeployingStack) -> Tuple[bool, str]:
        pass
