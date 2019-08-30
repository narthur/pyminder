import collections
import math


class Goal:
    _data = None
    _path = None

    def __init__(self, data: dict):
        self._data = data
        self._path = self._build_dense_path()

    def __getattr__(self, name):
        return self._get(name)

    def stage_rate_change(self, rate, start=None, end=None):
        end = end if end else next(reversed(self._path))

        self._extend_path(end)

        self._path = collections.OrderedDict({
            t: rate if start <= t <= end else r
            for t, r in self._path.items()
        })

    def _extend_path(self, end):
        day = 60 * 60 * 24
        end_time = next(reversed(self._path))
        end_rate = self._path[end_time]

        if end <= end_time:
            return

        pointer = end_time
        while pointer <= end:
            pointer += day
            self._path[pointer] = end_rate

    def get_road_val(self, time):
        val = self.fullroad[0][1]
        for _time, rate in self._path.items():
            if _time >= time:
                return val
            val += rate

        day = 60 * 60 * 24
        end_time = next(reversed(self._path))
        end_rate = self._path[end_time]
        time_left = time - end_time
        days_left = math.floor(time_left / day)

        return val + (days_left * end_rate) - 1

    def get_rate(self, time):
        tail = {t: r for t, r in self._path.items() if t >= time}

        if not tail:
            return None

        time_key = min(k for k, v in tail.items())

        return tail[time_key]

    def _build_dense_path(self, end_time=None):
        if not self.fullroad:
            return collections.OrderedDict()

        day_seconds = 60 * 60 * 24
        floor_time = self.fullroad[0][0]
        end_time = end_time if end_time else self.fullroad[-1][0]
        sparse_path = self._get_sparse_path()

        dense_path = {}
        time_pointer = end_time

        while time_pointer >= floor_time:
            if time_pointer in sparse_path:
                dense_path[time_pointer] = sparse_path[time_pointer]
            elif time_pointer + day_seconds in dense_path:
                dense_path[time_pointer] = dense_path[time_pointer + day_seconds]
            else:
                dense_path[time_pointer] = self.fullroad[-1][2]
            time_pointer -= day_seconds

        result = collections.OrderedDict(sorted(dense_path.items()))
        return result

    def _get_sparse_path(self):
        return {segment[0]: segment[2] for segment in self.fullroad}

    def _get(self, name):
        if name in self._data:
            return self._data[name]

        return None
