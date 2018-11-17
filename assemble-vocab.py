# Gets word frequencies from the lassy corpus and uses that to assemble a list
# of the 10.000 most frequent words (or word tokens like <PUNCT> and <NUM>),
# which are exported.

import os
import re

#pathnames
outpath = 'vocab.txt'
path = '/media/luka/Seagate Expansion Drive/LassyLarge'

#assemble list of paths
contents = os.listdir(path)
treebanks = []
for c in contents:
    if c.startswith('W'):
        treebanks.append('/' + c)

# prepare frequency dict

freqs_master = {'<NUM>': 0, '<PUNCT>': 0}
numerals = r'^[0-9]+$'
alphanumeric = r'\w+'

# extract frequencies from corpus

for treebank in treebanks:
    f = open(path+treebank+'/WORD-LEMMA-POS.freq')
    freqs_raw = f.read()
    f.close()

    freqs_list = freqs_raw.split('\n')

    freqs = dict()
    for i in freqs_list:
        i_list_raw = re.split(r'\s+', i)
        i_list = []
        for n in i_list_raw:
            if re.match(r'\S+', n):
                i_list.append(n)
        if len(i_list) >= 2:
            word = i_list[1]
            count = int(i_list[0])
            if word in freqs:
                freqs[word] += count
            else:
                freqs[word] = count

    for word in freqs:
        t = freqs[word]
        if re.match(numerals, word):
            freqs_master['<NUM>'] += t
        else:
            if re.search(alphanumeric, word):
                if word.lower() in freqs_master:
                    freqs_master[word.lower()] += t
                else:
                    freqs_master[word.lower()] = t
            else:
                freqs_master['<PUNCT>'] += t

#make list of (word, freq) tuples and sort

tuples_raw = []

for word in freqs_master:
    count = freqs_master[word]
    tuples_raw.append((word, count))

tuples = sorted(tuples_raw, key=lambda pair: pair[1], reverse=True)

#filter 10.000 most frequent

tuples = tuples[:10000]

#assemble and export vocabulary list

vocab = []vs_outpath

for w, c in tuples:
    vocab.append(w)
vocab.append('<UNK>')

out = open(outpath, 'w')

for w in vocab:
    out.write(w)
    out.write(' ')

out.close()
