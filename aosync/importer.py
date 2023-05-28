from aosync.api import AppOpticsAPI
from aosync.parser import map_to_dashboard
from aosync.models import Dashboard


class AppOpticsImporter:

    def __init__(self, api: AppOpticsAPI):
        self.api = api

    def import_dashboard(self, dashboard_id) -> Dashboard:
        dashboard_data = self.api.get_dashboard(
            dashboard_id
        )

        charts_data = self.api.get_all_charts(
            dashboard_id
        )
        dashboard_data['id'] = dashboard_id

        return map_to_dashboard(
            charts_data,
            dashboard_data
        )
