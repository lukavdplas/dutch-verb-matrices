# training and export of verb matrices. load holistic vectors and argument
# vectors, perform ridge regression to train a matrix and export the final
# product.

import numpy as np
from reach import Reach
import sklearn
import sklearn.linear_model
import sklearn.preprocessing
import math
import matplotlib.pyplot as plt
from tqdm import tqdm_notebook as tqdm
import pandas as pd

#pathnames
indexpath = './verbtrainingindex_withweights.npy'
holmatrixpath = './cooccurrence/svd/newmatrix.npy'
embeddingspath = './tulkens-embeddings/160/sonar-160.txt'
outputpath = './verbmatrices/version3'

#import data
index = np.load(indexpath)
holmatrix = np.load(holmatrixpath)
arg_data = Reach(embeddingspath, header=True)

#parameters
n_dim = 160
s_dim = 200
alpha_value = 50
min_sample_size = 400
# note how in testing, a samplesize of N = 500 was deemed acceptable. here we
# do not split in train an test data, so the min sample size can be 80% of the
# one used when testing.
variance_control = True
mean_std = 0.08

matrices = dict()

#loop through verbs
for row in tqdm(index):
    if len(row[0]) >= 1:
        verb = row[0]
        samples = row[1]
        #containers for train and test data
        hol_vs = {'train': np.zeros((1, s_dim)), 'test': np.zeros((1, s_dim))}
        arg_vs = {'train': np.zeros((1, n_dim)), 'test': np.zeros((1, n_dim))}
        weights = {'train': np.array([0.0]), 'test': np.array([0.0])}

        # randomly select train an test data
        samplesize = samples.shape[0]
        if samplesize > min_sample_size:
            trainindices = list(range(samplesize))
            # load vectors into train and test collections
            for i in range(samplesize):
                dest = ''
                if len(trainindices) > 0 and trainindices[0] == i:
                    dest = 'train'
                    trainindices = trainindices[1:]
                else:
                    dest = 'test'
                sample = samples[i]
                # samples are of form holmatrixrow, argstring, weight
                if sample[1] != '':
                    # import of vectors
                    hol_v = holmatrix[int(sample[0])]
                    arg_v = arg_data.vector(sample[1])
                    weight = float(sample[2])

                    #apply standard scaling
                    scaler = sklearn.preprocessing.StandardScaler(with_std=False)
                    arg_v = scaler.fit_transform(arg_v[:, np.newaxis])
                    arg_v = np.squeeze(arg_v)

                    #apply standard scaling
                    scaler = sklearn.preprocessing.StandardScaler()
                    scaler.set_params(with_std=variance_control)
                    arg_v = scaler.fit_transform(arg_v[:, np.newaxis])
                    arg_v = np.squeeze(arg_v)
                    if variance_control:
                        arg_v = mean_std * arg_v

                    #store holistic vector
                    if np.array_equal(hol_vs[dest], np.zeros((1, s_dim))):
                        hol_vs[dest] = np.array([hol_v])
                    else:
                        hol_vs[dest] = np.vstack([hol_vs[dest], hol_v])
                    #store argument vector
                    if np.array_equal(arg_vs[dest], np.zeros((1, n_dim))):
                        arg_vs[dest] = np.array([arg_v])
                    else:
                        arg_vs[dest] = np.vstack([arg_vs[dest], arg_v])
                    #store weight
                    if np.array_equal(weights[dest], np.array([0.0])):
                        weights[dest] = np.array([weight])
                    else:
                        weights[dest] = np.hstack([weights[dest], np.array([weight])])

            # train matrix
            verb_m = np.zeros((n_dim, s_dim))
            R2s = np.zeros(s_dim)
            R2s_train = np.zeros(s_dim)
            #train one column of the matrix
            for i in range(s_dim):
                model = sklearn.linear_model.Ridge(alpha=alpha_value, fit_intercept=False)
                model.fit(arg_vs['train'], hol_vs['train'][:, i, np.newaxis], sample_weight=weights['train'])
                #extract trained weights
                verb_m[:, i] = model.coef_

            matrices[verb] = verb_m

#export verb matrices as numpy arrays
for verb in matrices.keys():
    outputstr = outputpath+'/'+verb
    np.save(outputstr+'.npy', matrices[verb])
