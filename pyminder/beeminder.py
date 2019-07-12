import requests


class Beeminder:
    _base_url = 'https://www.beeminder.com/api/v1/'
    _username = None
    _token = None

    # Auth

    def set_username(self, username):
        self._username = username

    def set_token(self, token):
        self._token = token

    # User

    def get_user(self, username=None):
        if username is None:
            username = self._username

        return self._call(f'users/{username}/goals.json')

    # Goal

    def get_goal(self):
        pass

    def get_goals(self):
        return self._call(f'users/{self._username}/goals.json')

    def create_goal(self):
        pass

    def update_goal(self):
        pass

    # Datapoint

    def get_datapoints(self):
        pass

    def create_datapoint(self):
        pass

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

        data.update({'auth_token': self._token})

        url = f'{self._base_url}{endpoint}'

        if method == 'GET':
            return requests.get(url, data).json()

        if method == 'POST':
            return requests.post(url, data).json()

        if method == 'PUT':
            return requests.put(url, data).json()

        return None
