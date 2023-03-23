# FAVEL DATASET

FAVEL Dataset is created for the evaluation of fact validation algorithms. All facts are based on DBPedia release: dbpedia-snapshot-2022-03-release. This Dataset is entirely in english language.

FAVEL Dataset is a set of [RDF](https://www.w3.org/TR/rdf-primer/) Models. Each model contains a singular fact and its truth value. It consists of **train set**, **test set** and auxilliary files which are needed to create the models.

# Relations
FAVEL Dataset contains data of 11 relations. This data is directly extracted from Wikipedia(DBPedia).
| # | Property | Description | 
|--|--|--|
|1| Movie - Director | Person who is director of the movie |
|2| Movie - Producer | Person who is producer of the movie|
|3| Movie - Production Company | Company who is producing the movie |
|4| Movie - Starring | Person who is starring in the movie |
|5| Scientist - Academic Discipline | Academic Discipline/ Specialization to which a scientist belong |
|6| Scientist - Award | The awards which are received by the scientist|
|7| Scientist - Deathplace | The scientist's death place |
|8| Scientist - Birthplace | The scientist's birth place |
|9| University - Affiliation | The organization from which university is affiliated |
|10| University - Chancellor | The chancellor of the universtiy |
|11| University - City | The city in which university is located |

## Structure

FAVEL Dataset is structured in train set and test set of facts. Typically, the train set should be used to fit your algorithm and the test set to evaluate the algorithm.

# **Positive Data**
The positive data is collected from DBPedia. For each relation we queried DBPedia by issuing a SPARQL query and took top 50 results. We collected a total of 550 correct facts (165 in test set and 385 in train set). 

# **Negative Data**
The negative data is created by using the positive data that we have extracted earlier.

Assume a triple (s,p,o) in a knowledge base K. We have extracted triples (s,p',o') such that p and p' belong to same domain and have a close range.

**For example:** For the relation movie-director, p is dbo:director which is of domain dbo:Film and range dbo:Person. For creating negative examples, we extracted results with p' being dbo:Person, where (s,p,o) is not same as (s,p',o'). 

Correct: <http://dbpedia.org/resource/Dead_Snow> dbo:director <http://dbpedia.org/resource/Tommy_Wirkola>. --> (s,p,o)

Wrong: <http://dbpedia.org/resource/Dead_Snow> dbo:Person <http://dbpedia.org/resource/Ane_Dahl_Torp>. --> (s,p',o')

The negative examples are then stored as (s,p,o'), such that (s,p,o') does not exist.

**For example:**<http://dbpedia.org/resource/Dead_Snow> dbo:director <http://dbpedia.org/resource/Ane_Dahl_Torp>. --> (s,p,o')

We have generated a total of 550 wrong facts (165 in test set and 385 in train set).

# **Train - Test Split**
The training and test sets are divided randomly in the ratio of 70:30 respectively for all relations.


