import unittest
from pyminder.test.test_case import TestCase
from pyminder.goal import Goal


class TestGoal(TestCase):
    _pyminder = None
    _day = 24 * 60 * 60

    def _build_goal(self, data=None, points=None):
        data = data if data else {}
        data['slug'] = data['slug'] if 'slug' in data else 'the_slug'
        points = points if points else []

        def side_effect(*args, **kwargs):
            return points.copy()

        self._mock_beeminder.get_datapoints.side_effect = side_effect
        self._mock_beeminder.get_goal.return_value = data

        return self._factory.secure(Goal, data=data)

    def test_exposes_attributes(self):
        goal = self._build_goal({"title": "My Goal"})

        self.assertEqual("My Goal", goal.title)

    def test_get_val(self):
        goal = self._build_goal({"fullroad": [
            [0, 1, 0],
            [self._day * 7, 1, 0]
        ]})

        self.assertEqual(1, goal.get_road_val(0))

    def test_get_computed_val(self):
        rate = 1
        goal = self._build_goal({"fullroad": [
            [0, 0, 0],
            [self._day * 7, rate * 7, rate]
        ]})

        self.assertEqual(1, goal.get_road_val(self._day))

    def test_stage_rate_change(self):
        goal = self._build_goal({"fullroad": [
            [0, 0, 0],
            [self._day * 7, 0, 0]
        ]})

        goal.stage_rate_change(1, self._day)

        self.assertEqual(1, goal.get_road_val(self._day))

    def test_stage_rate_change_with_start(self):
        goal = self._build_goal({"fullroad": [
            [0, 0, 0],
            [self._day * 7, 0, 0]
        ]})

        goal.stage_rate_change(1, self._day * 2)

        self.assertEqual(0, goal.get_road_val(self._day))

    def test_bounded_rate_change(self):
        goal = self._build_goal({"fullroad": [
            [0, 0, 0],
            [self._day * 7, 0, 0]
        ]})

        goal.stage_rate_change(1, 0, self._day)

        self.assertEqual(2, goal.get_road_val(self._day * 3))

    def test_get_road_val_beyond_road_end(self):
        goal = self._build_goal({"fullroad": [
            [0, 0, 0],
            [self._day, 1, 1]
        ]})

        self.assertEqual(2, goal.get_road_val(self._day * 2))

    def test_get_road_val_far_beyond_road_end(self):
        goal = self._build_goal({"fullroad": [
            [0, 0, 0],
            [self._day, 1, 1]
        ]})

        self.assertEqual(10, goal.get_road_val(self._day * 10))

    def test_stage_rate_change_beyond_end_of_path(self):
        goal = self._build_goal({"fullroad": [[0, 0, 0]]})

        goal.stage_rate_change(1, self._day * 5, self._day * 10)

        self.assertEqual(6, goal.get_road_val(self._day * 10))

    def test_get_val_offset(self):
        goal = self._build_goal({"fullroad": [
            [0, 1, 0],
            [self._day * 7, 1, 0]
        ]})

        self.assertEqual(1, goal.get_road_val(1))

    def test_get_computed_val_offset(self):
        rate = 1
        goal = self._build_goal({"fullroad": [
            [0, 0, 0],
            [self._day * 7, rate * 7, rate]
        ]})

        self.assertEqual(1, goal.get_road_val(self._day * 1.5))

    def test_get_user_val(self):
        goal = self._build_goal()

        self.assertEqual(0, goal.get_data_sum(0))

    def test_get_user_val_gets_data_points(self):
        goal = self._build_goal()

        goal.get_data_sum(0)

        self._mock_beeminder.get_datapoints.assert_any_call('the_slug')

    def test_get_user_val_with_data_point(self):
        goal = self._build_goal(points=[{
            "timestamp": 0,
            "value": 1.0,
        }])

        self.assertEqual(1, goal.get_data_sum(0))

    def test_get_needed(self):
        goal = self._build_goal()

        self.assertEqual(0, goal.get_needed(0))

    def test_get_needed_with_rate(self):
        rate = 1
        goal = self._build_goal({"fullroad": [
            [0, 0, 0],
            [self._day * 7, rate * 7, rate]
        ]})

        self.assertEqual(1, goal.get_needed(self._day))

    def test_get_needed_never_negative(self):
        goal = self._build_goal(points=[{
            "timestamp": 0,
            "value": 1.0,
        }])

        self.assertEqual(0, goal.get_needed(0))

    def test_stage_datapoint(self):
        goal = self._build_goal()

        goal.stage_datapoint(1, 0)

        self.assertEqual(1, goal.get_data_sum(0))

    def test_commit_datapoints(self):
        goal = self._build_goal()

        goal.stage_datapoint(1, 0)
        goal.commit_datapoints()

        self._mock_beeminder.create_datapoint.assert_any_call('the_slug', 1, 0)

    def test_only_commits_staged_datapoints(self):
        goal = self._build_goal(points=[{
            "timestamp": 0,
            "value": 1.0,
            "id": "the_id"
        }])

        goal.commit_datapoints()

        self._mock_beeminder.create_datapoint.assert_not_called()

    def test_get_staged_points(self):
        goal = self._build_goal()

        goal.stage_datapoint(1, 0)

        self.assertEqual(1, len(goal.get_staged_datapoints()))

    def test_refreshes_datapoints_on_commit(self):
        goal = self._build_goal()

        goal.stage_datapoint(1, 0)
        goal.commit_datapoints()

        self.assertEqual([], goal.get_staged_datapoints())

    def test_reset_datapoints(self):
        goal = self._build_goal()

        goal.stage_datapoint(1, 0)
        goal.reset_datapoints()

        self.assertEqual([], goal.get_staged_datapoints())

    def test_commit_road(self):
        rate = 1
        goal = self._build_goal({"fullroad": [
            [0, 0, 0],
            [self._day * 7, rate * 7, rate]
        ]})

        goal.commit_road()

        self._mock_beeminder.update_goal.assert_any_call('the_slug', roadall=[
            [0, 0, None],
            [self._day * 7, None, 1]
        ])

    def test_commit_modified_road(self):
        rate = 1
        goal = self._build_goal({"fullroad": [
            [0, 0, 0],
            [self._day * 7, rate * 7, rate]
        ]})

        goal.stage_rate_change(2, self._day * 3)
        goal.commit_road()

        self._mock_beeminder.update_goal.assert_any_call('the_slug', roadall=[
            [0, 0, None],
            [self._day * 2, None, 1],
            [self._day * 7, None, 2]
        ])

    def test_reset_road(self):
        rate = 1
        goal = self._build_goal({"fullroad": [
            [0, 0, 0],
            [self._day * 7, rate * 7, rate]
        ]})

        goal.stage_rate_change(2, self._day * 3)
        goal.reset_road()
        goal.commit_road()

        self._mock_beeminder.update_goal.assert_any_call('the_slug', roadall=[
            [0, 0, None],
            [self._day * 7, None, 1]
        ])

    def test_reset_road_gets_goal_data(self):
        goal = self._build_goal()

        goal.reset_road()

        self._mock_beeminder.get_goal.assert_any_call('the_slug')

    def test_get_needed_uses_lane_width(self):
        rate = 1
        goal = self._build_goal({
            "fullroad": [
                [0, 0, 0],
                [self._day * 7, rate * 7, rate]
            ],
            "lanewidth": 1
        })

        self.assertEqual(0, goal.get_needed(self._day))


if __name__ == '__main__':
    unittest.main()
