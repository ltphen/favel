from rdflib import Graph
import os
import pandas as pd

class ReadFiles:
    """
    Class that reads the different datasets.
    """
    
    def extract_favel_triples(self, path):
        g = Graph()
        g.parse(path, format='ttl')
        for s, p, o in g.triples((None,  None, None)):
            return str(s), str(p), str(o)
        
    
    def getFavel(self, path):
        triples_test = pd.DataFrame(data=[], columns=['subject','predicate','object','truth'])
        triples_train = pd.DataFrame(data=[], columns=['subject','predicate','object','truth'])
        paths = [os.path.join(path,'Turtle/Test/Correct/'), 
                 os.path.join(path,'Turtle/Test/Wrong/'), 
                 os.path.join(path,'Turtle/Train/Correct/'), 
                 os.path.join(path,'Turtle/Train/Wrong/')]

        for p in paths:
            for root, dirs, files in os.walk(p):
                for name in files:
                    triple = self.extract_favel_triples(root+'/'+name)
                    if p.find("Correct") != -1:
                        triple=triple+(str(1),)
                    else:
                        triple=triple+(str(0),)
                    if p.find("Train") != -1:
                        triples_train = triples_train.append({'subject':triple[0], 'predicate':triple[1], 'object':triple[2], 'truth':triple[3]}, ignore_index=True)
                    else:
                        triples_test = triples_test.append({'subject':triple[0], 'predicate':triple[1], 'object':triple[2], 'truth':triple[3]}, ignore_index=True)

        return triples_train, triples_test
        

    def extract_ids(self, graph):
        ids = []
        for s,_,_ in graph:
            ids.append(s)
        return list(set(ids))
    
    def getFactbench(self, path):
        graph = Graph()
        
        for root, dirs, files in os.walk(path):
            for name in files:
                graph.parse(os.path.join(path, name), format="nt")
                
        ids = self.extract_ids(graph)
        
        triples = pd.DataFrame(data=[], columns=['subject','predicate','object','truth'])
        for id in ids:
            for _,p,o in graph.triples((id, None, None)):
                if str(p) == "http://swc2017.aksw.org/hasTruthValue":
                    if(str(o)=='1.0'):
                        truth = 1
                    else:
                        truth = 0
                if str(p).find("object") != -1:
                    object_elt=str(o)
                if str(p).find("predicate") != -1:
                    predicate=str(o)
                if str(p).find("subject") != -1:
                    subject=str(o)
            triples = triples.append({'subject':subject, 'predicate':predicate, 'object':object_elt, 'truth':truth}, ignore_index=True)

        return triples.iloc[:int(len(triples)*0.7)], triples.iloc[int(len(triples)*0.7):]
    
    def extract_bpdp_triples(self, file):
        subject = ""
        object_g = ""
        g = Graph()
        g.parse(file, format='ttl')
        if file.find("birth") != -1:
            predicate1 = "http://dbpedia.org/ontology/birth"
            predicate2 = "http://dbpedia.org/ontology/birthPlace"
        else:
            predicate1 = "http://dbpedia.org/ontology/death"
            predicate2 = "http://dbpedia.org/ontology/deathPlace"
        for s, p, o in g.triples((None,  None, None)):
            if str(p) == predicate1:
                subject=str(s)
            if str(p) == predicate2:
                object_g=str(o)
        return subject, predicate2, object_g

    def getBPDP(self, path):
        
        triples_train = pd.DataFrame(data=[], columns=['subject','predicate','object','truth'])
        triples_test = pd.DataFrame(data=[], columns=['subject','predicate','object','truth'])
        paths = [os.path.join(path,'Test/True/'), 
                 os.path.join(path,'Test/False/'), 
                 os.path.join(path,'Train/True/'), 
                 os.path.join(path,'Train/False/')]

        for p in paths:
            for root, dirs, files in os.walk(p):
                for name in files:
                    
                    triple = self.extract_bpdp_triples(p+name)
                    if p.find("True") != -1:
                        triple=triple+(str(1),)
                    else:
                        triple=triple+(str(0),)
                    if p.find("Train") != -1:
                        triples_train = triples_train.append({'subject':triple[0], 'predicate':triple[1], 'object':triple[2], 'truth':triple[3]}, ignore_index=True)
                    else:
                        triples_test = triples_test.append({'subject':triple[0], 'predicate':triple[1], 'object':triple[2], 'truth':triple[3]}, ignore_index=True)
                        
        return triples_train, triples_test
    
    def getCsv(self, path):
        triples = pd.DataFrame(data=[], columns=['subject', 'predicate', 'object', 'truth'])
        inputData = pd.read_csv(path)
        return inputData
        
