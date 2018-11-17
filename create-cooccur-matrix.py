# Takes the assembled training data with VO and VS combinations and counts
# cooccurence with words in the vocabulary. Counts within a window around the
# verb.
# V-argument pairs that only occur once are filtered out. Words are stored
# as <NUM>, <PUNCT>, or <UNK> when appropriate.
# output is stored in a single file (which will later be converted into a
# sparse matrix)

import re

#pathnames
outputpath = './cooccurrence/'
filerefpath_vo = 'verbs_vo.txt'
filerefpath_vs = 'verbs_vs.txt'
vocabpath = 'vocab.txt'
datapath = '/media/luka/Seagate Expansion Drive/training2/'
freqpath = './cooccurrence/arg_freq.txt'

#parameters, REs
window = 8    #window = nr of words on either side of token (so window of 2 looks at 5-grams)
numerals = r'^[0-9]+$'
alphanumeric = r'\w+'

#clear output files
output = open(outputpath+'spm1.sm', 'w')
output.write('')
output.close()

rowsfile = open(outputpath+'rows1.rows', 'w')
rowsfile.write('')
rowsfile.close()

freqfile = open(outputpath+'arg_freq.txt', 'w')
freqfile.write('')
freqfile.close()

#import verbs and make "to do" list from file index
to_do = list()

fileref = open(filerefpath_vo, 'r')
raw = fileref.read()
fileref.close()
verbs_o = raw.split('\n')
for verb in verbs_o:
    if len(verb) > 1:
        to_do.append((verb, 'O'))

fileref = open(filerefpath_vs, 'r')
raw = fileref.read()
fileref.close()
verbs_s = raw.split('\n')
for verb in verbs_s:
    if len(verb) > 1:
        to_do.append((verb, 'S'))


#split up to-do list in batches of 5 verbs
"""Note: Using batches of verb-relation pairs is just a way to prevent all of
the observed data from being stored in the working memory, while also making
sure some steps like vocabulary filtering and exporting output are not done with
every verb.
"""
sorted_to_do = sorted(to_do, key=lambda pair: pair[0])  #sort to-do list by verb
batches = list()
t = 0
current_batch = list()
for (word, relation) in sorted_to_do:
    if t < 5:
        current_batch.append((word, relation))
        t += 1
    else:
        batches.append(current_batch)
        current_batch = list()
        current_batch.append((word, relation))
        t = 0

#import vocabulary
vocab_file = open(vocabpath)
vocab_raw = vocab_file.read()
vocab_file.close()
vocab_list = vocab_raw.split(' ')
vocab_set = set(vocab_list)

vocab_positions = dict()
t = 0
for col in vocab_list:
    vocab_positions[col] = t
    t += 1

def getvocabindex(word):
    """return the index of  corresponding matrix column for a word in the vocabulary"""
    return(vocab_positions[word])

#loop through bathces
batchcount = 1
batchtotal = len(batches)
for batch in batches:
    matrix = dict()
    argfreqs = dict() #stores frequences of argumens for each verb-relation pair
    print()
    print('BATCH', batchcount, '/', batchtotal)
    batchcount += 1
    for (verb, relation) in batch:
        print(verb+' ('+relation+')...')
        if len(verb) > 2:
            argfreqs[verb+'|'+relation] = dict()
            #import data from relevant file
            verbfile = open(datapath+'V'+relation+'/'+verb+'.txt', 'r')
            raw = verbfile.read()
            verbfile.close()
            examples = raw.split('\n')

            #read each sentence in the data
            for e in examples:
                sent = e.split(' ')
                if len(sent) >= 2:
                    #get argument
                    arg = sent[0][:-1]
                    #add to count in argfreqs
                    if arg in argfreqs[verb+'|'+relation]:
                        argfreqs[verb+'|'+relation][arg] += 1
                    else:
                        argfreqs[verb+'|'+relation][arg] = 1
                    #create entry for verb|relation|argument in matrix  if necessary
                    item = verb + '|' + relation + '|' + arg
                    if not item in matrix:
                        matrix[item] = dict()

                    #get data from sentence
                    #find location of verb in sentence
                    x = 0
                    found = False
                    while found == False and x < len(sent):
                        if sent[x].startswith('&&|'+verb):
                            found = True
                        else:
                            x += 1
                    #get context window
                    context_start = x - window
                    if context_start < 1:
                        ngram = ['<S>']     #add start marker
                        context_start = 1
                    else:
                        ngram = []
                    context_end = x + window + 1
                    if context_end >= len(sent):
                        context_end = len(sent)
                        end = True
                    else:
                        end = False
                    #add words to ngram
                    for n in range(context_start,context_end):
                        word = sent[n]
                        if n != x:
                            if re.match(numerals, word):
                                ngram.append('<NUM>')
                            elif re.search(alphanumeric, word):
                                ngram.append(word.lower())
                            else:
                                ngram.append('<PUNCT>')
                    if end:
                        ngram.append('</S>')    #add end marker
                    #add observed words to matrix
                    for word in ngram:
                        if word in matrix[item]:
                            matrix[item][word] += 1
                        else:
                            matrix[item][word] = 1
            #filter arguments with freq < 2 and export freq matrix
            freqfile = open(freqpath, 'a')
            for arg in argfreqs[verb+'|'+relation]:
                frequency = argfreqs[verb+'|'+relation][arg]
                if frequency > 1:
                    entry = verb + '|' + relation + '|' + arg + ' ' + str(frequency)
                    freqfile.write(entry)
                    freqfile.write('\n')
                else:
                    item = verb + '|' + relation + '|' + arg
                    matrix.pop(item)
            freqfile.close()
    #transfer counts of unknown words to UNK
    print()
    print('filtering vocab...')
    for token in matrix:
        matrix[token]['<UNK>'] = 0
        for word in matrix[token]:
            if not word in vocab_set:
                matrix[token]['<UNK>'] += matrix[token][word]
                matrix[token][word] = 0
    #sort items in matrix
    items_set = set()
    for token in matrix:
        items_set.add(token)
    items_list = []
    for item in items_set:
        items_list.append(item)
    sorted_items = sorted(items_list)
    #write output to file
    print()
    print('writing output...')

    output = open(outputpath+'spm1.sm', 'a')
    rowsfile = open(outputpath+'rows1.rows', 'a')

    for token in sorted_items:
        rowsfile.write(token+'\n')
        args = []
        for word in matrix[token]:
            if matrix[token][word] > 0:

                args.append(word)
        args_sorted = sorted(args, key=getvocabindex)
        for word in args_sorted:
               #print('   ', word, '   ', matrix[token][word])
            output.write(token+' '+word+' '+str(matrix[token][word])+'\n')

    output.close()
    rowsfile.close()
