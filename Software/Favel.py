from controller.Controller import Controller
from os import path
import configparser, logging, argparse

def main():
    # Parse arguments, load configuration
    args = _parseArguments()
    paths, configPath = _loadPaths(args)
    config = _loadConfig(configPath)
    _configureLogging(config)

    # Conduct a single experiment (-e flag)
    if not args.experiment is None:
        logging.info("Experiment started")
        controller = Controller(approaches=dict(config['Approaches']), mlAlgorithm=config['MLAlgorithm']['method'], mlParameters=config['MLAlgorithm']['parameters'],
                                normalizer_name=config['MLAlgorithm']['normalizer'], paths=paths, iterations=int(config['General']['iterations']),
                                writeToDisk=args.write, useCache=eval(config['General']['useCache']), handleContainers=args.containers)
        controller.input()
        controller.validate()
        controller.ensemble()
        controller.output()
        logging.info("Experiment finished")
        
    # Conduct experiments in batch mode (-b flag)
    elif not args.batch is None:
        subsetGen = powerset(list(dict(config['Approaches']).items()))
        numberOfExperiments = 2**len(list(dict(config['Approaches']).keys())) - (len(list(dict(config['Approaches']).keys())) + 1)
        i = 0
        for subset in subsetGen:
            if len(subset) >= 2:
                logging.info("Experiment started")
                sub = f"sub{str(i).rjust(4, '0')}"
                paths['SubExperimentPath'] = path.join(paths['ExperimentPath'], sub)
                paths['SubExperimentName'] = f"{paths['ExperimentName']}.{sub}"
                controller = Controller(approaches=dict(subset), mlAlgorithm=config['MLAlgorithm']['method'], mlParameters=config['MLAlgorithm']['parameters'],
                                        normalizer_name=config['MLAlgorithm']['normalizer'], paths=paths, iterations=int(config['General']['iterations']),
                                        writeToDisk=args.write, useCache=eval(config['General']['useCache']), handleContainers=args.containers)
                
                controller.input()
                controller.validate()
                controller.ensemble()
                controller.output()
                logging.info("Experiment finished")

                i += 1
                logging.info(f"Finished {i} out of {numberOfExperiments} experiments.")

def powerset(approaches:list):
    if len(approaches) <= 0:
        yield approaches
    else:
        for item in powerset(approaches[1:]):
            yield [approaches[0]] + item
            yield item
                
    

def _parseArguments(argv=None):
    argumentParser = argparse.ArgumentParser()

    argumentParser.add_argument("-d", "--data", required=True, help="Path to input data")
    argumentParser.add_argument("-w", "--write", action="store_true", help="Write all possible outputs to disk. This includes all models and all result data frames. Without this option only the overview file is written to disk.")
    argumentParser.add_argument("-c", "--containers", action="store_true", help="To Start/Stop containers, if not already running")

    group = argumentParser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--experiment", help="Name of the experiment to execute. The name must correspond to one directory in the Evaluation directory which contains a configuration file")
    group.add_argument("-b", "--batch", help="Name of the experiment to execute in batch mode. Batch mode executes an experiment for each set in the powerset of the approaches.")
    
    return argumentParser.parse_args(argv)
    
def _loadPaths(args):
    paths = dict()
    # Evaluation path
    favelPath = path.realpath(__file__)
    pathLst = favelPath.split('/')
    favelPath = "/".join(pathLst[:-2])
    paths['EvaluationPath'] = path.join(favelPath, "Evaluation")

    # Dataset path
    paths['DatasetPath'] = args.data

    # Dataset name
    pathLst = args.data.split('/')
    pathLst = list(filter(lambda x: x != '', pathLst))
    paths['DatasetName'] = pathLst[-1]

    # Experiment name e.g. eval005.BPDP_Dataset
    experiment = args.experiment if not args.experiment is None else args.batch
    paths['ExperimentName'] = f"{experiment}.{paths['DatasetName']}"

    # Experiment path e.g. .../Evaluation/eval005/BPDP_Dataset/
    paths['ExperimentPath'] = path.join(paths['EvaluationPath'], experiment, paths['DatasetName'])
    
    # Sub-Experiment path e.g. .../Evaluation/eval005/BPDP_Dataset/sub0042/
    paths['SubExperimentPath'] = paths['ExperimentPath']
    
    # Sub-Experiment name e.g. eval005.BPDP_Dataset.sub0042
    paths['SubExperimentName'] = paths['ExperimentName']

    return paths, path.join(paths['EvaluationPath'], experiment)
    
def _loadConfig(experimentPath:str):
    configPath = path.join(experimentPath, "favel.conf")
    if not path.exists(configPath):
        raise FileNotFoundError(f"Config file {configPath} does not exist")
    configParser = configparser.ConfigParser()
    configParser.read(configPath)
    return configParser

def _configureLogging(configParser):
    loggingOptions = dict()
    loggingOptions['debug'] = logging.DEBUG
    loggingOptions['info'] = logging.INFO
    loggingOptions['warning'] = logging.WARNING
    loggingOptions['error'] = logging.ERROR
    loggingOptions['critical'] = logging.CRITICAL
    
    logging.basicConfig(level=loggingOptions[configParser['General']['logging']])

if __name__ == '__main__':
    main()
