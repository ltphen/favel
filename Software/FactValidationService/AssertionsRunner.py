import threading
import logging
from FactValidationService.AbstractJobRunner import AbstractJobRunner
from datastructures.Assertion import Assertion
from datastructures.exceptions.TrainingException import TrainingException
from datastructures.exceptions.TestingException import TestingException

class AssertionsRunner(AbstractJobRunner):
    """
    Subclass of AbstractJobRunner.
    Uses the functionality of AbstracJobRunner to validate lists of assertions.
    """

    def __init__(self, approach:str, port:int, trainingAssertions:list, testingAssertions:list):
        super().__init__(approach, port)
        self.trainingAssertions = trainingAssertions
        self.testingAssertions = testingAssertions
        self.errorCount = 0
        self.trainingComplete = False
        self.exception = None
    
    def run(self):
        try:
            # Validate train and test data
            self._test()
            
            # Close connection
            if self.server != None:
                self.server.close()
        except Exception as ex:
            self.exception = ex
            return

        size = len(self.trainingAssertions) + len(self.testingAssertions)
        if self.errorCount < size:
            logging.info("Validated {} out of {} assertions successfully using {}."
                         .format(size - self.errorCount, size, self.approach))
        
    def join(self):
        # Raise exception that occured in job thread in main thread.
        threading.Thread.join(self)
        if self.exception:
            raise self.exception
            
    def _validateAssertion(self, assertion:Assertion):
        """
        Overrides super method.
        If the approach is supervised, train before sending an assertion
        for validation.
        """
        if not self.trainingComplete and self.type == "supervised":
            self._train()
            self.trainingComplete = True
        
        return super()._validateAssertion(assertion)
    
    def _train(self):
        """
        Train a supervised approach.
        - Send call to begin training
        - Send training data
        - Send call to finish training
        """
        try:
            # Send start training call
            response = self._trainingStart()
            if response.type != "ack":
                raise TrainingException("TrainingException while calling {} to start training".format(self.approach))
            logging.info("Start training {}".format(self.approach))
            
            # Send training data
            for assertion in self.trainingAssertions:
                response = self._trainAssertion(assertion)
                if response.type != 'ack':
                    raise TrainingException("TrainingException while training {}".format(self.approach))
    
            # Send training complete call
            self._trainingComplete()
        except TrainingException as ex:
            logging.error("Something went wrong while training {}".format(self.approach))
            raise ex
            
        logging.info("Training of {} completed".format(self.approach))

    
    def _test(self):
        """
        Validate assertions in the self.trainingAssertions list
        and in the self.testingAssertions list using self.approach.
        """
        logging.info("Validating assertions using {}".format(self.approach))

        assertions = []
        assertions.extend(self.trainingAssertions)
        assertions.extend(self.testingAssertions)

        secondIterationsRequired = True
        # An approach might require the entire dataset to be uploaded before it can validate assertions.
        # In that case, upload the data in the first iteration, get the scores in the second iteration.
        while secondIterationsRequired:
            for assertion in assertions:
                response = self._validateAssertion(assertion)
    
                if response.type == "test_result":
                    secondIterationsRequired = False
                    assertion.score[self.approach] = float(response.score)
    
                elif response.type == "ack" and response.content == "test_ack":
                    # Second iteration is required, approach needs all assertions before it can start validating.
                    continue
                
                else:
                    assertion.score[self.approach] = 0
                    self.errorCount += 1
                    logging.error("'{}' while validating {} using {}."
                                  .format(response.content, assertion, self.approach))

            if secondIterationsRequired:
                response = self._testingUploadComplete()
                if not (response.type == "ack" and response.content == "test_upload_complete_ack"):
                    logging.error(f"Something went wrong while validating assertions using {self.approach}.")
                    raise TestingException(f"TestingException while validating assertions using {self.approach}.")
