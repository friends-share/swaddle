from dataclasses import dataclass
from typing import List

import paramiko

from src.model.commands import Command, CommandGroup
from src.model.server import Server


@dataclass
class SSHCmdState:
    out: List[str]
    err: List[str]
    status: int


@dataclass
class SSHClient:
    server: str
    username: str
    password: str = None
    port: int = None
    rsa_key: str = None
    dss_key: str = None

    def __connect__(self):
        assert None not in [self.server, self.username], "Mandatory details are not filled for connecting to server"
        ssh_configured = paramiko.SSHClient()
        if self.password:
            ssh_configured.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_configured.connect(self.server, username=self.username, port=self.port or 22, password=self.password)
            return ssh_configured
        elif self.rsa_key:
            k = paramiko.RSAKey.from_private_key_file(self.rsa_key)
            ssh_configured.connect(hostname=self.server, port=self.port or 22, username=self.username, pkey=k)
            return ssh_configured
        elif self.dss_key:
            k = paramiko.DSSKey.from_private_key_file(self.rsa_key)
            ssh_configured.connect(hostname=self.server, port=self.port or 22, username=self.username, pkey=k)
            ssh_configured.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            return ssh_configured

    def run(self, command: Command):
        password_required = False
        command_str = command.command
        if command.privileged and self.username != "root":
            command_str = f"sudo -S -p '' {command.command}"
            password_required = self.password is not None and len(self.password) > 0
        ssh_configured = self.__connect__()
        assert ssh_configured is not None, f'Failed to connect to server:{self.server}'
        stdin, stdout, stderr = ssh_configured.exec_command(command_str)
        if password_required:
            stdin.write(self.password + "\n")
            stdin.flush()
        return SSHCmdState(out=stdout.readlines(), err=stderr.readlines(), status=stdout.channel.recv_exit_status())

    def run_all(self, commands: List[Command]):
        return {cmd: self.run(cmd) for cmd in commands}

    def run_group(self, command_group: CommandGroup):
        return self.run_all(commands=command_group.commands)

    def run_groups_safe(self, commands: List[CommandGroup]):
        status = {}
        for cg in commands:
            status.update(self.run_all_safe(cg.commands) or {})

    def run_all_safe(self, commands: List[Command]):
        status = 0
        runs = {}
        for command in commands:
            if status == 0:
                run = self.run(command)
                status = run.status
                runs[command.command] = run.status
            else:
                return runs
        return runs


class SSH:

    @staticmethod
    def connect(server, username, password=None, port=None, rsa_key=None, dss_key=None) -> SSHClient:
        return SSHClient(server=server, username=username, password=password, port=port, rsa_key=rsa_key,
                         dss_key=dss_key)

    @staticmethod
    def connect_server(server: Server) -> SSHClient:
        if server.credential:
            if server.credential.secret_key:
                pass
            return SSHClient(server=server.ip_address, username=server.credential.name,
                             password=server.credential.password, port=server.ssh_port)
        return SSHClient(server=server.ip_address, port=server.ssh_port or 22)
