import unittest
from pyminder.test.test_case import TestCase
from pyminder.pyminder import Pyminder
from pyminder.goal import Goal


class TestPyminder(TestCase):
    _pyminder = None

    def setUp(self) -> None:
        super().setUp()

        self._pyminder = self._factory.secure(Pyminder, user="username", token="token")

    def test_get_goals(self):
        self._pyminder.get_goals()

        self._mock_beeminder.get_goals.assert_called()

    def test_sets_user(self):
        self._mock_beeminder.set_username.assert_called_with("username")

    def test_sets_token(self):
        self._mock_beeminder.set_token.assert_called_with("token")

    def test_get_goals_returns_goals(self):
        self._mock_beeminder.get_goals.return_value = [{}]

        goals = self._pyminder.get_goals()

        self.assertIsInstance(goals[0], Goal)


if __name__ == '__main__':
    unittest.main()
