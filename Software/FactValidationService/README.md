# FactValidationService
The service is used to validate a list of facts on multiple fact validation algorithms.
The algorithms are executed in different processes, which are connected through a TCP interface.

## Interface
The interface differs for supervised and unsupervised approaches.

### Unsupervised

![Unsupervised communication](Interface_documentation/Unsupervised_Sequence-Diagram.png)

### Supervised
There are two options for communication with supervised approaches. Some need the entire test set before they can validate facts. This is accounted for in the second option.

![Supervised communication 1](Interface_documentation/Supervised_Sequence-Diagram.png)

![Supervised communication 2](Interface_documentation/Supervised-batch_Sequence-Diagram.png)

## Fact Validation Algorithms
Implementations that support this interface are:

* <https://github.com/saschaTrippel/knowledgestream> offers multiple algorithms
* <https://github.com/palaniappan1/COPAAL> offers COPAAL
