from src.core.deployer import Deployer
from src.dependency.manager import Manager


class Deployers:
    SWARM_DEPLOYER = Deployer(Manager.DEPLOYMENT_LOG_MANAGER)
