import pandas as pd
from os import path
from sklearn import metrics

class Overview:

    def __init__(self, df, experimentPath:str, datasetPath:str, approaches:list, mlAlgorithm:str, trainingMetrics):
        self.evaluation = self._getEvaluation(experimentPath)
        self.experiment = self._getExperiment(experimentPath)
        self.dataset = self._getDataset(datasetPath)
        self.trainingMetrics = trainingMetrics
        self.mlAlgorithm = mlAlgorithm
        
        self.bestApproach, self.bestApproachScore = self._getBestApproach(df, approaches)
        self.testingAucRoc = self._testingAucRoc(df)
        
    def write(self):
        # Read existing file, or create new data frame
        try:
            overviewFrame = pd.read_excel(path.join(self.evaluation, "Overview.xlsx"))
        except Exception as ex:
            overviewFrame = pd.DataFrame(columns=["Experiment", "Dataset", "Best Single Approach", "Best Single Score", "ML Algorithm", "Training AUC-ROC Score", "AUC-ROC Score"])
            
        # Create a new row for current experiment
        row = pd.Series([self.experiment, self.dataset, self.bestApproach, self.bestApproachScore, self.mlAlgorithm, self.trainingMetrics['overall'], self.testingAucRoc], index=overviewFrame.columns)
        
        # See if there already is a row for the current experiment and dataset
        exSet = set(overviewFrame.index[overviewFrame.Experiment == row.Experiment].tolist())
        dataSet = set(overviewFrame.index[overviewFrame.Dataset == row.Dataset].tolist())
        inter = exSet & dataSet
        if len(inter) > 0:
            # Update existing row
            for index in inter:
                overviewFrame.loc[index, ['AUC-ROC Score']] = self.testingAucRoc
        else:
            # Add new row
            overviewFrame = overviewFrame.append(row, ignore_index=True)

            
        overviewFrame.to_excel(path.join(self.evaluation, "Overview.xlsx"), index=False)
        
    def _testingAucRoc(self, df):
        y = df.truth
        ensembleScore = df.ensemble_score
        return metrics.roc_auc_score(y, ensembleScore)
        
    def _getBestApproach(self, df, approaches):
        y = df.truth
        bestApproach = None
        bestScore = 0
        for approach in approaches:
            approachScore = df[approach]
            auc_roc_single = metrics.roc_auc_score(y, approachScore)
            if auc_roc_single > bestScore:
                bestScore = auc_roc_single
                bestApproach = approach
        return bestApproach, bestScore
  
    def _getExperiment(self, experimentPath:str):
        pathLst = experimentPath.split('/')
        return pathLst[-1]
    
    def _getEvaluation(self, experimentPath:str):
        pathLst = experimentPath.split('/')
        pathStr = "/".join(pathLst[:-1])
        return pathStr
    
    def _getDataset(self, datasetPath:str):
        pathLst = datasetPath.split('/')
        return pathLst[-1]