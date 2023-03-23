# FAVEL DATASET

FAVEL Dataset is created for the evaluation of fact validation algorithms. All facts are based on DBPedia release: dbpedia-snapshot-2022-03-release. This Dataset is entirely in english language.

FAVEL Dataset is a set of [RDF](https://www.w3.org/TR/rdf-primer/) Models. Each model contains a singular fact and its truth value. It consists of **train set**, **test set** and auxilliary files which are needed to create the models.

# Relations
FAVEL Dataset contains data of 10 relations. This data is directly extracted from Wikipedia(DBPedia).
| # | Property | Description | 
|--|--|--|
|1| Movie - Director | Person who is director of the movie |
|2| Movie - Producer | Person who is producer of the movie|
|3| Movie - Production Company | Company who is producing the movie |
|4| Movie - Starring | Person who is starring in the movie |
|5| Scientist - Academic Discipline | Academic Discipline/ Specialization to which a scientist belong |
|6| Scientist - Award | The awards which are received by the scientist|
|7| Scientist - KnownFor | The thing for which scientist is known for |
|8| University - Affiliation | The organization from which university is affiliated |
|9| University - Type | The type of university (eg. Public, Private) |
|10| University - City | The city in which university is located |

## Structure

FAVEL Dataset is structured in train set and test set of facts. Typically, the train set should be used to fit your algorithm and the test set to evaluate the algorithm.

# **Positive Data**
The positive data is collected from DBPedia. For each relation we queried DBPedia by issuing a SPARQL query and took top 50 results. We collected a total of 500 correct facts (150 in test set and 350 in train set). 

# **Negative Data**
The negative data is created by using the positive data that we have extracted earlier.
Assume a triple (s,p,o) in a knowledge base K.
1. We created triples (s',p,o) by random shuffling of s.
2. We created triples (s,p,o') by random shuffling of o.
3. We merged the triples as (s',p,o') to generate wrong triples.

We have also validated the negative triples by querying [DBPedia](https://dbpedia.org/sparql).
 
We have generated a total of 500 wrong facts (150 in test set and 350 in train set).

# **Train - Test Split**
The training and test sets are divided randomly in the ratio of 70:30 respectively for all relations.


