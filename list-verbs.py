# Compiles a list of verb stems that need to be trained from the translated
# RELPRON database, importing the Phrase class to read the database.

#import corpus processing class
import process-relpron-phrase

#pathnames
corpuspath = './repron_translation.txt'
outpath = 'verb-stems-list.txt'

#import copus
file = open(corpusfile,'r', encoding='latin-1')
items_raw = file.readlines()
file.close()

#read corpus
items_neat = []
for i in items_raw:
    #neat = processitem.Item(i)
    neat = process-phrase.Phrase(i)
    items_neat.append(neat)

#extract verbs
verbs = set()
for i in items_neat:
    verbs.add(i.V)

#export
outfile = open(outpath, 'w', encoding='utf-8')
for v in verbs:
    outfile.write(v+' ')
outfile.close()
