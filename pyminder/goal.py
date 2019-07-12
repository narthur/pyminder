class Goal:
    _data = None

    def __init__(self, data: dict):
        self._data = data

    def __getattr__(self, name):
        return self._get_name(name)

    def _get_name(self, name):
        if name in self._data:
            return self._data[name]

        return None
