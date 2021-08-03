from src.dependency.manager import Manager

group_manager = Manager.GROUPED_DATA_MANAGER


def scale(group: str, app_name: str, deployment_id: str, scale: int):
    app_log = group_manager.get_app_log(group, app_name)
    command = f"docker stack services {app_log.app.name} - -format = '{{.Name}}={{.Replicas}}'"


def get_scale(group: str, app_name: str, scale: int):
    app_log = group_manager.get_app_log(group, app_name)
    app_log.deployments.get()