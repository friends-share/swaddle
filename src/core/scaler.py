import json

from loguru import logger

from src.core.ssh import SSH
from src.dependency.manager import Manager
from src.model.commands import Command

group_manager = Manager.GROUPED_DATA_MANAGER


def _scale_cmd(service_name: str, scale: int):
    return f"docker service scale {service_name}={scale}"


def scale_app(group: str, app_name: str, scale: int):
    app_log = group_manager.get_app_log(group, app_name)
    find_service = "docker stack services " + app_name + " --format='{{.Name}}'"
    cluster_ids = list(app_log.deployments.keys())
    data = []
    for cluster_id in cluster_ids:
        cluster = group_manager.get_cluster(group, cluster_id)
        manager = cluster.data.managers[0]
        cmd_state = SSH.connect_server(manager).run(Command(command=find_service, privileged=manager.privileged))
        if cmd_state.out:
            scaling = []
            for service in cmd_state.out:
                scaled_service = service.replace("\n", "")
                logger.info("Found {} to scale", scaled_service)
                command = Command(command=_scale_cmd(scaled_service, scale), privileged=manager.privileged)
                logger.info("Executing command: {}", command)
                scale_cmd_state = SSH.connect_server(manager).run(command)
                logger.info("Scale response: {}", scale_cmd_state)
                scaling.append({"service": scaled_service, "status": scale_cmd_state.status})
            data.append({cluster_id: scaling})
        else:
            data.append({cluster_id: "No service found to scale"})
    return data


def get_scale(group: str, app_name: str):
    app_log = group_manager.get_app_log(group, app_name)
    command = "docker stack services " + app_name + " --format='{ {{json .Name}}: {{json .Replicas}}}'"
    cluster_ids = list(app_log.deployments.keys())
    data = []
    logger.info("Searching scale config for {}", cluster_ids)
    for cluster_id in cluster_ids:
        cluster = group_manager.get_cluster(group, cluster_id)
        manager = cluster.data.managers[0]
        cmd_state = SSH.connect_server(manager).run(Command(command=command, privileged=manager.privileged))
        cluster_data = []
        for service in cmd_state.out:
            out = service.replace("\n", "")
            cluster_data.append(json.loads(out))
        data.append({cluster_id: cluster_data})
    return data
