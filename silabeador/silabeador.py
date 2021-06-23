#!/usr/bin/env python3 import re
import re


def silabea(word):
    return silabas(word).silabas


def tonica(word):
    return silabas(word).tonica


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
    vocales = ['a', 'e', 'i', 'o', 'u',
               'á', 'é', 'í', 'ó', 'ú',
               'ä', 'ë', 'ï', 'ö', 'ü']

    def __init__(self, palabra):
        self.palabra = palabra
        self.silabas = self.__silabea(self.palabra)
        self.tonica = tonica_s(self.silabas)

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
        return slbs

    def __une(self, letras):
        cerradas = ['i', 'u']
        debiles = ['e', 'i', 'é', 'í']
        hiatos = ['ú', 'í']
        dieresis = ['ä', 'ë', 'ï', 'ö', 'ü']
        lista = []
        for letra in letras:
            if len(lista) == 0:
                lista = [letra]
            elif (letra.lower() in self.vocales and
                  lista[-1][-1].lower() in self.vocales) and (
                      (not any(y.lower() in hiatos
                               for y in (lista[-1][-1], letra)) and
                       any(y.lower() in cerradas for y in
                           (lista[-1][-1], letra)) and
                       not any(y.lower() in dieresis for
                               y in (lista[-1][-1], letra))) or
                      (letra in debiles and
                          ''.join(lista).lower().endswith('gü'))) or (
                                  ''.join(lista).lower().endswith('qu')):
                lista[-1] = lista[-1] + letra
            else:
                lista = lista + [letra]
        return lista

    def __separa(self, letras):
        inseparables_onset = ['pl', 'bl', 'fl', 'cl', 'kl', 'gl', 'll',
                              'pr', 'br', 'fr', 'cr', 'kr', 'gr', 'rr',
                              'tr', 'ch']
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
                    lista[-1] = lista[-1] + onset[:media]
                    lista = lista + [onset[media:] + letra]
                    onset = ''
            lista[-1] = lista[-1] + onset
        return lista
