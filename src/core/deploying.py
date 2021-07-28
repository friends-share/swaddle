import abc
from typing import Generic, TypeVar, Tuple, Optional

from src.model.deploy import DeploymentStep
from src.model.message import SimpleStatus, MinStatus

Component = TypeVar('Component')
Result = TypeVar('Result')


class Deploying(abc.ABC, Generic[Component, Result]):

    def run_step(self, component: Component) -> Tuple[DeploymentStep, SimpleStatus, Optional[Result]]:
        result, message = self.entry_criteria(component)
        if result:
            process = self.define_process(component)
            return self.deployment_step(), process[0], process[1]
        return self.deployment_step(), SimpleStatus(status=MinStatus.NOT_STARTED, messages=[message]), None

    @abc.abstractmethod
    def define_process(self, component: Component) -> Tuple[SimpleStatus, Result]:
        pass

    @abc.abstractmethod
    def deployment_step(self) -> DeploymentStep:
        pass

    @abc.abstractmethod
    def entry_criteria(self, component: Component) -> Tuple[bool, str]:
        pass
