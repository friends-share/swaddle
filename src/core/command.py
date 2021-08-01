from typing import List

from src.core.service import Id
from src.core.ssh import SSH
from src.model.commands import Command, CommandGroup
from src.model.message import Status, ProcessStatus
from src.model.server import Cluster
from src.storage.cache.store import CommandStore

DEFAULT_CMD = [
    CommandGroup(name="docker-setup", type="ubuntu", commands=[
        Command(command="apt-get update", privileged=False),
        Command(command="apt-get install apt-transport-https ca-certificates curl gnupg lsb-release -y",
                privileged=False),
        Command(command="curl -fsSL https://get.docker.com -o get-docker.sh"),
        Command(command="chmod +x get-docker.sh"),
        Command(command="sh get-docker.sh", privileged=False)
    ])
]


class CommandService:
    cmd_store = CommandStore()

    def get_id(self, obj: CommandGroup) -> Id:
        return CommandService.command_id(obj)

    @staticmethod
    def get_id_components(name, type):
        return "|".join([name, type])

    @staticmethod
    def command_id(obj: CommandGroup):
        return CommandService.get_id_components(obj.name, obj.type)

    @staticmethod
    def load_defaults():
        for cmd in DEFAULT_CMD:
            CommandService.cmd_store.put(CommandService.command_id(cmd), cmd)

    def save_obj(self, cmd: CommandGroup) -> ProcessStatus:
        if CommandService.cmd_store.exists(self.get_id(cmd)):
            return ProcessStatus(status=Status.FAILURE, errors=["Command already present with same name"])
        return ProcessStatus(status=Status.SUCCESS if CommandService.cmd_store.put(CommandService.command_id(cmd),
                                                                                   cmd) else Status.FAILURE)

    def get_by_id(self, command_id):
        return CommandService.cmd_store.get(command_id)

    def get_obj_components(self, name: str, type: str) -> CommandGroup:
        return CommandService.cmd_store.get(CommandService.get_id_components(name, type), None)

    def search(self, search_term: str) -> ProcessStatus:
        if search_term:
            return ProcessStatus(status=Status.SUCCESS, data=CommandService.cmd_store.get_all(search_term))
        return ProcessStatus(status=Status.SUCCESS, data=self.list_all(),
                             messages=["No command name given, Showing all commands"])

    def list_all(self):
        return CommandService.cmd_store.get_all()

    def process(self, cluster: Cluster, commands: List[CommandGroup]):
        servers = cluster.data.managers
        servers.extend(cluster.data.workers or [])
        status = []
        for server in servers:
            status.append(SSH.connect_server(server).run_all_safe(commands))
        return status
