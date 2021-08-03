from src.core.ssh import SSH
from src.dependency.manager import Manager
from src.model.commands import Command

group_manager = Manager.GROUPED_DATA_MANAGER


def scale(group: str, app_name: str, deployment_id: str, scale: int):
    app_log = group_manager.get_app_log(group, app_name)
    command = f"docker stack services {app_log.app.name} - -format = '{{.Name}}={{.Replicas}}'"


def get_scale(group: str, app_name: str):
    app_log = group_manager.get_app_log(group, app_name)
    command = f"docker stack services {app_name} - -format = '{{.Name}}={{.Replicas}}'"
    cluster_ids = list(app_log.deployments.keys())
    data = []
    for cluster_id in cluster_ids:
        cluster = group_manager.get_cluster(group, cluster_id)
        manager = cluster.data.managers[0]
        out = ",".join(SSH.connect_server(manager).run(Command(command=command, privileged=manager.privileged)).out)
        data.append({cluster_id: out})
    return data
