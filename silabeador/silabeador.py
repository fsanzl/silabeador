import re


class Syllabification:
    __vowels = 'aeiouáéíóúäëïöüàèìòùAEIOUÁÉÍÓÚÄËÏÓÜÀÈÌÒÙ'
    __close = 'iuIUüÜ'

    def __init__(self, word, exceptions=True, ipa=False):
        self.__ipa = ipa
        if self.__ipa:
            self.__vowels += 'jw'
            self.__close += 'jw'
        if exceptions:
            self.__word = self.__make_exceptions(word)
        else:
            self.__word = word
        self.__word = self.__latin(self.__word)
        self.syllables = self.__syllabify(self.__word)
        self.stress = stressed_s(self.syllables)

    def __make_exceptions(self, word):
        from importlib import resources
        lines = resources.read_text('silabeador', 'exceptions.lst')
        nouns = lines.splitlines()
        nouns = [noun.strip().split() for noun in nouns if not noun.startswith('#')]
        for noun in nouns:
            word = re.sub(re.compile(noun[0]), noun[1], word)
        return word

    def __latin(self, verbum):
        flexiones = ('um', 'em', 'at', 'ant', 'it', 'unt', 'am', 'at', 'ur',
                     'it', 'int', 'et', 'ent')
        dictionarium = {'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú'}
        diphthongi = {'ae': 'æ', 'oe': 'œ'}
        if verbum.lower().endswith(flexiones) and not any(x in verbum.lower()
                                                          for x in 'áéíóú'):
            verbum = verbum.lower()
            for flexio in flexiones:
                if verbum.endswith(flexio):
                    verbum = re.sub(fr'{flexio}\b', f'_{flexio}', verbum)
            for clavis, pretium in diphthongi.items():
                verbum = verbum.replace(clavis, pretium)
            syllabae = self.__syllabify(verbum)
            if len(syllabae) == 2 or (len(syllabae) > 1 and (
                any(dipht in syllabae[-2] for dipht in diphthongi.values()) or
                len([x for x in dictionarium.keys() if x in syllabae[-2]]) > 1 or
                not syllabae[-2].endswith(tuple(dictionarium.keys())))):
                for clavis, pretium in dictionarium.items():
                    if clavis in syllabae[-2]:
                        syllabae[-2] = syllabae[-2].replace(clavis, pretium)
                        break
            elif any(dipht in syllabae[-3] for dipht in diphthongi.values()) or (
                len([x for x in dictionarium.keys() if x in syllabae[-3]]) > 1 or
                not syllabae[-3].endswith(tuple(dictionarium.keys()))):
                for clavis, pretium in dictionarium.items():
                    if clavis in syllabae[-3]:
                        syllabae[-3] = syllabae[-3].replace(clavis, pretium)
                        break
            if not any(x in ''.join(syllabae) for x in 'áéíóú'):
                for i in dictionarium:
                        syllabae[-2] = syllabae[-2].replace(i, dictionarium[i])
                        break
            verbum = syllabae
        return verbum


    def __syllabify(self, letters):
        foreign_lig = {'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
                       'ã': 'a', 'ẽ': 'e', 'ĩ': 'i', 'õ': 'o', 'ũ': 'u',
                       'ﬁ': 'fi', 'ﬂ': 'fl'}
        slbs = []
        if type(letters) is str:
            word = re.sub(r'\W', '', letters)
            word = ''.join([letter if letter not in foreign_lig
                        else foreign_lig[letter] for letter in letters])
            slbs[:0] = word
            slbs = self.__join(slbs)
            slbs = self.__split(slbs)
            letters = [x.strip() for x in slbs]
        return letters

    def __join(self, letters):
        frontal = 'eiéí'
        hiatuses = 'úíÚÍ'
        diereses = 'äëïöüÄËÏÖÜ'
        gwe = ['gü', 'qu', 'gu', 'ɣw', 'gw']
        diphthong = re.compile(f'[{self.__vowels}][{self.__close}]$')
        word = []
        word_sofar = ''
        last_letter = ''
        for letter in letters:
            if len(word) == 0:
                word = [letter]
            elif all(vocal in self.__vowels + self.__close
                     for vocal in (letter, last_letter)) and any(
                         vocal in self.__close for vocal in (letter, last_letter)):
                if letter in frontal and any(word_sofar.endswith(x) for x in gwe):
                    word[-1] = word[-1] + letter
                elif re.search(diphthong, word_sofar):
                    word = word + [word_sofar[-1]+letter]
                    word[-2] = word[-2][:-1]
                elif any(vocal in self.__close for vocal in letter + last_letter):
                    if letter not in hiatuses+diereses and last_letter not in diereses:
                        word[-1] = word[-1] + letter
                    elif letter == 'í' and len(word) > 1 and (
                            word[-2:] == ['c', 'u']):
                        word[-1] = word[-1] + letter
                    else:
                        word = word + [letter]
                else:
                    word = word + [letter]
            elif last_letter == '_':
                word[-1] = letter
            elif letter == '_':
                word += [letter]
            elif letter in 'œæ':
                word += [letter.replace('œ', 'oe').replace('æ', 'ae')]
            else:
                word = word + [letter]
            last_syllable = word[-1]
            last_letter = last_syllable[-1]
            word_sofar = ''.join(word).lower()
        return word

    def __split(self, letters):
        indivisible_onset = ['pl', 'bl', 'fl', 'cl', 'kl', 'gl', 'll',
                             'pr', 'br', 'fr', 'cr', 'kr', 'gr', 'rr',
                             'dr', 'tr', 'ch', 'dh', 'rh',
                             'βl', 'ɣl',
                             'βɾ', 'pɾ', 'fɾ', 'kɾ', 'gɾ', 'ɣɾ', 'dɾ', 'ðɾ',
                             'tɾ', 'bɾ', 'tʃ', 'gw', 'ɣw']
        indivisible_coda = ['ns', 'bs', 'nz', 'βs', 'bz', 'βz']
        word = []
        onset = ''
        if self.__ipa:
            symbols = ''
        else:
            symbols = 'jw'
        for letter in letters:
            if letter == '_':
                pass
            elif all(x.lower() not in self.__vowels for x in letter):
                if len(word) == 0:
                    onset = onset + letter
                else:
                    onset = onset + letter
                    media = len(onset) // 2
            elif len(onset) <= 1 or len(word) == 0:
                word = word + [onset+letter]
                onset = ''
            elif any(onset.endswith(x) for x in indivisible_onset):
                if len(word) > 0:
                    word[-1] = word[-1] + onset[:-2]
                    word = word + [onset[-2:] + letter]
                else:
                    word = word + [onset + letter]
                onset = ''
            elif any(onset.startswith(x) for x in indivisible_coda) and (
                    len(onset) > 2):
                word[-1] = word[-1] + onset[:2]
                word = word + [onset[2:] + letter]
                onset = ''
            else:
                if (onset[-1] in 'dðfkt' and onset[-2] in
                    'bβcθkdðfgɣkmɱɲñpqstvwxχz' + symbols
                    or onset[-1] in 'gɣ' and onset[-2] in 'cθtk' + symbols
                    or onset[-1] in 'lmɱ' and onset[-2] in 'mɱl'
                        or onset[-1] in 'cθ' and onset[-2] in 'kc'):
                    word[-1] = word[-1] + onset[:-1]
                    word = word + [onset[-1] + letter]
                else:
                    word[-1] = word[-1] + onset[:media]
                    word = word + [onset[media:] + letter]
                onset = ''
        word[-1] = word[-1] + onset
        return word


def stressed_s(slbs):
    if len(slbs) == 1:
        stress = -1
    elif len(slbs) > 2 and any(k in 'áéíóúÁÉÍÓÚ' for k in slbs[-3]):
        stress = -3
    else:
        if any(k in 'áéíóúÁÉÍÓÚ' for k in slbs[-2]):
            stress = -2
        elif any(k in 'áéíóúÁÉÍÓÚ' for k in slbs[-1]):
            stress = -1
        else:
            if (slbs[-1][-1] in 'nsNS' or
                    slbs[-1][-1] in 'aeiouAEIOU'):
                stress = -2
            else:
                stress = -1
    return stress

def syllabify(word, exceptions=True):
    return Syllabification(word, exceptions).syllables


def tonica(word, exceptions=True):
    return Syllabification(word, exceptions).stress
