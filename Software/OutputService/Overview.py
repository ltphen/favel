from os import path
from sklearn import metrics
import logging
import pandas as pd
import statistics

class Overview:
    """
    Write or update favel/Evaluation/Overview.xlsx.
    The overview file has primaryKey attributes and dependentProperties.
    A certain configuration of primaryKey attributes can only exist once in the overview.
    If an existing configuration of primaryKey attributes appears a second time, the dependentProperties of the first
    appearance are updated.
    """

    def __init__(self, testingResults:list, paths:dict, approaches:list, mlAlgorithm:str, mlParameters:str, trainingMetrics, normalizer_name):
        self.evaluation = paths['EvaluationPath']

        self.primaryKey = ["Dataset", "ML Algorithm", "ML Parameters", "Normalizer", "Iterations", "Fact Validation Approaches"]
        self.dependentProperties = ["Approaches Scores", "#Approaches", "Best Single Approach", "Best Single Score", "Experiment",
                                    "Training AUC-ROC Min.", "Training AUC-ROC Max.", "Training AUC-ROC Mean", "Training AUC-ROC Std. Dev.",
                                    "Testing AUC-ROC Min.", "Testing AUC-ROC Max.", "Testing AUC-ROC Mean", "Testing AUC-ROC Std. Dev.", "Improvement"]
        
        # Set the key attributes
        self.keyData = dict()
        self.keyData["Dataset"] = paths["DatasetName"]
        approachesLst = list(approaches)
        approachesLst.sort()
        self.keyData["Fact Validation Approaches"] = ", ".join(approachesLst)
        self.keyData["ML Algorithm"] = mlAlgorithm
        self.keyData["ML Parameters"] = mlParameters
        self.keyData["Iterations"] = len(testingResults)
        self.keyData["Normalizer"] = normalizer_name
        
        # Set the dependent attributes
        self.dependentData = dict()
        self.dependentData["Experiment"] = paths["SubExperimentName"]
        self.dependentData["Testing AUC-ROC Min."], self.dependentData["Testing AUC-ROC Max."], self.dependentData["Testing AUC-ROC Mean"], self.dependentData["Testing AUC-ROC Std. Dev."] = self._testingStatistics(testingResults)
        self.dependentData["Training AUC-ROC Min."], self.dependentData["Training AUC-ROC Max."], self.dependentData["Training AUC-ROC Mean"], self.dependentData["Training AUC-ROC Std. Dev."] = self._trainingStatistics(trainingMetrics)
        self.dependentData["Approaches Scores"], self.dependentData["Best Single Approach"], self.dependentData["Best Single Score"] = self._getBestApproach(testingResults[0][0], approaches)
        self.dependentData["#Approaches"] = len(approaches)
        self.dependentData["Improvement"] = self.dependentData["Testing AUC-ROC Mean"] - self.dependentData["Best Single Score"]
        
        for key in self.primaryKey:
            assert(key in self.keyData.keys())
                
        for key in self.dependentProperties:
            assert(key in self.dependentData.keys())
        
    def writeExcel(self):
        """
        Read an existing overview file, or create new data frame.
        """
        try:
            overviewFrame = pd.read_excel(path.join(self.evaluation, "Overview.xlsx"))
        except Exception as ex:
            col = []
            col.extend(self.primaryKey)
            col.extend(self.dependentProperties)
            overviewFrame = pd.DataFrame(columns=col)
            
        
        # See if there already is a row for the current experiment and dataset
        intersection = self.findRow(overviewFrame)
        if len(intersection) > 0:
            # Update existing row
            self.update(overviewFrame, intersection)
            logging.debug(f"Updated row in evaluation overview")

        else:
            # Add new row
            data = [self.keyData[key] for key in self.primaryKey]
            data.extend([self.dependentData[key] for key in self.dependentProperties])
            row = pd.Series(data, index=overviewFrame.columns)

            overviewFrame = overviewFrame.append(row, ignore_index=True)
            logging.debug(f"Added row to evaluation overview \n{row}")

            
        overviewFrame.to_excel(path.join(self.evaluation, "Overview.xlsx"), index=False)
        
    def findRow(self, frame):
        """
        Find a row that has the same primaryKey attributes as self.
        """
        result = dict()
        for key in self.primaryKey:
            result[key] = set(frame.index[frame[key] == self.keyData[key]].tolist())

        intersect = None
        for key in self.primaryKey:
            if intersect is None:
                intersect = result[key]
            else:
                intersect &= result[key]
        return intersect

    def update(self, frame, intersection):
        """
        Update the dependentProperties of an existing row.
        """
        for index in intersection:
            for key in self.dependentProperties:
                frame.loc[index, [key]] = self.dependentData[key]
        
    def _trainingStatistics(self, trainingMetrics):
        """
        Calculate statistics on training results.
        """
        return self._statistics(list(map(lambda x: x['overall'], trainingMetrics)))
    
    def _testingStatistics(self, testingResults):
        """
        Calculate statistics on testing results.
        """
        tmp = []
        for df, auc_roc in testingResults:
            tmp.append(auc_roc)
        return self._statistics(tmp)
    
    def _statistics(self, values:list):
        """
        Returns min, max, mean, stdev
        """
        if len(values) == 1:
            return values[0], values[0], values[0], 0
        return min(values), max(values), statistics.mean(values), statistics.stdev(values)
        
    def _getBestApproach(self, df, approaches):
        """
        Find the best single approach used in self.
        """
        y = df.truth
        results = dict()
        bestApproach = None
        bestScore = 0
        for approach in approaches:
            approachScore = df[approach]
            auc_roc_single = metrics.roc_auc_score(y, approachScore)
            results[approach] = auc_roc_single
            if auc_roc_single > bestScore:
                bestScore = auc_roc_single
                bestApproach = approach
        return str(results), bestApproach, bestScore
