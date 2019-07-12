import unittest
from natlibpy.factory import Factory


class TestCase(unittest.TestCase):
    _factory = None

    def setUp(self) -> None:
        super().setUp()

        self._factory = Factory()
