import unittest
from OutputService.Output import Output
from OutputService.Output import GerbilFormat
from datastructures.Assertion import Assertion

import pandas as pd
import os


class TestOutputService(unittest.TestCase):

    def setUp(self):
        experiment = "./../Evaluation/example/"
        self.output = Output(experiment)
        self.gerbil = GerbilFormat(self.mockTestingData(), experiment)

    def testWriteOutput(self):
        df = self.createMockForOutputFile()
        self.output.writeOutput(df)
        self.assertTrue(os.path.exists("./../Evaluation/example/Output.csv"))
        os.remove("./../Evaluation/example/Output.csv")

    def mockTestingData(self):
        a = Assertion("Barack Obama", "born", "America")
        a._expectedScore = 1
        return [a]

    def testCreateTripleSubject(self):
        result = self.gerbil.createTripleSubject("<http://favel/>", "born")
        self.assertEqual(result, "<http://favel/> <http://www.w3.org/1999/02/22-rdf-syntax-ns#subject> <born>.\n")

    def testCreateTripleObject(self):
        result = self.gerbil.createTripleObject("<http://favel/>", "born")
        self.assertEqual(result, "<http://favel/> <http://www.w3.org/1999/02/22-rdf-syntax-ns#object> <born>.\n")

    def testCreateTriplePredicate(self):
        result = self.gerbil.createTriplePredicate("<http://favel/>", "born")
        self.assertEqual(result, "<http://favel/> <http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate> <born>.\n")

    def testCreateTripleType(self):
        result = self.gerbil.createTripleType("<http://favel/>")
        self.assertEqual(result, '<http://favel/> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement> .\n')
    def testCreateTruthValueTriple(self):
        result = self.gerbil.createTruthValueTriple("<http://favel/>", 1.0)
        self.assertEqual(result, '<http://favel/> <http://swc2017.aksw.org/hasTruthValue> "1.0"^^<http://www.w3.org/2001/XMLSchema#double> .\n')

    def testFormatDataset(self):
        self.gerbil.formatDataset()
        self.assertTrue(os.path.exists("./../Evaluation/example/favel.nt"))
        os.remove("./../Evaluation/example/favel.nt")

    def createMockForOutputFile(self):
        d = {'subject': ["<http://favel/Donald>", "<http://favel/Donald>"],
             'predicate': ["<http://favel/born>", "<http://favel/born>"],
             'object': ["<http://favel/Africa>", "<http://favel/America>"], 'ensemble_score': [0, 1]}
        return pd.DataFrame(data=d)

    def testCreateOutputFileForEvaluation(self):
        df = self.createMockForOutputFile()
        self.output.writeOutput(df)
        self.gerbil.createOutputFileForEvaluation()
        self.assertTrue(os.path.exists("./../Evaluation/example/favel_ensemble.nt"))
        os.remove("./../Evaluation/example/favel_ensemble.nt")
        os.remove("./../Evaluation/example/Output.csv")

