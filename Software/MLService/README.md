FAVEL ML Service
=

# Configuration

MLApproches tag in the configuration file favel.conf has three variable method, parameters, and normalizer. 

```
[MLApproches]
method = GradientBoostingClassifier
parameters = default
normalizer = default
```


## method
The machine learning (ML) algorithm has to be specified to the method. The algorithm name must be the sklearn module. 

```
method = GradientBoostingClassifier
```

## parameters
```default``` is used to run an experiment on the default ML algorithm parameters.

```
parameters = default
```

To set specified parameters of ML algorithm. The parameters should be passed in JSON format.
```
parameters = {'n_estimators': 100, 'learning_rate': 1.0, 'max_depth': 1, 'random_state': 0}
```

For optimization of ML Algorithm parameters. Parameters name with range is specified.
```
parameters = [
            {'name':'n_estimators',  'range':(1, 3)},
            {'name':'learning_rate', 'range':(1.0,2.0)},
            {'name': 'warm_start', 'range':[True, False]}
            ]
```

## normalizer
To normalize data used for ML. Any one of these normalizers should be specified in the config file.

```
normalizer = default
normalizer = Normalizer
normalizer = MinMaxScaler
normalizer = StandardScaler
normalizer = MaxAbsScaler
normalizer = RobustScaler
```

# Outputs 

* ``` Classification Report.xlsx ``` shows the performance of the ML model for each class. 
* ``` classifier.pkl ``` trained ml model dump in pickle format.
* ``` predicate_le.pkl ``` label encoding for predicates dump in pickle format.
