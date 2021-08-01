from src.dependency.manager import Manager
from src.deploying_plugin.app import AppConfigSearcher
from src.deploying_plugin.infra import InfraRequirementMatcher
from src.deploying_plugin.server import ClusterConfigValidator, ClusterInit
from src.deploying_plugin.stack_deployer import StackDeployer


class DeploymentAccessory:
    PLUGINS = [
        AppConfigSearcher(Manager.GROUPED_DATA_MANAGER),
        ClusterConfigValidator(Manager.GROUPED_DATA_MANAGER),
        InfraRequirementMatcher(),
        ClusterInit(Manager.GROUPED_DATA_MANAGER, Manager.COMMAND_SERVICE),
        StackDeployer(Manager.GROUPED_DATA_MANAGER),
    ]
