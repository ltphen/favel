from os import path
from OutputService.GerbilFormat import GerbilFormat
from OutputService.Overview import Overview

class Output():
    """
    Main class of the OutputService.
    Responsible for writing the different output files.
    """

    def __init__(self, paths:dict):
        self.paths = paths

    def writeOutput(self, mlResults):
        """
        Writes results to file.
        """
        for i in range(len(mlResults)):
            df, auc_roc = mlResults[i]
            df.to_csv(path.join(self.paths['SubExperimentPath'], f"Output_it{i}.csv"), index=False)
        
    def writeOverview(self, testingResults, approaches:list, mlAlgorithm:str, mlParameters:str, trainingMetrics, normaliser_name:str):
        """
        Write Overview.xlsx
        """
        overview = Overview(testingResults, self.paths, approaches, mlAlgorithm, mlParameters, trainingMetrics, normaliser_name)
        overview.writeExcel()
    
    def gerbilFormat(self,testingData):
        """
        To convert testingData into GERBIL format.
        Also, converts output(ensemble_score) from Favel to GERBIL format for Evaluation purposes.
        """
        g = GerbilFormat(testingData, self.paths['SubExperimentPath'])
        g.getGerbilFormat()

