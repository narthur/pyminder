import unittest
from pyminder.test.test_case import TestCase
from pyminder.goal import Goal


class TestPyminder(TestCase):
    _pyminder = None

    def test_exposes_attributes(self):
        goal = self._factory.secure(Goal, data={"title": "My Goal"})

        self.assertEqual("My Goal", goal.title)


if __name__ == '__main__':
    unittest.main()
