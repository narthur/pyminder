import collections
from pyminder.beeminder import Beeminder


class Goal:
    _beeminder = None

    _data = None
    _datapoints = None
    _sparse_path = None
    _dense_path = None
    _day = 60 * 60 * 24

    def __init__(self, beeminder: Beeminder, data: dict):
        self._beeminder = beeminder

        self._load_goal_data(data)
        self.reset_datapoints()

    def __getattr__(self, name):
        return self._get(name)

    def _load_goal_data(self, data: dict):
        self._data = data
        self._sparse_path = self._build_sparse_path()
        self._dense_path = self._build_dense_path()

    def stage_datapoint(self, value, time):
        self._datapoints.append({
            "timestamp": time,
            "value": value
        })

    def commit_datapoints(self):
        for point in self.get_staged_datapoints():
            self._beeminder.create_datapoint(self.slug, point['value'], point['timestamp'])

        self.reset_datapoints()

    def commit_road(self):
        self._beeminder.update_goal(self.slug, roadall=self._build_roadall())

    def _build_roadall(self):
        dense_keys_sorted = sorted(self._dense_path)
        road_reversed = []
        last_key = dense_keys_sorted[-1]
        road_reversed.append([last_key, None, self._dense_path[last_key]])

        for the_time in reversed(dense_keys_sorted):
            if self._dense_path[the_time] is not road_reversed[-1][2]:
                road_reversed.append([the_time, None, self._dense_path[the_time]])

        road = list(reversed(road_reversed))
        road[0] = [self.fullroad[0][0], self.fullroad[0][1], None]

        return road

    def reset_datapoints(self):
        self._datapoints = self._beeminder.get_datapoints(self.slug)

    def reset_road(self):
        data = self._beeminder.get_goal(self.slug)

        self._load_goal_data(data)

    def get_staged_datapoints(self):
        return [p for p in self._datapoints if 'id' not in p]

    def get_needed(self, time):
        return max(self.get_road_val(time) - self.get_data_sum(time), 0)

    def get_data_sum(self, time):
        return sum([p['value'] for p in self._datapoints if p['timestamp'] <= time])

    def stage_rate_change(self, rate, start=None, end=None):
        end = end if end else next(reversed(self._dense_path))

        self._extend_path(end)

        self._dense_path = collections.OrderedDict({
            t: rate if start <= t <= end else r
            for t, r in self._dense_path.items()
        })

    def get_road_val(self, time):
        if not self.fullroad:
            return 0

        self._extend_path(time)

        initial_val = self.fullroad[0][1]
        filtered_rates = [rate for _time, rate in self._dense_path.items() if _time <= time]

        return sum(filtered_rates) + initial_val

    def _extend_path(self, time):
        if not self._dense_path:
            return

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
