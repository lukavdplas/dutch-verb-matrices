# Imports the frequency of each verb-arg combination as counted in
# create-cooccur-matrix.py, and uses that to make a list of sample weights for
# ridge regression. Weights are calculated as the log of the frequency.

import numpy as np
import math
import transformargs
import re

# pathnames
freqpath = './cooccurrence/arg_freq.txt'
indexpath = './verbtrainingindex2.npy'
exportpath = './verbtrainingindex_withweights'

index = np.load(indexpath)
freqfile = open(freqpath, 'r')
t = transformargs.Transformer()

rowcount = 0

freqdict = dict()
for line in freqfile.readlines():
    items = line[:-1].split()
    freq = int(items[1])

    #decipher tag
    try:
        verb, rel, arg = items[0].split('|')
    except ValueError:
        #apparently argument names sometimes include the | character. in that
        #case, use REs to parse row names
        verb = re.search(r'^(\w)+(?=\|)', items[0]).group(0)
        rel = re.search(r'(?<=\|)(\w)+(?=\|)', items[0]).group(0)
        arg = re.search(r'(?<=(O|S)\|).+$', items[0]).group(0)
    key = verb + '|' + rel

    if not key in freqdict.keys():
        freqdict[key] = dict()

    freqdict[key][arg] = freq
    alt_args = t.transform(arg)
    for a in alt_args:
        freqdict[key][a] = freq

"""
for row in index:
    verbrel = row[0]
    if verbrel != '':
        for sample in row[1]:
            if sample[1] != '':
                arg = sample[1]
                freq = freqdict[verbrel][arg]
                weight = math.log(freq)
"""

newindex = np.array(['', [0, '']], object)


for i in range(len(index)):
    row = index[i]
    verbrel = row[0]
    if verbrel != '':
        newindex = np.vstack([newindex, np.array([verbrel, [0, '', 0.0]], object)])
        for j in range(len(row[1])):
            sample = row[1][j]
            if sample[1] != '':
                matrixrow = sample[0]
                arg = sample[1]
                freq = freqdict[verbrel][arg]
                weight = math.log(freq)
            else:
                matrixrow = 0
                arg = ''
                weight = 0.0
            newindex[-1][1] = np.vstack([newindex[-1][1], np.array([matrixrow, arg, weight])])

np.save(exportpath, newindex)
