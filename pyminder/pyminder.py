from pyminder.beeminder import Beeminder
from pyminder.goal_factory import GoalFactory
from natlibpy.factory import Factory


class Pyminder:
    _beeminder: Beeminder = None
    _goal_factory: GoalFactory = None

    def __init__(self, user, token, beeminder: Beeminder = None, goal_factory: GoalFactory = None):
        factory = Factory()

        self._beeminder = beeminder if beeminder else factory.secure(Beeminder)
        self._goal_factory = goal_factory if goal_factory else factory.secure(GoalFactory)

        self._beeminder.set_username(user)
        self._beeminder.set_auth_token(token)

    def get_goals(self):
        return self._goal_factory.get_goals()

    def get_goal(self, slug):
        return self._goal_factory.get_goal(slug)
