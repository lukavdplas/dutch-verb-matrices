# Creates an index array fro training verbs. Read the rows file line by line,
# identify corresponding holistic vector and arg vector, save an array which
# stores a list of row numbers and argument strings per verb.

import re
import numpy as np
from reach import Reach
import transformargs

#pathnames
rowspath = './cooccurrence/weighted_sm.rows'
embeddingspath = './tulkens-embeddings/160/sonar-160.txt'
logpath = './failedwords.txt'
exportpath = './verbtrainingindex2'

#import data
rowsfile = open(rowspath, 'r', encoding='utf-8')
r = Reach(embeddingspath, header=True)
#holmatrix = np.load(holmatrixpath)

#load output file
log = open(logpath, 'w', encoding='utf-8')

control = np.zeros(160)
failedcount = 0
rowcount = 590408
t = transformargs.Transformer()
verbarray = np.array(['', np.array([np.array([0,''], object)], object)], object)   #will contain line indexes and corresponding argument strings for each verb
                                                                #dummy first row added to show structure
verbindex = 0
oldkey = ''

#loop through v-arg combinations
for i in range(rowcount):
    #parse row names
    line = rowsfile.readline()
    try:
        verb, rel, arg = line[:-1].split('|')
    except ValueError:
        #apparently argument names sometimes include the | character. in that
        #case, use REs to parse row names
        verb = re.search(r'^(\w)+(?=\|)', line).group(0)
        rel = re.search(r'(?<=\|)(\w)+(?=\|)', line).group(0)
        arg = re.search(r'(?<=(O|S)\|).+$', line).group(0)

    key = verb+'|'+rel
    # check if this is a new row
    if oldkey != key:
        verbarray = np.vstack([verbarray,
                            np.array([key,
                                        np.array([
                                                np.array([0, ''], object)
                                                ], object)
                                    ], object)
                            ])
        verbindex += 1
    oldkey = key

    arg_v = np.array(r.vector(arg))
    if np.array_equal(arg_v, control):
        new_args = t.transform(arg)
        arg_str = ''
        for w in new_args:
            new_v = np.array(r.vector(w))
            if not np.array_equal(new_v, control):
                arg_str = w
                break
    else:
        arg_str = arg
    if not arg_str:
        log.write(arg+'\t\t'+str(new_args)+'\n')
        failedcount += 1
    else:
        verbarray[-1][1] = np.vstack([verbarray[-1][1], np.array([i, arg_str], object)])

print('Failed loading', failedcount, 'out of', rowcount, 'items. ('+ (100*failedcount/rowcount) +'%)')
log.close()
rowsfile.close()

np.save(exportpath, verbarray)
