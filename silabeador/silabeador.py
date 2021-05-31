#!/usr/bin/env python3 import re
import re

def silabea(palabra):
    return silabas(palabra).silabas

def tonica(palabra):
    return silabas(palabra).tonica

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
                       'ã': 'a', 'ẽ': 'e', 'ĩ': 'i', 'õ': 'o', 'ũ': 'u'}
        diccionario = {'b': 'be', 'c': 'ce', 'd': 'de', 'f': 'efe', 'g': 'ge',
                       'h': 'hache', 'j': 'jota', 'k': 'ka', 'l': 'ele',
                       'm': 'eme', 'n': 'ene', 'p': 'pe', 'q': 'qu',
                       'r': 'erre', 's': 'ese', 't': 'te', 'v': 'uve',
                       'w': 'uvedoble', 'x': 'equis', 'y': 'igriega',
                       'z': 'zeta'}
        slbs = []
        palabra = re.sub(r'\W', '', letras)
        if palabra.lower() in diccionario:
            palabra = diccionario[palabra]
        palabra = ''.join([letra if letra not in extranjeras
                           else extranjeras[letra] for letra in letras])
        slbs[:0] = palabra
        slbs = self.__une(slbs)
        slbs = self.__separa(slbs)
        return slbs

    def __une(self, letras):
        cerradas = ['i', 'u']
        hiatos = ['í', 'ú']
        lista = []
        for letra in letras:
            if len(lista) == 0:
                lista = [letra]
            elif letra.lower() in self.vocales:
                if lista[-1][-1].lower() in self.vocales and (
                    not any(y.lower() in hiatos
                            for y in (lista[-1][-1], letra)) and
                    any(y.lower() in cerradas
                        for y in [letra, lista[-1][-1]])):
                    lista[-1] = lista[-1] + letra
                elif lista[-1] == 'ü' and lista[-2] == 'g':
                    lista[-1] = lista[-1] + letra
                else:
                    lista = lista + [letra]
            elif lista[-1][-1].lower() not in self.vocales:
                lista[-1] = lista[-1] + letra
            else:
                lista = lista + [letra]
        return lista

    def __separa(self, letras):
        inseparables_onset = ['pl', 'bl', 'fl', 'cl', 'kl', 'll',
                              'pr', 'br', 'fr', 'cr', 'kr', 'rr', 'tr', 'ch']
        inseparables_coda = ['ns', 'bs']
        lista = []
        onset = ''
        for letra in letras:
            if all(x.lower() not in self.vocales for x in letra):
                if len(lista) == 0:
                    onset = letra
                elif len(letra) == 1:
                    onset = letra
                elif len(letra) == 2:
                    if letra in inseparables_onset:
                        onset = letra
                    elif letra in inseparables_coda and lista[-1][-a] == 'a':
                        lista[-1] = lista[-1] + letra
                    else:
                        lista[-1] = lista[-1] + letra[0]
                        onset = letra[1]
                elif any(letra.endswith(x) for x in inseparables_onset):
                    onset = letra[-2:]
                    lista[-1] = lista[-1] + letra[:-2]
                elif any(letra.startswith(x) for x in inseparables_coda):
                    lista[-1] = lista[-1] + letra[:2]
                    onset = letra[2:]
            else:
                lista = lista + [onset+letra]
                onset = ''
        lista[-1] = lista[-1] + onset
        return lista
