from Exscript import Account, Host
from Exscript.util.start import quickstart, start


def do_something(job, host, conn):
    conn.execute('mkdir re')
    conn.execute('cd re')
    conn.execute('mkdir re1')


account = Account("root", "Passw0rd")
host = Host("ssh://172.17.0.3")
host.set_account(account)


start(account, host, do_something)
