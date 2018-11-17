# try transforming the argument strings in the 'failed arguments' document
# created by train-verbs-index for the purpose of oading their appropriate
# vector. This file does not load the actual embeddings that the arguments
# need to match, which makes it faster to run for testing.

import re
import numeraltostring

class Transformer:
    """Class for the operations to process arguments"""
    def __init__(self):
        self.c = numeraltostring.Converter()

    def transform(self, w):
        """basic frame for transforming a word. import the word, redirect to
        relevant methods, then export a list of alternatives."""
        #check if the word is a number
        if re.match(r'[0-9]+(e|de|ste)?$', w):
            return self.numeral(w)
        w = w.lower()
        options = []
        suffixes = []
        #store possible suffix changes
        #see if the word is a diminutive
        if w.endswith('_dim'):
            suffixes = self.dim(w)
            w = w[:-4]
        #see if it is an unparsed plural form
        elif w.endswith('s') or w.endswith('en'):
            suffixes = self.singular(w)
        options = [w]
        #try to fuse compound words
        if len(w.split('_')) > 1:
            options = self.fuse(w)
        #merge word with suffix options
        if len(suffixes) > 0:
            newoptions = []
            for s in suffixes:
                for o in options:
                    if s[1] == 'rep':
                        newoptions.append(o+o[-1]+s[0])
                    elif s[1] == 'del':
                        newoptions.append(o[:-1]+s[0])
                    elif s[1] == 'del2':
                        newoptions.append(o[:-2]+s[0])
                    else:
                        newoptions.append(o+s[0])
            options = newoptions
        return(options)

    def fuse(self, w):
        """fuse compound words"""
        parts = w.split('_')
        bridges = '', '-', 's', 'en', 'e'
        fused = []
        fused.append(parts[0])
        for part in parts[1:]:
            newfused = []
            for b in bridges:
                if b.startswith('e'):
                    #some exceptions for words like paddenstoel, schapenwol
                    prefixes = []
                    if re.search(r'(^|[^aeiouy])[aeiouy][^aeiouy]$', fused[0]):
                        # like in pad_stoel -> paddenstoel
                        for i in range(len(fused)):
                            prefixes.append(fused[i]+fused[i][-1])
                    elif re.search(r'(aa|ee|oo|uu)[^aeiouy]$', fused[0]):
                        # like in schaap_wol -> schapenwol
                        for i in range(len(fused)):
                            prefixes.append(fused[i][:-2]+fused[i][-1])
                    else:
                        prefixes = fused
                    #now change exceptions like brief_bus -> brievenbus
                    if re.search(r'[^f]f$', prefixes[0]):
                        newprefixes = []
                        for i in range(len(prefixes)):
                            #add voiced-final variant and original
                            newprefixes.append(prefixes[i][:-1]+'v')
                            newprefixes.append(prefixes[i])
                        prefixes = newprefixes
                    # identical but for s-z
                    if re.search(r'[^s]s$', prefixes[0]):
                        newprefixes = []
                        for i in range(len(prefixes)):
                            newprefixes.append(prefixes[i][:-1]+'z')
                            newprefixes.append(prefixes[i])
                        prefixes = newprefixes
                else:
                    prefixes = fused
                for p in prefixes:
                    newfused.append(p+b+part)
            fused = newfused
        return fused

    def dim(self, w):
        """change '_DIM' suffix into actual diminiutive form. not completely
        accurate, but the goal is to catch most forms"""
        stem = w[:-4]
        lst = []
        # stack possible suffixes. a suffix indicates the suffix, then whether
        # the last character should be repeated (rep), deleted (del) or left (None)
        if re.search(r'(m|n)$', stem):
            #like in oom -> oompje, lam, lammetje
            lst.append(('pje', None))
            if re.search(r'(?<![aeiou])[aeiouy](m|n)$', stem):
                #like in kom -> kommetje
                lst.append(('etje', 'rep'))
        elif re.search(r'ng$', stem):
            #like in koning -> koninkje, slang -> slangetje
            lst.append(('kje', 'del'))
            lst.append(('etje', None))
        elif re.search(r'[aeiou]$', stem):
            # like in kado -> kadootje
            if re.search(r'(?<![aeiou])[aeiou]$', stem):
                lst.append(('tje', 'rep'))
        elif re.search(r'(?<![aeiou])[aeiouy][^aeiouy]$', stem):
            #like in kip -> kippetje
            lst.append(('etje', 'rep'))
        lst.append(('je', None))
        if (r'[qwryshjklzcvb]$', stem):
            lst.append(('tje', None))
        return lst

    def singular(self,w):
        """try removing a possible plural suffix"""
        sing = [('', None)]
        if w.endswith('\'s|[ie]ë)'):
            sing.append(('', 'del2'))
        elif re.search(r'[^aeio]en$', w):
            sing.append(('', 'del2'))
        elif re.search(r'[^aeiouys]s$', w):
            sing.append(('', 'del'))
        return sing

    def numeral(self, w):
        """turn a numeral into a list with the string. also covers ordinals."""
        if re.match(r'[0-9]+$', w):
            i = int(w)
            suffix = None
        else:
            i = int(re.match(r'[0-9]+', w).group(0))
            suffix = re.search(r'(e|ste|de)$', w).group(0)
        if i < 1000:
            word = self.c.convert(i)
            if suffix:
                if suffix == 'de' or suffix == 'ste':
                    return[word+suffix]
                else:
                    if i == 1:
                        return['eerste']
                    if i == 8:
                        return['achtste']
                    if i >= 20:
                        return[word+'ste']
                    return[word+'de']
            else:
                return[word]
        else:
            return w

# code for testing
#testwords = ['os_haas']
#t = Transformer()
#for word in testwords:
#    print(t.transform(word))
