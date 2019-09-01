import collections
from pyminder.beeminder import Beeminder


class Goal:
    _beeminder = None

    _data = None
    _sparse_path = None
    _dense_path = None
    _day = 60 * 60 * 24

    def __init__(self, beeminder: Beeminder, data: dict):
        self._beeminder = beeminder

        self._data = data
        self._sparse_path = self._build_sparse_path()
        self._dense_path = self._build_dense_path()

    def __getattr__(self, name):
        return self._get(name)

    def get_data_sum(self, time):
        return sum([p['value'] for p in self._get_datapoints() if p['timestamp'] <= time])

    def _get_datapoints(self):
        return self._beeminder.get_datapoints(self.slug)

    def stage_rate_change(self, rate, start=None, end=None):
        end = end if end else next(reversed(self._dense_path))

        self._extend_path(end)

        self._dense_path = collections.OrderedDict({
            t: rate if start <= t <= end else r
            for t, r in self._dense_path.items()
        })

    def get_road_val(self, time):
        self._extend_path(time)

        initial_val = self.fullroad[0][1]
        filtered_rates = [rate for _time, rate in self._dense_path.items() if _time <= time]

        return sum(filtered_rates) + initial_val

    def _extend_path(self, time):
        end_time = next(reversed(self._dense_path))
        end_rate = self._dense_path[end_time]

        ticks = list(range(end_time, round(time) + 1, self._day))
        for tick in ticks:
            self._dense_path[tick] = end_rate

    def get_rate(self, time):
        tail = {t: r for t, r in self._dense_path.items() if t >= time}

        if not tail:
            return None

        time_key = min(k for k, v in tail.items())

        return tail[time_key]

    def _build_dense_path(self):
        if not self.fullroad:
            return collections.OrderedDict()

        ticks = self._get_dense_path_ticks()
        path = {}
        for tick in reversed(ticks):
            path[tick] = self._get_day_rate(tick, path)

        return collections.OrderedDict(sorted(path.items()))

    def _get_dense_path_ticks(self):
        road_start = self.fullroad[0][0]
        road_end = self.fullroad[-1][0]

        return list(range(road_start, road_end + 1, self._day))

    def _get_day_rate(self, tick, dense_path):
        if tick in self._sparse_path:
            return self._sparse_path[tick]

        if tick + self._day in dense_path:
            return dense_path[tick + self._day]

        return self.fullroad[-1][2]

    def _build_sparse_path(self):
        if not self.fullroad:
            return {}

        return {segment[0]: segment[2] for segment in self.fullroad}

    def _get(self, name):
        if name in self._data:
            return self._data[name]

        return None
