# Sorts the data assembled by create-cooccur-matrix. This converts what is
# essentially just a list of observations into a proper sparse matrix.

#pathnames
vocabpath = 'vocab.txt'
matrixpath = './cooccurrence/'

#import vocab list
vocabfile = open(vocabpath, 'r')
vocab_raw = vocabfile.read()
vocabfile.close()

# convert vocab to column index
cols = vocab_raw.split(' ')
positions = dict()
cols_out = open(matrixpath+'cols1.cols', 'w')
t = 0
for col in cols:
    positions[col] = t
    t += 1
    cols_out.write(col)
    cols_out.write('\n')
cols_out.close()

def getvocabindex(word):
    return(positions[word])

#
smfile = open(matrixpath+'spm1.sm', 'r')
matrix_raw = smfile.read()
smfile.close()
matrix_rows = matrix_raw.split('\n')
matrix_tuples = list()
for row in matrix_rows:
    tup = row.split(' ')
    matrix_tuples.append(tup)
