from rdflib import Graph
import os
import pandas as pd
import re

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
        train_data = []
        test_data = []
        for root, dirs, files in os.walk(path):
            for name in files:
                # Open the input, unchanged and changed output files
                with open(os.path.join(path, name), "r") as f_in:
                    # Define a dictionary to hold the triple
                    triple = {}
                    statement_lines = []
                    # Iterate over each line in the file
                    for line in f_in:
                        # Add the line to the current statement lines
                        statement_lines.append(line)

                        # Find the parts of the triple
                        parts = re.findall(r"<(http://[^>]+)>", line)
                        if parts:
                            # Identify the parts of the triple based on their position in the quad
                            if "rdf-syntax-ns#subject" in parts[1]:
                                triple["subject"] = parts[2]
                            elif "rdf-syntax-ns#predicate" in parts[1]:
                                triple["predicate"] = parts[2]
                            elif "rdf-syntax-ns#object" in parts[1]:
                                triple["object"] = parts[2]

                        # If we have a complete triple
                        if len(triple) == 3 and len(statement_lines) == 5:
                            # URL encode the parts of the triple
                            subject = triple["subject"]
                            predicate = triple["predicate"]
                            object = triple["object"]
                            if(name.find("train") != -1):
                                train_data.append([subject, predicate, object, 0 if '"0.0"' in statement_lines[-1] else 1 ])
                            else:
                                test_data.append([subject, predicate, object, 0 if '"0.0"' in statement_lines[-1] else 1 ])
                        # Clear the triple and truth value line
                            triple.clear()
                            statement_lines.clear()
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
        inputData = pd.read_csv(path, index_col=0)
        return inputData
        
