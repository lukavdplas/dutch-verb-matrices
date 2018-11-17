# Get the number of argument types for each verb+relation in the reduced
# matrix, which constitutes sample size for regression.

import numpy as np
import re

#pathnames
rowspath = './cooccurrence/weighted_sm.rows'
exportpath = './cooccurrence/sampleindex.txt'

index = [[None,0]]   #iniate list with dummy item (prevents later indexerror)

#count rows total
rowsfile = open(rowspath, 'r', encoding='latin-1')
for line in rowsfile.readlines():
    try:
        verb, rel, arg = line[:-1].split('|')
    except ValueError:
        #apparently argument names sometimes include the | character. in that
        #case, use REs to parse row names
        verb = re.search(r'^(\w)+(?=\|)', line).group(0)
        rel = re.search(r'(?<=\|)(\w)+(?=\|)', line).group(0)
        arg = re.search(r'(?<=(O|S)\|).+$', line).group(0)
    #add to count of verb
    if index[-1][0] == verb+'|'+rel:
        index[-1][1] += 1
    else:
        index.append([verb+'|'+rel, 1])
rowsfile.close()

index = index[1:]   #remove dummy item

export = open(exportpath, 'w')
for item, count in index:
    export.write(item+'\t'+str(count)+'\n')
export.close()
