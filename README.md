# Dutch verb matrices
Code used to train verb matrices for use in compositional distributional semantics, created for my thesis in BA Linguistics.

The verb matrices are trained to use the embeddings created by Tulkens, Emmery & Daelemans (2016) as noun vectors.
https://github.com/clips/dutchembeddings

Training data was assembled from the Lassy Groot corpus.
http://www.let.rug.nl/~vannoord/Lassy/

Verb matrices are created to be tested on a dataset of relative clauses. This dataset is a loose translation of the one used by Rimmell, Maillard, Polajnar & Clark (2016).
https://www.repository.cam.ac.uk/handle/1810/256355

The trained verb matrices are included, as well as the database of relative clauses used to test them.

Since each python file corresponds to one step in the analysis, it is recommended to keep in mind the order in which these steps were performed when reviewing the code. See the file-overview document for a comprehensive graph of the structure between the python files. 
