# imports the sparse matrix and converts it to a sparse matrix in scipy format,
# then applies SVD to reduce dimensions and exports the matrix.

import scipy.sparse
import scipy.sparse.linalg
import numpy as np

#pathnames
smpath = './cooccurrence/sm_numbered.txt'
rowspath = './cooccurrence/weighted_sm.rows'
colspath = './cooccurrence/weighted_sm.cols'
outfile = './cooccurrence/svd/matrix2'

#get shape of matrix
print('assessing matrix shape...')
rowsfile = open(rowspath, 'r')
colsfile = open(colspath, 'r')
rowcount = len(rowsfile.readlines())
colcount = len(colsfile.readlines())
rowsfile.close()
colsfile.close()

#initiate sparse matrix in lil format
print('loading matrix...')
matrix = scipy.sparse.lil_matrix((rowcount, colcount), dtype='float32')

#read file and add entries to matrix
smfile = open(smpath, 'r')
for line in smfile.readlines():
    strings = line.split()
    data = [int(strings[0]), int(strings[1]), float(strings[2])]
    matrix[data[0], data[1]] = data[2]
smfile.close()

matrix.tocsr()

#apply SVD
print('applying SVD...')
u, s, vt = scipy.sparse.linalg.svds(matrix, k=200, return_singular_vectors='u')
matrix200 = u.dot(np.diag(s))

#export
print('exporting...')
np.save(outfile, matrix200)
