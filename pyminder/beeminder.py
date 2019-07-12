import requests


class Beeminder:
    _base_url = 'https://www.beeminder.com/api/v1/'
    _user = None
    _token = None

    def set_user(self, user):
        self._user = user

    def set_token(self, token):
        self._token = token

    def get_goals(self):
        endpoint = f'users/{self._user}/goals.json'

        return self._call(endpoint)

    def _call(self, endpoint, data=None, method='GET'):
        url = f'{self._base_url}{endpoint}'

        if method == 'GET':
            return requests.get(url, data).json()

        if method == 'POST':
            return requests.post(url, data).json()

        if method == 'PUT':
            return requests.put(url, data).json()

        return None
