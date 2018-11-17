# some filtering of the training directory. Checks for training files that do
# not have a corresponding verb stem (of which their should be none) and
# and verb stems for which no training data were found. Also prints the size
# of the training data for individual verbs.

# the filter_dir function is defined but not called on.

import os

#pathnames
path_o = '/media/luka/Seagate Expansion Drive/training2/VO'
path_s = '/media/luka/Seagate Expansion Drive/training2/VS'

#get paths for object-verb and subject-verb data
files_o = os.listdir(path_o)
files_s = os.listdir(path_s)

def filter_dir(path, files):
    """delete any files not in the stems list"""
    verbfile = open('./verb-stems-list.txt', 'r')
    verbs_raw = verbfile.read()
    verbfile.close()
    stems = verbs_raw.split()

    #identify any verb stems without corresponding data file
    for stem in stems:
        if not stem+'.txt' in files:
            print(stem)
    print()

    #identify any data files without corresponding verb stem
    for file in files:
        if not file[:-4] in stems:
            print(file)
            #os.remove(path+'/'+file)

def getsize(path, files):
    """print the size of each data file in the directory
    (i.e. number of instances for each verb)"""
    for file in files:
        conn = open(path+'/'+file, 'r')
        text = conn.read()
        conn.close()
        size = len(text.split('\n'))
        spacing = (25 - len(file) - len(str(size)))*' '
        print(file[:-4], spacing, size)

getsize(path_s, files_s)
