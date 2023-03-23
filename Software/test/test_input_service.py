import unittest

import rdflib.term

from InputService.Input import Input
from InputService.ReadFiles import ReadFiles
from datastructures.Assertion import Assertion
import pandas as pd
from rdflib import Graph


class TestInputService(unittest.TestCase):

    def setUp(self):
        self.path = "./../Favel_Dataset/"
        self.input = Input()
        self.readFile = ReadFiles()

    def testGetInput(self):
        train, test = self.input.getInput(self.path)
        self.assertIsInstance(train[0], Assertion)
        self.assertIsInstance(test[0], Assertion)
        self.assertGreater(len(train), 1)
        self.assertGreater(len(test), 1)

    def createMockForTriples(self):
        d = {'subject': ["<http://favel/Donald>", "<http://favel/Donald>"],
             'predicate': ["<http://favel/born>", "<http://favel/born>"],
             'object': ["<http://favel/Africa>", "<http://favel/America>"], 'ensemble_score': [0, 1]}
        return pd.DataFrame(data=d)

    def testParseTriples(self):
        result = self.input.parseTriples(self.createMockForTriples())
        self.assertIsInstance(result[0], Assertion)
        self.assertEqual(result[0].expectedScore, 0)
        self.assertGreater(len(result), 1)

    def testExtractFavelTriples(self):
        return
        triple = self.readFile.extract_favel_triples(self.path+"Turtle/Test/Correct/Movie-Director/movie-director-0.ttl")
        self.assertEqual(triple[0], "http://dbpedia.org/resource/Legend_(2014_film)")
        self.assertEqual(triple[1], "http://dbpedia.org/property/director")
        self.assertEqual(triple[2], "http://dbpedia.org/resource/Boyapati_Srinu")

    def testGetFavel(self):
        train, test = self.readFile.getFavel(self.path)
        self.assertIsInstance(train, pd.DataFrame)
        self.assertGreater(len(train), 1)
        self.assertGreater(len(test), 1)

    def testExtractIds(self):
        return
        g = Graph()
        g.parse(self.path+"Turtle/Test/Correct/Movie-Director/movie-director-0.ttl", format='ttl')
        a = rdflib.term.URIRef("http://dbpedia.org/resource/Legend_(2014_film)")
        self.assertIn(a, self.readFile.extract_ids(g))

    def testGetFactbench(self):
        return
        # TODO Replace this with the path to the dataset
        triples = self.readFile.getFactbench("./../../Datasets/factbench")
        self.assertIsInstance(triples, tuple)
        self.assertGreater(len(triples), 1)

    def testExtractBpdpTriples(self):
        # TODO Replace this with the path to the dataset
        return
        subject, predicate, object_g = self.readFile.extract_bpdp_triples("./../../Datasets/bpdp/Test/False/birth_154.ttl")
        self.assertEqual(subject, "http://dbpedia.org/resource/Ambrose")
        self.assertEqual(predicate, "http://dbpedia.org/ontology/birthPlace")
        self.assertEqual(object_g, "http://dbpedia.org/resource/Milan")

    def testGetBPDP(self):
        # TODO check the parsing problem of the dataset
        return
        train, test = self.readFile.getBPDP("./../../Datasets/bpdp")
        self.assertIsInstance(train, pd.DataFrame)
        self.assertGreater(len(train), 1)
        self.assertGreater(len(test), 1)