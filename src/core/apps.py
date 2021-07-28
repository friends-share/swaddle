from src.core.service import AService, Id
from src.dependency import app_store, app_log_store
from src.model.apps import AppsRequest, App, AppLog


class AppService(AService[App, str]):

    def get_id(self, obj: App) -> Id:
        return obj.name

    def __init__(self, group_data_manager):
        super().__init__(app_store)
        self.group_data_manager = group_data_manager

    def add_new(self, apps_request: AppsRequest):
        errors = []
        for app in apps_request.apps:
            if self.exists(app.name):
                errors.append(f'{app.name} already exists')
            else:
                self.save_obj(app)
                self.group_data_manager.add_app(app)
        return errors

    def upsert(self, apps_request: AppsRequest):
        data = []
        for app in apps_request.apps:
            action = "added"
            if self.exists(app.name):
                action = "updated"
            self.save_obj(app)
            self.group_data_manager.add_app(app)
            data.append(f'{app.name} {action}')
        return data

    def get_by_names(self, *apps):
        return [self.get_by_id(app_name) for app_name in apps]


class AppLogManager(AService[AppLog, str]):

    def __init__(self):
        super().__init__(app_log_store)

    def get_id(self, obj: AppLog) -> Id:
        return obj.name
