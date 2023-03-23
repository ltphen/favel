from ContainerService.Containers import Containers
from FactValidationService.Validator import Validator
from InputService.Input import Input
from MLService.ML import ML
from OutputService.Output import Output
from pathlib import Path
import logging

class Controller:
    """
    Controler that interacts with the different services.
    Typical call order:
        - controller.input()
        - controller.validate()
        - controller.ensemble()
        - controller.output()
    """

    def __init__(self, approaches:dict, mlAlgorithm:str, mlParameters:str, normalizer_name:str, paths:dict, iterations:int, writeToDisk:bool, useCache:bool, handleContainers:bool):
        self.approaches = approaches
        self.mlAlgorithm = mlAlgorithm
        self.mlParameters = mlParameters
        self.normalizer_name = normalizer_name
        self.paths = paths
        self.iterations = iterations
        self.writeToDisk = writeToDisk
        self.useCache = useCache
        self.handleContainers = handleContainers
        self.testingData = None
        self.testingResults = []
        self.trainingData = None
        self.trainingMetrics = []

        self.createDirectories()
        
    def createDirectories(self):
        """
        If -w flag is set, create directories for output files.
        """
        if self.writeToDisk:
            experimentPath = Path(self.paths['ExperimentPath'])
            experimentPath.mkdir(parents=True, exist_ok=True)
            if not self.paths['SubExperimentPath'] is None:
                subExpPath = Path(self.paths['SubExperimentPath'])
                subExpPath.mkdir(parents=True, exist_ok=True)

    def _startContainers(self):
        """
        If -c flag is set, start the containers that hold the fact validation approaches.
        """
        if self.handleContainers:
            logging.info("Starting Containers")
            c = Containers()
            c.startContainers() 
            c.status()
    
    def _stopContainers(self):
        """
        If -c flag is set, stop the containers that hold the fact validation approaches.
        """
        if self.handleContainers:
            logging.info("Stopping Containers")
            c = Containers()
            c.rmContainers()
        
    def input(self):
        """
        Read the input dataset that is specified in the '-d' argument.
        The assertions are held in self.trainingData and self.testingData.
        """
        input = Input()
        self.trainingData, self.testingData = input.getInput(self.paths['DatasetPath'])

    def validate(self):
        """
        Validate the assertions in self.trainingData and self.testingData
        on the fact validation approaches specified in self.approaches.
        """
        self._startContainers()
        
        validator = Validator(self.approaches, self.useCache)
        validator.validate(self.trainingData, self.testingData)

        self._stopContainers()
        
    def ensemble(self):
        """
        Repeat training and testing as often as specified in the configuration.
        """
        for i in range(self.iterations):
            self.train()
            self.test()
    
    def train(self):
        """
        Train the ML model.
        Has to be called before self.test()
        """
        self.ml = ML(self.writeToDisk)
        training_df = self.ml.createDataFrame(self.trainingData)

        ml_model_name = self.mlAlgorithm
        ml_model = self.ml.get_sklearn_model(ml_model_name, self.mlParameters, training_df)

        self.model, self.lableEncoder, self.normalizer, trainMetrics = self.ml.train_model(df=training_df, 
                                            ml_model=ml_model, 
                                            normalizer_name=self.normalizer_name,
                                            output_path=self.paths['SubExperimentPath'])
        self.trainingMetrics.append(trainMetrics)

    def test(self):
        """
        Test the ML model created in the previous call of self.train().
        Has to be called after self.train()
        """
        testing_df = self.ml.createDataFrame(self.testingData)

        testing_result = self.ml.test_model(df=testing_df, ml_model=self.model, le_predicate=self.lableEncoder,
                                                normalizer=self.normalizer)

        self.testingResults.append(testing_result)
    

    def output(self):
        """
        Write the results to disk.
        """
        op = Output(self.paths)
        op.writeOverview(self.testingResults, self.approaches.keys(), self.mlAlgorithm, self.mlParameters, self.trainingMetrics, self.normalizer_name)
        if self.writeToDisk:
            op.writeOutput(self.testingResults)
            #op.gerbilFormat(self.testingData)
