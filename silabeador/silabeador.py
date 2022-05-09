#!/usr/bin/env python3
import re
from sys import prefix


def syllabify(word, exceptions=True):
    return syllabification(word, exceptions).syllables


def tonica(word, exceptions=True):
    return syllabification(word, exceptions).stress


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


class syllabification:
    vowels = 'aeiouáéíóúäëïöüàèìòùAEIOUÁÉÍÓÚÄËÏÓÜÀÈÌÒÙ'
    semivowels = 'wj'
    stressed = 'áéíóúÁÉÍÓÚ'
    close = 'iuIU'
    openv = 'aeoAEO'
    close_ipa = 'jw'
    weak = 'eiéí'
    hiatuses = 'úíÚÍ'
    diereses = 'äëïöüÄËÏÖÜ'

    def __init__(self, word, exceptions=True, ipa=False):
        self.__ipa = ipa
        self.word = self.__make_exceptions(word, exceptions)
        if self.__ipa:
            self.vowels += self.semivowels
            self.close += self.close_ipa
            self.word = self.word.replace("'", '').replace('ˌ', '')
        self.syllables = self.__syllabify(self.word, self.__ipa)
        self.stress = stressed_s(self.syllables)

    def __make_exceptions(self, word, exceptions):
        if exceptions:
            import importlib.resources as pkg_resources
            lines = pkg_resources.read_text('silabeador', 'exceptions.lst')
            nouns = lines.splitlines()
            nouns = [noun.strip().split()
                     for noun in nouns if not noun.startswith('#')]
        else:
            nouns = []
        uir = ['uir', 'uido', 'uida', 'uid', 'uidos', 'uidas'
               'uimos',
               'uiste', 'uisteis',  'uido', 'uida', 'uid'
               'uiré', 'uirás', 'uirá', 'uiremos', 'uiréis', 'uirán',
               'uiría', 'uirías', 'uiría', 'uiríamos', 'uiríais', 'uirían',
               'uiɾ', 'uido', 'uida', 'uid', 'uidos', 'uidas'
               'uimos',
               'uiste', 'uisteis',  'uido', 'uida', 'uid'
               'uiɾé', 'uiɾás', 'uiɾá', 'uiɾemos', 'uiɾéis', 'uiɾán',
               'uiɾía', 'uiɾías', 'uiɾía', 'uiɾíamos', 'uiɾíais', 'uiɾían']

        uar = ['uar', 'uado', 'uada', 'uad', 'uás', 'uados', 'uadas'
               'uamos', 'uáis',
               'uaba', 'uabas', 'uábamos', 'uabais', 'uaban',
               'uaste', 'uó', 'uamos', 'uasteis', 'uaron',
               'uaré', 'uarás', 'uará', 'uaremos', 'uaréis', 'uarán',
               'uaría', 'uarías', 'uaría', 'uaríamos', 'uaríais', 'uarían',
               'uaɾ', 'uado', 'uada', 'uad', 'uás', 'uados', 'uadas'
               'uamos', 'uáis',
               'uaba', 'uabas', 'uábamos', 'uabais', 'uaban',
               'uaste', 'uó', 'uamos', 'uasteis', 'uaɾon',
               'uaɾé', 'uaɾás', 'uaɾá', 'uaɾemos', 'uaɾéis', 'uaɾán',
               'uaɾía', 'uaɾías', 'uaɾía', 'uaɾíamos', 'uaɾíais', 'uaɾían',
               'acuí', 'akui', 'uoso', 'uosa', 'uosos', 'uosas']

        but = ['g', 'c']
        for noun in nouns:
            if re.search(re.compile(noun[0]), word):
                word = re.sub(re.compile(noun[0]), noun[1], word)
        if (any(word.endswith(x) for x in uir if len(x)+2 <= len(word))
            or any(word.endswith(x) for x in uar
                   if not word.endswith(f'g{x}'))):
            word = re.sub('i([aeouáéó])', r'i_\1', word)
            if not any(x in word for x in ['gu', 'qu', 'cu', 'ku']):
                word = re.sub('u([aeioáéó])', r'u_\1', word)
        return word

    def __syllabify(self, letters, ipa):
        foreign_lig = {'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
                       'ã': 'a', 'ẽ': 'e', 'ĩ': 'i', 'õ': 'o', 'ũ': 'u',
                       'ﬁ': 'fi', 'ﬂ': 'fl'}
        letters_dic = {'b': 'be', 'c': 'ce', 'd': 'de', 'f': 'efe', 'g': 'ge',
                       'h': 'hache', 'j': 'jota', 'k': 'ka', 'l': 'ele',
                       'm': 'eme', 'n': 'ene', 'p': 'pe', 'q': 'qu',
                       'r': 'erre', 's': 'ese', 't': 'te', 'v': 'uve',
                       'w': 'uvedoble', 'x': 'equis',
                       'z': 'zeta', 'ph': 'pehache'}
        slbs = []
        word = re.sub(r'\W', '', letters)
        word = ''.join([letter if letter not in foreign_lig
                        else foreign_lig[letter] for letter in letters])
        if word.lower() in letters_dic:
            word = letters_dic[word]
        slbs[:0] = word
        slbs = self.__join(slbs, ipa)
        slbs = self.__split(slbs, self.__ipa)
        return [x.strip() for x in slbs]

    def __join(self, letters, ipa):
        weak = 'eiéí'
        hiatuses = 'úíÚÍ'
        diereses = 'äëïöüÄËÏÖÜ'
        if ipa:
            semivowels = 'wjiu'
        else:
            semivowels = 'iu'
        word = []
        for letter in letters:
            if len(word) == 0:
                word = [letter]
            elif all(vocal in self.vowels + semivowels
                     for vocal in [letter, ultima]) and any(
                         vocal in semivowels for vocal in [letter, ultima]):
                if letter in weak and any(''.join(word).lower().endswith(x)
                                          for x in ['gü', 'qu', 'gu',
                                                    'ɣw', 'gw']):
                    word[-1] = word[-1] + letter
                elif any(vocal in self.close for vocal in letter + ultima):
                    if letter not in hiatuses+diereses and ultima not in diereses:
                        word[-1] = word[-1] + letter
                    elif letter == 'í' and len(word) > 1 and (
                            word[-2:] == ['c', 'u']):
                        word[-1] = word[-1] + letter
                    else:
                        word = word + [letter]
                else:
                    word = word + [letter]
            elif ultima == '_':
                word[-1] = letter
            elif letter == '_':
                word = word + [letter]
            else:
                word = word + [letter]
            ultima = word[-1][-1]
        return word

    def __split(self, letters, ipa):
        indivisible_onset = ['pl', 'bl', 'fl', 'cl', 'kl', 'gl', 'll',
                             'pr', 'br', 'fr', 'cr', 'kr', 'gr', 'rr',
                             'dr', 'tr', 'ch', 'dh', 'rh',
                             'βl', 'ɣl',
                             'βɾ', 'pɾ', 'fɾ', 'kɾ', 'gɾ', 'ɣɾ', 'dɾ', 'ðɾ',
                             'tɾ', 'bɾ', 'tʃ', 'gw', 'ɣw']
        indivisible_coda = ['ns', 'bs', 'nz', 'βs', 'bz', 'βz']
        word = []
        onset = ''
        if ipa:
            symbols = ''
        else:
            symbols = 'jw'
        if len(letters) == 1:
            word = letters
        else:
            for letter in letters:
                if letter == '_':
                    pass
                elif all(x.lower() not in self.vowels for x in letter):
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
