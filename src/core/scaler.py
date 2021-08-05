import json

from src.core.ssh import SSH
from src.dependency.manager import Manager
from src.model.commands import Command
from loguru import logger

group_manager = Manager.GROUPED_DATA_MANAGER


def scale(group: str, app_name: str, scale: int):
    app_log = group_manager.get_app_log(group, app_name)
    command = "docker stack services " + app_name + " --format = '{{.Name}}={{.Replicas}}'"
    cluster_ids = list(app_log.deployments.keys())
    data = []
    for cluster_id in cluster_ids:
        cluster = group_manager.get_cluster(group, cluster_id)
        manager = cluster.data.managers[0]
        out = ",".join(SSH.connect_server(manager).run(Command(command=command, privileged=manager.privileged)).out)
        print(out)
        data.append({cluster_id: out})
    return data


def get_scale(group: str, app_name: str):
    app_log = group_manager.get_app_log(group, app_name)
    command = "docker stack services " + app_name + " --format='{ {{json .Name}}: {{json .Mode}}}'"
    cluster_ids = list(app_log.deployments.keys())
    data = []
    logger.info("Searching scale config for {}", cluster_ids)
    for cluster_id in cluster_ids:
        cluster = group_manager.get_cluster(group, cluster_id)
        manager = cluster.data.managers[0]
        cmd_state = SSH.connect_server(manager).run(Command(command=command, privileged=manager.privileged))
        out = (",".join(cmd_state.out)).replace("\n", " ")
        data.append({cluster_id: json.loads(out)})
    return data
