import unittest

from sklearn.tree import DecisionTreeClassifier
from MLService.ML import ML
import pandas as pd
from datastructures.Assertion import Assertion



def createMockForTriples():
    approaches = {"Adamic_Adar": 4000, "Copaal": 3333}
    data = []
    for i in range(10):
        assertion = Assertion("<http://favel/Donald>", "<http://favel/born>", "<http://favel/Africa" + str(i) + ">")
        assertion.expectedScore = i % 2
        data.append(assertion)
    return data, approaches


class TestMLService(unittest.TestCase):

    def setUp(self):
        self.path = "./../Favel_Dataset/"
        self.ml = ML(self.path + "log.txt")

    def getFakeDataForML(self):
        data, approaches = createMockForTriples()
        return self.ml.createDataFrame(data)

    def testCreateDataFrame(self):
        self.assertIsInstance(self.getFakeDataForML(), pd.DataFrame)

    def testTrainModel(self):
        data = self.getFakeDataForML()
        # data["truth"] = [0, 1, 0]
        a = self.ml.train_model(data,
                                DecisionTreeClassifier(),
                                self.path, self.path)
        self.assertEqual(a, True)

    def testGetModelName(self):
        self.assertEqual(self.ml.get_model_name(DecisionTreeClassifier()), "DecisionTreeClassifier")

    def testCustomModelTrainCv(self):
        pass
        # This depends a lot on external libraries

    def testCustomModelTrain(self):
        pass
        # This depends a lot on external libraries

    def testValidateModel(self):
        df = self.getFakeDataForML()
        # df["truth"] = [0, 1, 0]
        output = self.ml.validate_model(df, self.path, "")
        self.assertIsInstance(output, pd.DataFrame)

    def testTestModel(self):
        df = self.getFakeDataForML()
        # df["truth"] = [0, 1, 0]
        output = self.ml.test_model(df, self.path)
        self.assertIsInstance(output, pd.DataFrame)
