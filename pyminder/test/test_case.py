import unittest
from unittest.mock import MagicMock
from natlibpy.factory import Factory
from pyminder.beeminder import Beeminder


class TestCase(unittest.TestCase):
    _factory = None

    _mock_beeminder = None

    def setUp(self) -> None:
        super().setUp()

        self._factory = Factory()

        self._mock_beeminder = self.__mock(Beeminder)

    def __mock(self, class_):
        mock = MagicMock(spec_set=class_)

        self._factory.inject(mock)

        return mock
