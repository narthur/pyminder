from pyminder.beeminder import Beeminder
from pyminder.goal_factory import GoalFactory


class Pyminder:
    _beeminder: Beeminder = None
    _goal_factory: GoalFactory = None

    def __init__(self, beeminder: Beeminder, goal_factory: GoalFactory, user, token):
        self._beeminder = beeminder
        self._goal_factory = goal_factory

        self._beeminder.set_username(user)
        self._beeminder.set_token(token)

    def get_goals(self):
        return self._goal_factory.get_goals()
