# transform an int into a string with the full dutch word for the number. only
# works up to 999, because after that words would always be spelled with spaces
# in between.


class Converter:
    def __init__(self):
        self.units = ['nul', 'een', 'twee', 'drie', 'vier', 'vijf', 'zes', 'zeven', 'acht', 'negen']
        self.tens = ['', 'tien', 'twintig', 'dertig', 'veertig', 'vijftig', 'zestig', 'zeventig', 'tachtig', 'negentig']
        self.exceptions = {11: 'elf', 12: 'twaalf', 13: 'dertien', 14: 'veertien'}

    def convert(self,i):
        result = ''
        e2 = int(i/100)
        if e2 > 0:
            if e2 > 1:
                result = result + self.lasttwo(e2)
            result = result+'honderd'
        result = result + self.lasttwo(i%100)
        return result

    def lasttwo(self,i):
        """For any n in [0,100)"""
        if i in self.exceptions.keys():
            return self.exceptions[i]
        e0 = i % 10
        e1 = int(i/10)
        if e1 == 0:
            return self.units[e0]
        word = ''
        if e0 >= 1:
            word = self.units[e0]
        if e1 == 1 or word == '':
            return word+self.tens[e1]
        if word.endswith('e'):
            return word + 'ën' + self.tens[e1]
        return word+'en'+self.tens[e1]
