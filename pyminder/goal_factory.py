from pyminder.beeminder import Beeminder
from natlibpy.factory import Factory
from pyminder.goal import Goal


class GoalFactory:
    _beeminder: Beeminder = None
    _factory: Factory = None

    def __init__(self, beeminder: Beeminder, factory: Factory):
        self._beeminder = beeminder
        self._factory = factory

    def get_goals(self):
        raw_goals = self._beeminder.get_goals()

        return [self._factory.secure(Goal, data=raw_goal) for raw_goal in raw_goals]