from src.dependency.manager import Manager
from src.deploying.app import AppConfigSearcher
from src.deploying.deploy import DeploymentConfigValidator
from src.deploying.docker_deployer import StackDeployer
from src.deploying.infra import InfraRequirementMatcher
from src.deploying.server import ClusterConfigSearcher, ClusterInit


class DeploymentConfigProcessors:
    STEP_0 = DeploymentConfigValidator(Manager.APP_MANAGER, Manager.COMMAND_SERVICE, Manager.COMMAND_SERVICE, Manager.GROUPED_DATA_MANAGER)
    STEP_1 = AppConfigSearcher(Manager.APP_LOG_MANAGER)
    STEP_2 = ClusterConfigSearcher(Manager.GROUPED_DATA_MANAGER)
    STEP_3 = InfraRequirementMatcher()
    STEP_4 = ClusterInit(Manager.CLUSTER_LOG_MANAGER)
    STEP_5 = StackDeployer(Manager.CLUSTER_MANAGER, Manager.CLUSTER_LOG_MANAGER, Manager.APP_LOG_MANAGER)
