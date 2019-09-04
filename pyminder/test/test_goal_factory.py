import unittest
from pyminder.test.test_case import TestCase
from pyminder.goal_factory import GoalFactory


class TestPyminder(TestCase):
    _goal_factory = None

    def setUp(self) -> None:
        super().setUp()

        self._goal_factory = self._factory.secure(GoalFactory)

    def test_injects_data_into_goals(self):
        self._mock_beeminder.get_goals.return_value = [{"title": "My Goal"}]

        goals = self._goal_factory.get_goals()

        self.assertEqual("My Goal", goals[0].title)

    def test_makes_discrete_goals(self):
        self._mock_beeminder.get_goals.return_value = [
            {"title": "Goal 1"},
            {"title": "Goal 2"},
        ]

        goals = self._goal_factory.get_goals()

        self.assertNotEqual(goals[0].title, goals[1].title)


if __name__ == '__main__':
    unittest.main()
