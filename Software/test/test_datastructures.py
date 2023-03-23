import unittest
from datastructures.Assertion import Assertion


class TestDataStructure(unittest.TestCase):

    def setUp(self):
        self.assertion = Assertion("Barack Obama", "born", "America")

    def testExpectedScoreRange(self):
        self.assertion.expectedScore = 1
        # Set an extreme value
        self.assertion.expectedScore = 10
        self.assertIn(self.assertion.expectedScore, [0,1])

    def testExpectedScore(self):
        self.assertion.expectedScore = 1
        self.assertEqual(self.assertion.expectedScore, 1)

    def testGetTurtle(self):
        self.assertEqual(self.assertion.getTurtle(), "<Barack Obama> <born> <America> .")

    def testCastingToString(self):
        self.assertEqual(str(self.assertion), "<Barack Obama> <born> <America> .")
