import requests
import json


class AppOpticsAPI:

    def __init__(self, token):
        self.token = token
        self.base_url = f'https://{self.token}:@api.appoptics.com/v1'

    def get_dashboard(self, dashboard_id):
        return self._get(
            f'/spaces/{dashboard_id}'
        ).json()

    def create_dashboard(self, dashboard):
        path = f"/spaces"
        return self._post(path, dashboard).json()

    def update_dashboard(self, dashboard_id, dashboard):
        path = f"/spaces/{dashboard_id}"
        return self._put(path, dashboard).json()

    def delete_dashboard(self, dashboard_id):
        path = f"/spaces/{dashboard_id}"
        return self._delete(path)

    def create_chart(self, dashboard_id, chart):
        path = f"/spaces/{dashboard_id}/charts"
        return self._post(path, chart).json()

    def get_all_charts(self, dashboard_id):
        return self._get(f"/spaces/{dashboard_id}/charts").json()

    def update_chart(self, dashboard_id, chart_id, chart):
        path = f"/spaces/{dashboard_id}/charts/{chart_id}"
        return self._put(path, chart).json()

    def delete_chart(self, dashboard_id, chart_id):
        path = f"/spaces/{dashboard_id}/charts/{chart_id}"
        return self._delete(path)

    def _get(self, path):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(self.base_url + path, headers=headers)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise Exception(f"Request failed with status {response.status_code}. Response: {response.text}") from e
        return response

    def _post(self, path, payload):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        response = requests.post(self.base_url + path, headers=headers, data=json.dumps(payload))
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise Exception(f"Request failed with status {response.status_code}. Response: {response.text}") from e
        return response

    def _put(self, path, payload):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        response = requests.put(self.base_url + path, headers=headers, data=json.dumps(payload))
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise Exception(f"Request failed with status {response.status_code}. Response: {response.text}") from e
        return response
