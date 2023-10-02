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
        paths = [os.path.join(path,'Turtle/Test/Correct/'), 
                 os.path.join(path,'Turtle/Test/Wrong/'), 
                 os.path.join(path,'Turtle/Train/Correct/'), 
                 os.path.join(path,'Turtle/Train/Wrong/')]

        train_data = []
        test_data = []
        for p in paths:
            for root, dirs, files in os.walk(p):
                for name in files:
                    triple = self.extract_favel_triples(root+'/'+name)
                    if p.find("Correct") != -1:
                        triple=triple+(str(1),)
                    else:
                        triple=triple+(str(0),)
                    if p.find("Train") != -1:
                        train_data.append((triple[0], triple[1], triple[2], triple[3]))
                    else:
                        test_data.append((triple[0], triple[1], triple[2], triple[3]))

        return pd.DataFrame(data=train_data, columns=['subject','predicate','object','truth']), pd.DataFrame(data=test_data, columns=['subject','predicate','object','truth'])
        

    def extract_ids(self, graph):
        ids = []
        for s,_,_ in graph:
            ids.append(s)
        return list(set(ids))
    
    def getFactbench(self, path):
        graph_test = Graph()
        graph_train = Graph()
        
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.find("train")  != -1:
                    graph_train.parse(os.path.join(path, name), format="nt")
                else:
                    graph_test.parse(os.path.join(path, name), format="nt")
                
        ids_train = self.extract_ids(graph_train)
        ids_test = self.extract_ids(graph_test)
        
        data = []
        train_data = []
        test_data = []
        for id in ids_train:
            for _,p,o in graph_train.triples((id, None, None)):
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
            train_data.append((subject, predicate, object_elt, truth))
        for id in ids_test:
            for _,p,o in graph_test.triples((id, None, None)):
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
            test_data.append((subject, predicate, object_elt, truth))
        
        train = pd.DataFrame(data=train_data, columns=['subject','predicate','object','truth'])
        test = pd.DataFrame(data=test_data, columns=['subject','predicate','object','truth'])

        return train, test
    
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
        paths = [os.path.join(path,'Test/True/'), 
                 os.path.join(path,'Test/False/'), 
                 os.path.join(path,'Train/True/'), 
                 os.path.join(path,'Train/False/')]

        train_data = []
        test_data = []
        for p in paths:
            for root, dirs, files in os.walk(p):
                for name in files:
                    
                    triple = self.extract_bpdp_triples(p+name)
                    if p.find("True") != -1:
                        triple=triple+(str(1),)
                    else:
                        triple=triple+(str(0),)
                    if p.find("Train") != -1:
                        train_data.append((triple[0], triple[1], triple[2], triple[3]))
                    else:
                        test_data.append((triple[0], triple[1], triple[2], triple[3]))
                        
        return pd.DataFrame(data=train_data, columns=['subject','predicate','object','truth']), pd.DataFrame(data=test_data, columns=['subject','predicate','object','truth'])
    
    def getCsv(self, path):
        triples = pd.DataFrame(data=[], columns=['subject', 'predicate', 'object', 'truth'])
        inputData = pd.read_csv(path)
        return inputData
        
