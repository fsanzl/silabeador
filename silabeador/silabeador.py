#!/usr/bin/env python3
import re
from sys import prefix


def silabea(word, excepciones=True):
    return silabas(word, excepciones).silabas


def tonica(word, excepciones=True):
    return silabas(word, excepciones).tonica


def tonica_s(slbs):
    if len(slbs) == 1:
        tonica = -1
    elif len(slbs) > 2 and any(k in 'áéíóúÁÉÍÓÚ' for k in slbs[-3]):
        tonica = -3
    else:
        if any(k in 'áéíóúÁÉÍÓÚ' for k in slbs[-2]):
            tonica = -2
        elif any(k in 'áéíóúÁÉÍÓÚ' for k in slbs[-1]):
            tonica = -1
        else:
            if (slbs[-1][-1] in 'nsNS' or
                    slbs[-1][-1] in 'aeiouAEIOU'):
                tonica = -2
            else:
                tonica = -1
    return tonica


class silabas:
    vocales = 'aeiouáéíóúäëïöüàèìòùAEIOUÁÉÍÓÚÄËÏÓÜÀÈÌÒÙ'

    def __init__(self, palabra, excepciones=True):
        self.palabra = self.__excepciones(palabra, excepciones)
        self.excepcions = excepciones
        self.silabas = self.__silabea(self.palabra)
        self.tonica = tonica_s(self.silabas)

    def __excepciones(self, palabra, excepciones):
        if excepciones:
            import importlib.resources as pkg_resources
            lineas = pkg_resources.read_text('silabeador', 'excepciones.lst')
            nombres = lineas.splitlines()
            nombres = [nombre.strip()
                       for nombre in nombres if not nombre.startswith('#')]
        else:
            nombres = []
        uir = ['uir', 'uido', 'uida', 'uid', 'uidos', 'uidas'
               'uimos',
               'uiste', 'uisteis',  'uido', 'uida', 'uid'
               'uiré', 'uirás', 'uirá', 'uiremos', 'uiréis', 'uirán',
               'uiría', 'uirías', 'uiría', 'uiríamos', 'uiríais', 'uirían']

        uar = ['uar', 'uado', 'uada', 'uad', 'uás', 'uados', 'uadas'
               'uamos', 'uáis',
               'uaba', 'uabas', 'uábamos', 'uabais', 'uaban',
               'uaste', 'uó', 'uamos', 'uasteis', 'uaron',
               'uaré', 'uarás', 'uará', 'uaremos', 'uaréis', 'uarán',
               'uaría', 'uarías', 'uaría', 'uaríamos', 'uaríais', 'uarían']
        acui = 'acuí'
        excepto = ['g', 'c']
        uoso = ['uoso', 'uosa', 'uosos', 'uosas']
        if (any(x in palabra for x in nombres) or
            any(palabra.endswith(x) for x in nombres) or
            any(palabra.endswith(x) for x in uir if len(x)+2 <= len(palabra))
            or any(palabra.endswith(x) for x in uar
                   if not palabra.endswith(f'g{x}'))):
            palabra = re.sub('i([aeouáéó])', r'i \1', palabra)
            if not any(x in palabra for x in ['gu', 'qu', 'cu']):
                palabra = re.sub('u([aeioáéó])', r'u \1', palabra)
        return palabra

    def __silabea(self, letras):
        extranjeras = {'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
                       'ã': 'a', 'ẽ': 'e', 'ĩ': 'i', 'õ': 'o', 'ũ': 'u',
                       'ﬁ': 'fi', 'ﬂ': 'fl'}
        diccionario = {'b': 'be', 'c': 'ce', 'd': 'de', 'f': 'efe', 'g': 'ge',
                       'h': 'hache', 'j': 'jota', 'k': 'ka', 'l': 'ele',
                       'm': 'eme', 'n': 'ene', 'p': 'pe', 'q': 'qu',
                       'r': 'erre', 's': 'ese', 't': 'te', 'v': 'uve',
                       'w': 'uvedoble', 'x': 'equis',
                       'z': 'zeta', 'ph': 'pehache'}
        slbs = []
        palabra = re.sub(r'\W', '', letras)
        palabra = ''.join([letra if letra not in extranjeras
                           else extranjeras[letra] for letra in letras])
        if palabra.lower() in diccionario:
            palabra = diccionario[palabra]
        slbs[:0] = palabra
        slbs = self.__une(slbs)
        slbs = self.__separa(slbs)
        return [x.strip() for x in slbs]

    def __une(self, letras):
        cerradas = 'iuIU'
        debiles = 'eiéí'
        hiatos = 'úíÚÍ'
        dieresis = 'äëïöüÄËÏÖÜ'
        lista = []
        for letra in letras:
            if len(lista) == 0:
                lista = [letra]
            elif all(vocal in self.vocales
                     for vocal in [letra, ultima]):
                if letra in debiles and any(''.join(lista).lower().endswith(x)
                                            for x in ['gü', 'qu', 'gu']):
                    lista[-1] = lista[-1] + letra
                elif any(vocal in cerradas for vocal in letra + ultima):
                    print(lista, letra)
                    if letra not in hiatos+dieresis and ultima not in dieresis:
                        lista[-1] = lista[-1] + letra
                    elif letra == 'í' and len(lista) > 1 and (
                        lista[-2:] == ['c','u']):
                        lista[-1] = lista[-1] + letra
                    else:
                        lista = lista + [letra]
                else:
                    lista = lista + [letra]
            else:
                lista = lista + [letra]
            ultima = lista[-1][-1]
        return lista

    def __separa(self, letras):
        inseparables_onset = ['pl', 'bl', 'fl', 'cl', 'kl', 'gl', 'll',
                              'pr', 'br', 'fr', 'cr', 'kr', 'gr', 'rr',
                              'dr', 'tr', 'ch', 'dh', 'rh']
        inseparables_coda = ['ns', 'bs']
        lista = []
        onset = ''
        if len(letras) == 1:
            lista = letras
        else:
            for letra in letras:
                if all(x.lower() not in self.vocales for x in letra):
                    if len(lista) == 0:
                        onset = onset + letra
                    else:
                        onset = onset + letra
                        media = len(onset) // 2
                elif len(onset) <= 1 or len(lista) == 0:
                    lista = lista + [onset+letra]
                    onset = ''
                elif any(onset.endswith(x) for x in inseparables_onset):
                    if len(lista) > 0:
                        lista[-1] = lista[-1] + onset[:-2]
                        lista = lista + [onset[-2:] + letra]
                    else:
                        lista = lista + [onset + letra]
                    onset = ''
                elif any(onset.startswith(x) for x in inseparables_coda) and (
                        len(onset) > 2):
                    lista[-1] = lista[-1] + onset[:2]
                    lista = lista + [onset[2:] + letra]
                    onset = ''
                else:
                    if (onset[-1] in 'dfkt' and onset[-2] in 'bcdfgjkm' +
                        'ñpqstvwxz'
                        or onset[-1] in 'g' and onset[-2] in 'ctjk'
                        or onset[-1] in 'lm' and onset[-2] in 'ml'
                            or onset[-1] == 'c' and onset[-2] == 'c'):
                        lista[-1] = lista[-1] + onset[:-1]
                        lista = lista + [onset[-1] + letra]
                    else:
                        lista[-1] = lista[-1] + onset[:media]
                        lista = lista + [onset[media:] + letra]
                    onset = ''
            lista[-1] = lista[-1] + onset
        return lista
