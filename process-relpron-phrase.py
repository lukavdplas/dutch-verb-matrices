# This defines a class Phrase which is intended to read a single item in the
# translated RELPRON database, and do some pre-processing for analysis.

import re

letters = r'([èëéïCD]|[a-z])+'
nonletters = r'(\:|\n| |/)+'
typeletters = r'(O|S)BJ'

class Phrase:
    """object for item, allows easy
    access to properties like head
    noun, structure, etc."""
    def __init__(self, text):
        words = text.split()
        self.type = words[0]
        self.termN = words[1][:-1]
        self.NP = words[2:]
        self.headN = self.NP[0]
        argument = self.NP[2]
        verb = self.NP[-1]
        self.argN = re.split(r'/', argument)[-1]
        self.V = re.split(r'/', verb)[-1]

    def NPstring (self, inflection=True):
        """Return a string of the property. Parameter
        inflection determines if you get inflected version
        (standard) or word stems.
        """
        NPlist = list(self.NP)
        if inflection:
            n = 0
        else:
            n = -1
        NPlist[2] = re.split(r'/', NPlist[2])[n]
        NPlist[-1] = re.split(r'/', NPlist[-1])[n]
        return " ".join(NPlist)

    def taggedNP (self):
        """May be useful for alpino parsing or vector
        composition. Gives tuples of words and POS tags.
        Tags probably need to be changed.
        """
        tags = ['noun', 'pronoun', 'noun', 'verb']
        words = self.NPstring(True).split()
        tuples = []
        for n in range(len(words)):
            tuples.append((words[n], tags[n]))
        return tuples
