import requests
from models import Dashboard, Chart, Stream, Tag


class AppOpticsImporter:

    def __init__(self, token, dashboard_id):
        self.token = token
        self.dashboard_id = dashboard_id
        self.base_url = f'https://{self.token}:@api.appoptics.com/v1'

    def get_dashboard(self) -> Dashboard:
        response = self._get(
            f'/spaces/{self.dashboard_id}'
        )

        if response.status_code != 200:
            raise Exception(f'Failed to retrieve dashboard: {response.text}')

        dashboard_data = response.json()

        charts_response = self._get(f"/spaces/{self.dashboard_id}/charts")
        charts_data = charts_response.json()
        charts = [self._chart_from_response(chart) for chart in charts_data]

        return Dashboard(
            name=dashboard_data['name'],
            charts=charts,
            dashboard_id=self.dashboard_id,
        )

    def _get(self, path):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(self.base_url + path, headers=headers)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise Exception(f"Request failed with status {response.status_code}. Response: {response.text}") from e
        return response

    def _chart_from_response(self, response):
        name = response['name']
        type = response['type']
        chart_id = response['id']
        min = response.get('min', None)
        max = response.get('max', None)
        label = response.get('label', None)
        related_space = response.get('related_space', None)
        streams = [self._stream_from_response(stream) for stream in response['streams']]
        return Chart(
            name=name,
            type=type,
            streams=streams,
            chart_id=chart_id,
            min=min,
            max=max,
            label=label,
            related_space=related_space
        )

    def _stream_from_response(self, response):
        metric = response['metric']
        tags = [self._tag_from_response(tag) for tag in response['tags']]
        group_function = response.get('group_function', None)
        summary_function = response.get('summary_function', None)
        downsample_function = response.get('downsample_function', None)
        color = response.get('color', None)
        name = response.get('name', None)
        units_short = response.get('units_short', None)
        units_long = response.get('units_long', None)
        min = response.get('min', None)
        max = response.get('max', None)
        transform_function = response.get('transform_function', None)
        period = response.get('period', None)
        return Stream(
            metric=metric,
            tags=tags,
            group_function=group_function,
            summary_function=summary_function,
            downsample_function=downsample_function,
            color=color,
            name=name,
            units_short=units_short,
            units_long=units_long,
            min=min,
            max=max,
            transform_function=transform_function,
            period=period
        )

    def _tag_from_response(self, response):
        name = response['name']
        values = response.get('values', [])  # Returns an empty list if 'values' doesn't exist
        grouped = response.get('grouped', None)
        dynamic = response.get('dynamic', None)
        return Tag(name=name, values=values, grouped=grouped, dynamic=dynamic)
