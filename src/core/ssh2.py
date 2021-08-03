from dataclasses import dataclass
from typing import List

from Exscript import Account, Host, PrivateKey
from Exscript.protocols import SSH2
from Exscript.util.start import start

from src.core import vault
from src.model.commands import Command


@dataclass
class SSHClient2:
    server: str
    username: str
    password: str = None
    port: int = None
    rsa_key: str = None
    dss_key: str = None

    def __connect__(self):
        assert None not in [self.server, self.username], "Mandatory details are not filled for connecting to server"
        host = Host("".join(["ssh://", self.server, ":", str(self.port or 22)]))
        if self.password:
            return Account(name=self.username, password=self.password), host
        elif self.rsa_key:
            return Account(name=self.username, key=PrivateKey.from_file(vault.get(self.rsa_key))), host
        elif self.dss_key:
            return Account(name=self.username, key=PrivateKey.from_file(filename=vault.get(self.dss_key), keytype="dss")), host

    def run_all(self, commands: List[Command]):
        def execute_commands(job, host, conn: SSH2):
            conn.autoinit()
            conn.set_timeout(3600)
            for command in commands:
                conn.execute("sudo " + command.command if command.privileged else command.command)
                conn.execute("echo $?")

        account, host = self.__connect__()
        host.set_account(account)
        start(account, host, execute_commands)

    def run(self, command: Command):
        def execute_commands(job, host, conn: SSH2):
            conn.execute("sudo " + command.command if command.privileged else command.command)
            conn.execute("echo $?")

        account, host = self.__connect__()
        host.set_account(account)
        try:
            start(account, host, execute_commands)
            return 1
        except:
            return 0
