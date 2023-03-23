FAVEL
=
<i>Fact Validation Ensemble Learner</i>

The vision of this project is to explore the possibility to train a supervised machine learning algorithm based on the results of several fact validation approaches.

To achieve this vision this project offers:
* A software which can automatically
    1. Validate a dataset on multiple fact validation approaches
    2. Use the results of the fact validation approaches to train a supervised machine learning algorithm
    3. Validate the dataset on the trained machine learning model
* Two datasets that can be used for evaluation

# Structure of the Repository

- [**Analysis**](Analysis): Simple script to plot diagrams based on the data in [**Evaluation/Overview**](Evaluation/Overview.xlsx)
- [**Evaluation**](Evaluation): The software saves results to this directory
- [**Favel_Dataset**](Favel_Dataset): Dataset with simple example.  You can find the documentation [**here**](Favel_Dataset/README.md).
  
- [**FinalDataset_Hard**](FinalDataset_Hard) : Dataset with harder examples.  You can find the documentation [**here**](Favel_Dataset/README.md).
  
- [**Software**](Software): Software for exploring the vision
# Installation
```
git clone https://github.com/saschaTrippel/favel
cd favel/Software
```

# Usage
* To conduct an experiment with the software execute the following steps:
    1. Create a directory inside the Evaluation directory.\
        The name of the directory is the name of the experiment \
        Example: ```favel/Evaluation/experiment42```
    2. Create a configuration file ```favel.conf``` inside the experiment directory. \
        The configuration file defines the set of fact validation approaches and the machine learning algorithm. \
        A basic configuration file is can be found [**here**](Evaluation/example/favel.conf). \
        For more advaced configuration options look [**here**](Software/MLService/README.md). \
        Example: ```favel/Evaluation/experiment42/favel.conf```
    3. Execute the software. \
        For the software to be able to use fact validation approaches, these approaches might have to be started manually. \
        An exaustive description how to run the software can be found in the following section. \
        Results will be saved to the [**favel/Evaluation/**](Evaluation) directory. \
        Example: ```python3 favel/Software/Favel.py -d favel/FinalDataset_Hard -e experiment42```

## How to run

```
python3 Favel.py [options]
```

### Options
* ```-e EXPERIMENT, --experiment EXPERIMENT``` name of the experiment, corresponds with the name of the experiment folder in the ```Evaluation``` directory
* ```-b EXPERIMENT, --batch EXPERIMENT``` name of the experiment, corresponds with the name of the experiment folder in the ```Evaluation``` directory.
Experiment will be run in batch mode, meaning that an experiment will be executed with every subset of the specified set of fact validation approaches.
* ```-d DATA, --data DATA``` path to the dataset to validate
* ```-w, --write``` write everything to disk. If this flag is set, all possible outputs are written to disk. This includes models, normalizers, predicate encoders, and dataframes.
If the flag is not set, only the overview is written to disk.
* ```-c, --containers``` automatically Start/Stop containers which encapsulate the fact validation approaches

## How to test

```
python3 -m unittest
```

# Additional Resources

## Datasets
* [FactBench](https://github.com/saschaTrippel/FactBench-Dataset_2022)
* [BPDP](https://github.com/saschaTrippel/BPDP-Dataset_2022)
* [Favel](https://github.com/saschaTrippel/favel/tree/main/Favel_Dataset)
* [Favel-hard](https://github.com/saschaTrippel/favel/tree/main/FinalDataset_Hard)

## Fact Validation Approaches
* <https://github.com/saschaTrippel/knowledgestream> offers multiple algorithms
* <https://github.com/palaniappan1/COPAAL> offers COPAAL
