import requests
import os
import json


class Beeminder:
    _base_url = 'https://www.beeminder.com/api/v1/'
    _user = None
    _auth_token = None
    _access_token = None

    # Auth

    def set_username(self, username):
        self._user = username

    def set_auth_token(self, token):
        self._auth_token = token

    def set_access_token(self, token):
        self._access_token = token

    # User

    def get_user(self):
        return self._call(f'users/{self._user}.json')

    # Goal

    def get_goal(self, goal_name):
        return self._call(f'users/{self._user}/goals/{goal_name}.json')

    def get_goals(self):
        return self._call(f'users/{self._user}/goals.json')

    def create_goal(self):
        pass

    def update_goal(self, goal_name, slug=None, title=None, yaxis=None, secret=None,
                       datapublic=None, nomercy=None, roadall=None, datasource=None):
        args = {
            'slug': slug,
            'title': title,
            'yaxis': yaxis,
            'secret': secret,
            'datapublic': datapublic,
            'nomercy': nomercy,
            'roadall': roadall,
            'datasource': datasource
        }

        data = {k: v for k, v in args.items() if v is not None}

        return self._call(f'users/{self._user}/goals/{goal_name}.json',
                          data=data, method="PUT")

    # Datapoint

    def get_datapoints(self, goal_name):
        return self._call(f'/users/{self._user}/goals/{goal_name}/datapoints.json')

    def create_datapoint(
            self,
            goal_name: str,
            value: float,
            unix_timestamp: float = None,
            comment: str = None
    ):
        return self._call(f'/users/{self._user}/goals/{goal_name}/datapoints.json', data={
            'value': value,
            'unix_timestamp': unix_timestamp,
            'comment': comment
        }, method="POST")

    def create_datapoints(self):
        pass

    def update_datapoint(self):
        pass

    def delete_datapoint(self):
        pass

    # Charge

    def create_charge(self):
        pass

    # Internal

    def _call(self, endpoint, data=None, method='GET'):
        if data is None:
            data = {}

        if self._auth_token:
            data.update({'auth_token': self._auth_token})
        elif self._access_token:
            data.update({'access_token': self._access_token})

        url = f'{self._base_url}{endpoint}'
        result = None

        if method == 'GET':
            result = requests.get(url, data)

        if method == 'POST':
            result = requests.post(url, data)

        if method == 'PUT':
            result = requests.put(url, data)

        if not result.status_code == requests.codes.ok:
            raise Exception(f'API request failed with code {result.status_code}: {result.text}')

        # self._persist_result(endpoint, result)

        return None if result is None else result.json()

    @staticmethod
    def _persist_result(endpoint, result):
        path = f'data/{endpoint}'
        dir_ = os.path.dirname(path)
        if not os.path.exists(dir_):
            os.makedirs(dir_)
        with open(path, "w") as f:
            f.write(json.dumps(result.json()))
