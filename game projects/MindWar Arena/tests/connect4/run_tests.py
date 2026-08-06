import unittest

from tests.connect4.test_board import TestConnect4Board
from tests.connect4.test_rules import TestConnect4Rules
from tests.connect4.test_ai import TestConnect4AI
from tests.connect4.test_game import TestConnect4Game


def suite():
    test_suite = unittest.TestSuite()

    test_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(
            TestConnect4Board
        )
    )

    test_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(
            TestConnect4Rules
        )
    )

    test_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(
            TestConnect4AI
        )
    )

    test_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(
            TestConnect4Game
        )
    )

    return test_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(
        verbosity=2
    )

    runner.run(suite())