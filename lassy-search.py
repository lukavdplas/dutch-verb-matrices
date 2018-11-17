
# Conducts a search through the lassy coprus to extract observations of
# relevant verbs.

import xml.etree.ElementTree as ET

#pathnames
verbspath = './verb-stems-list.txt'
corpuspath = 'treebanks.txt'
outputpath = '/media/luka/Seagate Expansion Drive/training2/'

#import verbs
verbfile = open(verbspath, 'r')
verbs_raw = verbfile.read()
verbfile.close()
stems = verbs_raw.split()

#queries
query = './/node[@pos="verb"]/..node[@rel="obj1"][@cat="np"]/..'
query_o = './node[@rel="obj1"]'
query_s = './node[@rel="su"]'
query_v = './node[@pos="verb"]'
query_any_v = './/node[@pos="verb"]'
query_head = './node[@rel="hd"]'
query_rp = './/node[@cat="rel"]/node[@rel="body"][@cat="ssub"]'

#some functions for searching through XML tree

def findhead (node):
    """Find the head of an NP."""
    cat = node.get('cat')
    if cat == 'np':  #if it's an NP, find the head node
        return node.findall(query_head)[0]
    if node.get('pt') == 'n' or node.get('pt') == 'vnw':  #if it is a single noun or pronoun return the node itself
            return node
    return None  #else, return none. Usually a null pronoun

def findsbj (vp, root):
    """Find the subject of a VP, by looking through the entire tree."""
    sbj = vp.find(query_s)  #identify the verb's external argument
    if ET.iselement(sbj):
        head = findhead(sbj)  #check if the subject is overt
        if ET.iselement(head):
            return head
        index = sbj.get('index')  #if not, find an overt phrase with the same index
        if index:
            coindices = root.findall('.//node[@index="'+index+'"]')
            for node in coindices:
                result = findhead(node)
                if ET.iselement(result):
                    return result
    return None

#set up treebank files
fileref = open(corpuspath, 'r')
files_raw = fileref.read()
fileref.close()

files = files_raw.split('\n')
files_to_do = files

def updatefileref():
    """after each file, call on this function to remove it from reference file"""
    global files_to_do
    files_to_do = files_to_do[1:]
    fileref = open('treebanks.txt', 'w')
    for f in files_to_do:
        fileref.write(f)
        fileref.write('\n')
    fileref.close()

#loop through treebanks

for file in files:
    #progress update
    print(file[-10:], end='...')
    print ((100 -(100 * (len(files_to_do) / 3867))), '%...')
    #clear local output
    VO_output = dict()
    VS_output = dict()

    #open file
    f = open(file, 'r')
    raw = f.read()
    f.close()

    #loop trough sentences in data
    sentences = raw.split('<?xml version="1.0" encoding="UTF-8"?>')
    for sentence in sentences[1:]:
        try:
            #get root tree
            root = ET.fromstring(sentence)
            text = root.find('sentence').text.split(' ')
            #loop through all verbs
            for verb in root.findall(query_any_v):
                #see if it matches one of the training verbs
                for stem in stems:
                    if verb.get('root') == stem:
                        #clear variables
                        obj = None
                        sbj = None
                        #get the VP
                        v_id = verb.get('id')
                        vp = root.find('.//node[@id="' + v_id + '"]/..')
                        #find the object
                        obj_cons = vp.find(query_o)
                        verb_root = verb.get('root')
                        if ET.iselement(obj_cons):
                            obj = findhead(obj_cons)
                        #find the subject
                        sbj = findsbj(vp, root)

                        #formulate output for VO and VS
                        if ET.iselement(obj):
                            if obj.get('root'):
                                prefix = obj.get('root') + '|' #set up a prefix '[obj]|' e.g. 'bal|'
                                text[int(verb.get('begin'))] = '&&|' + verb.get('root') + '|' + obj.get('root')  #substitute the verb with a token '&&|[verb]|[obj]' e.g. '&&|gooi|bal'
                                joined = ' '.join(text)
                                output = prefix + ' ' + joined
                                if verb_root in VO_output:
                                    VO_output[verb_root].append(output)
                                else:
                                    VO_output[verb_root] = [output]
                        if ET.iselement(sbj):
                            if sbj.get('root'):
                                prefix = sbj.get('root')+'|' #set up a prefix '[obj]|' e.g. 'hij|'
                                text[int(verb.get('begin'))] = '&&|' + verb.get('root') + '|' + sbj.get('root')  #substitute the verb with a token '&&|[verb]|[subj]' e.g. '&&|gooi|hij'
                                joined = ' '.join(text)
                                output = prefix + ' ' +  joined
                                if verb_root in VS_output:
                                    VS_output[verb_root].append(output)
                                else:
                                    VS_output[verb_root] = [output]
        except Exception as e:
            print(e)

    #save results to files
    for verb in VO_output.keys():
        outfile = open(outputpath+'VO/'+verb+'.txt', 'a')
        for i in VO_output[verb]:
            outfile.write(i+'\n')
        outfile.close()

    for verb in VS_output.keys():
        outfile = open(outputpath+'VS/'+verb+'.txt', 'a')
        for i in VS_output[verb]:
            outfile.write(i+'\n')
        outfile.close()

    updatefileref()
