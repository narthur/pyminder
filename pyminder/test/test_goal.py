import unittest
from pyminder.test.test_case import TestCase
from pyminder.goal import Goal


class TestPyminder(TestCase):
    _pyminder = None
    _day = 24 * 60 * 60

    def _build_goal(self, data):
        return self._factory.secure(Goal, data=data)

    def test_exposes_attributes(self):
        goal = self._build_goal({"title": "My Goal"})

        self.assertEqual("My Goal", goal.title)

    def test_get_val(self):
        goal = self._build_goal({"fullroad": [
            [0, 1, 0],
            [self._day*7, 1, 0]
        ]})

        self.assertEqual(1, goal.get_road_val(0))

    def test_get_computed_val(self):
        rate = 1
        goal = self._build_goal({"fullroad": [
            [0, 0, rate],
            [self._day*7, rate*7, rate]
        ]})

        self.assertEqual(1, goal.get_road_val(self._day))

    def test_stage_rate_change(self):
        goal = self._build_goal({"fullroad": [
            [0, 0, 0],
            [self._day * 7, 0, 0]
        ]})

        goal.stage_rate_change(1, 0)

        self.assertEqual(1, goal.get_road_val(self._day))

    def test_stage_rate_change_with_start(self):
        goal = self._build_goal({"fullroad": [
            [0, 0, 0],
            [self._day * 7, 0, 0]
        ]})

        goal.stage_rate_change(1, self._day)

        self.assertEqual(0, goal.get_road_val(self._day))

    def test_bounded_rate_change(self):
        goal = self._build_goal({"fullroad": [
            [0, 0, 0],
            [self._day * 7, 0, 0]
        ]})

        goal.stage_rate_change(1, 0, self._day)

        self.assertEqual(2, goal.get_road_val(self._day*3))

    def test_get_road_val_with_progressively_future_times(self):
        pass

    def test_stage_rate_change_beyond_end_of_path(self):
        pass


if __name__ == '__main__':
    unittest.main()
