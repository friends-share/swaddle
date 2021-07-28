from src.core.ssh import SSH
from src.dependency.manager import Manager
from src.model.apps import App
from src.model.commands import Command
from src.model.server import Server, Cluster


class Swarmer:

    def __init__(self, cluster: Cluster):
        server = cluster.data.managers[0]
        self.main_manager = SSH.connect_server(server)
        self.other_managers = cluster.data.managers[1:]
        self.workers = cluster.data.workers
        self.logger = Manager.CLUSTER_LOG_MANAGER

    def init(self):
        worker_command = None
        manager_command = None
        init_run = self.main_manager.run(Command(command="docker swarm init", privileged=True))
        assert init_run.status == 0, f"Failed to initialise docker swarm: out={init_run.out}, err:{init_run.err}, " \
                                     f"status:{init_run.status} "
        join_token_worker = self.main_manager.run(Command(command="docker swarm join-token worker", privileged=True))
        if join_token_worker.status == 0:
            worker_command = Command(
                command=f'docker swarm {" ".join(join_token_worker.out).split("docker swarm")[1]}', privileged=True)
        else:
            return False
        join_token_manager = self.main_manager.run(Command(command="docker swarm join-token manager", privileged=True))
        if join_token_manager.status == 0:
            manager_command = Command(
                command=f'docker swarm {" ".join(join_token_manager.out).split("docker swarm")[1]}', privileged=True)
        else:
            return False
        for manager in self.other_managers:
            Swarmer._join_as_manager(manager, manager_command)

        for worker in self.workers:
            Swarmer._join_as_worker(worker, worker_command)
        return True

    @staticmethod
    def _join_as_worker(server: Server, worker_command_str):
        worker = SSH.connect_server(server)
        worker_command = worker.run(worker_command_str)
        assert worker_command.status == 0, f"Failed to initialise docker swarm worker: out={worker_command.out}, err:{worker_command.err}, status:{worker_command.status} "

    @staticmethod
    def _join_as_manager(server: Server, manager_command_str):
        worker = SSH.connect_server(server)
        command = worker.run(manager_command_str)
        assert command.status == 0, f"Failed to initialise docker swarm worker: out={command.out}, err:{command.err}, " \
                                    f" status:{command.status} "

    @staticmethod
    def scale(cluster: Cluster, app: App, scale: int) -> bool:
        manager = cluster.data.managers[0]
        return SSH.connect_server(manager).run(Command(f"docker service scale {app.name}={scale}", True)).status == 0
