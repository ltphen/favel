from InputService.Input import Input
from FactValidationService.Cache import Cache
import pandas as pd
import os

def main():
    # Set parameters
    approaches = ("adamic_adar","degree_product","jaccard","katz","kl","kl_rel","pathent","predpath","simrank")
    dataset = "factbench" # "bpdp" #"favel"
    datasetPath = "../datasets/FactBench-Dataset_2022/factbench-clean" #"../datasets/BPDP-Dataset_2022/BPDP_Dataset" #"../FinalDataset_Hard"
    outPath = "../exported/" + dataset + "/"
    
    if not os.path.exists(outPath):
        os.makedirs(outPath)
    
    # Read dataset
    reader = Input()
    trainingData, testingData = reader.getInput(datasetPath)
    
    # Read cached data from DB
    cache = Cache("../Evaluation/Cache-DB.sqlite","")
    
    for approach in approaches:
        cache.approach = approach
        exportData(cache, trainingData, outPath + approach + "_train.csv")
        exportData(cache, testingData, outPath + approach + "_test.csv")

    
def exportData(cache, data, outputFile):
    resultData = []
    for assertion in data:
        resultData.append((assertion.subject, assertion.predicate, assertion.object, cache.getScore(assertion.subject, assertion.predicate, assertion.object)))
    
    pd.DataFrame(data=resultData, columns=['subject','predicate','object','truth']).to_csv(outputFile, index=False)

if __name__ == '__main__':
    main()
    
