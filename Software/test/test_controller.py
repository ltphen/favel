import unittest
from controller.Controller import Controller


class TestController(unittest.TestCase):

    def setUp(self):
        self.ctrl = Controller(["-e", "example", "-d", "./../Favel_Dataset"])

    def testLoadConfig(self):
        self.ctrl._loadConfig()
        self.assertIn("Approaches", self.ctrl.configParser, "Expect configuration file to contains Approaches")
        self.assertIn("MLApproches", self.ctrl.configParser)
        self.assertIn("General", self.ctrl.configParser)
        self.assertIn("logging", self.ctrl.configParser["General"])
        self.assertIn("cachePath", self.ctrl.configParser["General"])
        self.assertIn("useCache", self.ctrl.configParser["General"])

    # def testGetMethod(self):
    #     method = self.ctrl.getMethod()
    #     self.assertIn(method, ["train", "cache", "test"])

    def testInput(self):
        self.ctrl.input()
        self.assertGreaterEqual(len(self.ctrl.trainingData), 1)
        self.assertGreaterEqual(len(self.ctrl.testingData), 1)

    # TODO review this for because of containers load
    def testValidate(self):
        pass
        #self.ctrl.validate()
        # self.assertGreaterEqual(len(self.ctrl.testingData), 1)
