import re


class Syllabification:
    __vowels = 'aeiouáéíóúäëïöüàèìòùAEIOUÁÉÍÓÚÄËÏÓÜÀÈÌÒÙ'
    __close = 'iuIU'

    def __init__(self, word, exceptions=True, ipa=False):
        self.__ipa = ipa
        if self.__ipa:
            self.__vowels += 'jw'
            self.__close += 'jw'
        if exceptions:
            self.__word = self.__make_exceptions(word)
            self.__word = self.__latin(self.__word)
        else:
            self.__word = word
        self.syllables = self.__syllabify(self.__word)
        self.stress = stressed_s(self.syllables)

    def __make_exceptions(self, word):
        from importlib import resources
        lines = resources.read_text('silabeador', 'exceptions.lst')
        nouns = lines.splitlines()
        nouns = [n.strip().split() for n in nouns if n.strip() and not n.startswith('#')]
        for noun in nouns:
            word = re.sub(re.compile(noun[0]), noun[1], word)
        return word

    def __latin(self, verbum):
        flexiones = ('um', 'em', 'at', 'ant', 'it', 'unt', 'am')
        # 'int', 'ent', it', 'et', 'at', 'ur' 'int', 'ent'
        dictionarium = {'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú'}
        diphthongi = {'ae': 'æ', 'oe': 'œ'}
        if verbum.lower().endswith(flexiones) and not any(x in verbum.lower()
                                                          for x in 'áéíóú'):
            verbum = verbum.lower()
            for flexio in flexiones:
                if verbum.endswith(flexio):
                    verbum = re.sub(fr'{flexio}\b', f'_{flexio}', verbum)
                    break
            for clavis, pretium in diphthongi.items():
                verbum = verbum.replace(clavis, pretium)
            syllabae = self.__syllabify(verbum)
            if len(syllabae) == 1:
                pass
            elif len(syllabae) == 2 or (len(syllabae) > 1 and (
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
            else:
                for i in dictionarium:
                        syllabae[-2] = syllabae[-2].replace(i, dictionarium[i])
                        break
            verbum = syllabae
        return verbum

    def __syllabify(self, letters):
        slbs = []
        if type(letters) is str:
            foreign_lig = {'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
                        'ã': 'a', 'ẽ': 'e', 'ĩ': 'i', 'õ': 'o', 'ũ': 'u',
                        'ﬁ': 'fi', 'ﬂ': 'fl'}
            word = re.sub(r'\W', '', letters)
            word = ''.join([letter if letter not in foreign_lig
                        else foreign_lig[letter] for letter in letters])
            slbs = self.__split(word)
            slbs = self.__join(slbs)
            letters = [x.strip() for x in slbs]
        return letters

    def __split(self, letters, word = []):
        dipht = re.findall(rf'(?:[qg][wuü](?:[eé](?:h*[{self.__close}])'
                           '{,1}|i(?:h*[aeoáéó]){,1}|í)|'
                           fr'[{self.__close}](?:h*[aáoóeéi])(?:h*[{self.__close}])'
                           '{,1}|'
                           rf'[aáoóeéií](?:h*[{self.__close}]))\b', letters)
        digraph = ('ll', 'ch', 'rr')
        if dipht:
            dipht = dipht[0].strip('gq')
            word = self.__split(letters.removesuffix(dipht), [dipht]+ word)
        elif letters.endswith('_'):
            word = self.__split(letters[:-1], word)
        elif letters.endswith(digraph):
            word = self.__split(letters[:-2], [letters[-2:]] + word)
        elif letters:
            word = self.__split(letters[:-1], [letters[-1]]+ word)
        return word

    def __join(self, letters):
        indivisible_onset = ('pl', 'bl', 'fl', 'cl', 'kl', 'gl', 'll',
                             'pr', 'br', 'fr', 'cr', 'kr', 'gr', 'rr',
                             'dr', 'tr', 'ch', 'dh', 'rh', 'th',
                             'βl', 'ɣl',
                             'βɾ', 'pɾ', 'fɾ', 'kɾ', 'gɾ', 'ɣɾ', 'dɾ', 'ðɾ',
                             'tɾ', 'bɾ', 'tʃ', 'gw', 'ɣw')
        indivisible_coda = ('ns', 'bs', 'nz', 'βs', 'bz', 'βz', 'nd', 'rt',
                            'st', 'ff', 'ls', 'zz', 'll', 'nt', 'rs', 'ɾs',
                            'ch', 'nk', 'nc', 'lk', 'sh', 'nt')
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
                if onset.endswith('y'):
                    if onset == 'y' and word[-1][-1] in 'AOEÁÓÉaoeáóé':
                        word[-1] += onset
                    else:
                        word += [onset]
                    onset = letter
                else:
                    onset += letter
                    if len(word) > 0:
                        media = len(onset) // 2
            elif len(onset) <= 1 or len(word) == 0:
                word += [onset+letter]
                onset = ''
            elif onset.endswith(indivisible_onset):
                if len(word) > 0:
                    word[-1] += onset[:-2]
                    word += [onset[-2:] + letter]
                else:
                    word += [onset + letter]
                onset = ''
            elif onset.startswith(indivisible_coda) and (len(onset) > 2):
                word[-1] = word[-1] + onset[:2]
                word = word + [onset[2:] + letter]
                onset = ''
            elif (onset[-1] in 'dðfkt' and
                  onset[-2] in 'bβcθkdðfgɣkmɱɲñpqstvwxχz' + symbols
                  or onset[-1] in 'gɣ' and onset[-2] in 'cθtk' + symbols
                  or onset[-1] in 'lmɱ' and onset[-2] in 'mɱl'
                  or onset[-1] in 'cθ' and onset[-2] in 'kc'):
                word[-1] = word[-1] + onset[:-1]
                word = word + [onset[-1] + letter]
                onset = ''
            else:
                word[-1] = word[-1] + onset[:media]
                word = word + [onset[media:] + letter]
                onset = ''
        word[-1] = word[-1] + onset
        return word


def stressed_s(slbs):
    if len(slbs) == 1:
        stress = -1
    elif any(k in 'áéíóúÁÉÍÓÚ' for k in ''.join(slbs)):
        for x in  range(-len(slbs), 0, 1):
            if any(k in 'áéíóúÁÉÍÓÚ' for k in slbs[x]):
                stress = x
                break
    elif slbs[-1][-1] in 'aeiouAEIOUy':
        stress = -2
    elif slbs[-1][-1] in 'nsNS' and slbs[-1][-2] in 'aeiouAEIOU':
        stress = -2
    else:
        stress = -1
    return stress


def syllabify(word, exceptions=True):
    return Syllabification(word, exceptions).syllables


def tonica(word, exceptions=True):
    return Syllabification(word, exceptions).stress
