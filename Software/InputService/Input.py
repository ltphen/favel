from InputService.ReadFiles import ReadFiles
from datastructures.Assertion import Assertion
from datastructures.exceptions.InputException import InputException
import logging, copy

class Input:
    """
    Main class of InputService.
    Class that is called to read the input dataset.
    """

    cache = dict()
    
    def getInput(self, filePath:str):
        """
        Get the dataset located at 'filePath' divided into test and training data.
        If the dataset has been read before, it is cached in 'cache'.
        """
        if not filePath in Input.cache.keys():
            result = self._readInput(filePath)
            Input.cache[filePath] = result
        return copy.deepcopy(Input.cache[filePath])
            
    def _readInput(self, filePath:str):

        rf = ReadFiles()

        result = []
        if (filePath.endswith(".csv")):
            df = rf.getCsv(filePath)
            result = self.parseTriples(df)
            logging.info("Read {} assertions".format(len(result)))
            return result,result
        
        elif(str(filePath).lower().find("favel") != -1):
            df_train, df_test = rf.getFavel(filePath)
        elif(str(filePath).lower().find("factbench") != -1):
            df_train, df_test = rf.getFactbench(filePath)
        elif(str(filePath).lower().find("bpdp") != -1):
            df_train, df_test = rf.getBPDP(filePath)
        result_train = self.parseTriples(df_train)
        result_test = self.parseTriples(df_test)
        if len(result_train) == 0 or len(result_test) == 0:
            raise InputException("The specified dataset does not contain any assertions.")
        logging.info("Read {} training assertions, {} testing assertions".format(len(result_train),len(result_test)))
        return result_train, result_test
            
    def parseTriples(self, df):
        result = []
        for i, (s,p,o,t) in df.iterrows():
            a = Assertion(s,p,o)
            a._expectedScore = t
            result.append(a)
        return result
