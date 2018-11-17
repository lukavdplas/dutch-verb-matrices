# Preparation for searching throug the Lassy corpus. Assembles a list of all
# treebankfiles in the LassyLarge corpus, and stores their complete path in a
# txt file

from os import listdir

#directories
corpus = '/media/luka/Seagate Expansion Drive/LassyLarge/'
outpath = 'treebanks.txt'

output = open(outpath, 'w')

treebanks = []
for subdir in listdir(corpus):
    if subdir.startswith('WR'):
        treebanks.append(corpus+subdir+'/COMPACT/')
for treebank in treebanks:
    files = []
    for filename in listdir(treebank):
        if filename.endswith('.data'):
            files.append(filename)

    for file in files:
        output.write(treebank+ file)
        output.write('\n')

output.close()
