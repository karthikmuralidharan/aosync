from typing import List, Optional
from dataclasses import dataclass, field, asdict

from aosync.api import AppOpticsAPI
from aosync.models import Dashboard


class AppOpticsSyncer:

    def __init__(self, api: AppOpticsAPI):
        self.api = api

    def sync(self, appoptics_dashboard: Dashboard) -> Dashboard:
        # If dynamic_tags is not None, add it to all charts
        if appoptics_dashboard.dynamic_tags:
            for chart in appoptics_dashboard.charts:
                for stream in chart.streams:
                    for dynamic_tag in appoptics_dashboard.dynamic_tags:
                        existing_tag = None
                        if stream.tags is None:
                            stream.tags = []
                        for tag in stream.tags:
                            if tag.name == dynamic_tag.name:
                                existing_tag = tag
                                break

                        if existing_tag:
                            # If a tag with the same name exists, update its values
                            existing_tag.values = dynamic_tag.values
                            existing_tag.dynamic = dynamic_tag.dynamic
                        else:
                            # If no such tag exists, add the dynamic tag
                            stream.tags.append(dynamic_tag)

        if appoptics_dashboard.id is not None:
            existing_dashboard = True
        else:
            existing_dashboard = False

        if existing_dashboard:
            self.api.update_dashboard(appoptics_dashboard.id, asdict(appoptics_dashboard))
        else:
            self.api.create_dashboard(asdict(appoptics_dashboard))

        for chart in appoptics_dashboard.charts:
            if chart.id is None:
                existing_chart = False
            else:
                existing_chart = True

            if existing_chart:
                self.api.update_chart(appoptics_dashboard.id, chart.id, asdict(chart))
            else:
                self.api.create_chart(appoptics_dashboard.id, asdict(chart))

        return appoptics_dashboard
