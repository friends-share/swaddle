from src.core.deployer import Deployer
from src.dependency.manager import Manager

DEPLOYER = Deployer(Manager.APP_MANAGER, Manager.COMMAND_SERVICE, Manager.GROUPED_DATA_MANAGER)
