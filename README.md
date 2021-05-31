<h2 align="center">Silabeador</h2>
<h3 align="center">Una librería de Python para la división silábica y detección de acentos</h2>


*silabeador* es una librería de métodos y funciones para la la división silábica palabras y localización de acentos prosódicos.

La librería surge en el marco del proyecto de investigación [Sound and Meaning in Spanish Golden Age Literature](https://soundandmeaning.univie.ac.at/). Para la escansión automática de versos se requería un separador silábico tolerante a grupos consonánticos ajenos al español y diacríticos poco comunes o extranjeros. Otras librerías disponibles asumen que la entrada es una palabra bien construida de acuerdo a las reglas del español, lo que no siempre es el caso en determinado tipo de textos, que puede incluir vocales con diacríticos de otras lenguas, tales como *`* u *~*, caracteres en desuso, como *ç*, o usados pero con implicaciones en la división silábica en contextos específicos, como en *ü* en su uso habitual o como diacrítico métrico (p.ej., *Si-güen-za* y *crü-el*).

## Instalación

```bash
pip3 install silabeador
```

## Uso

La librería provee funciones y métodos que pueden ser llamados de forma independiente.:

```python
>>> import silabeador
```

La función para dividir en sílabas una palabra acepta una cadena de caracteres como argumento y devuelve una lista de sílabas.

```python
>>> silabeador.silabea('Uvulopalatofaringoplastia')
['U', 'vu', 'lo', 'pa', 'la', 'to', 'fa', 'rin', 'go', 'plas', 'tia']
```

La función para recuperar el índice de la sílaba tónica acepta como argumento una cadena de caracteres y devuelve el índice de la sílaba tónica en la lista de sílabas.


```python
>>> silabeador.tonica('Uvulopalatofaringoplastia')
-2
```

Una versión alternativa acepta una lista de sílabas y devuelve el índice de la sílaba tónica.

```python
>>> silabeador.tonica_s(['U', 'vu', 'lo', 'pa', 'la', 'to', 'fa', 'rin', 'go', 'plas', 'tia'])
-2
```

También puede crearse un objeto con los mismo valores:

```python
>>> objeto_silabas = silabeador.silabas('Uvulopalatofaringoplastia')
>>> objeto_silabas.palabra
'Uvulopalatofaringoplastia'
>>> objeto_silabas.silabas
['U', 'vu', 'lo', 'pa', 'la', 'to', 'fa', 'rin', 'go', 'plas', 'tia']
>>> objeto_silabas.tonica
-2
``` 

## Descripción

### Silabificación

La división silábica se efectúa siguiendo los principios descritos por (1984/2013, p. 47-49)
Primero se identifican los núcleos silábicos a partir de las vocales. En caso de vocales cerradas no acentuadas, se unen a las vocales adyacentes constituyendo diptongos o triptongos. Las cerradas acentuadas se consideran como núcleos silábicos independientes. Las consonates adyacentes se unen en un solo grupo.

Después se dividen los grupos consonánticos según sus componentes sean separables o inseparables y se añaden a los núcleos silábicos adyacentes  en coda u onset según corresponda.



### Acento prosódico
La detección del acento prosódico según las reglas de acentuación ortográfica del español. Las palabras proparoxítonas siempre lleván acento gráfico en la antepenúltima sílaba. Las paroxitonas no llevan acento gráfico salvo que la palabra no acabe en n, s o vocal, en cuyo caso lo llevabn en la penúltima sílaba. Las oxítonas no llevan acento gráfico salvo que acaben en n, s, o vocal, en cuyo caso lo llevan en la última sílaba.

## Problemas

Para preguntas, reportar errores o suerir nuevas características, use  [GitHub Issue Tracker](https://github.com/fsanzl/silabeador/issues). Antes de crear una nueva entrada, por favor, asegúrese de buscar entradas existentes similares.


## Licencia

Silabeador se halla bajo licencia GNU LGPL 2.1. Ver archivo [LICENSE](https://github.com/fsanzl/silabeador/LICENSE) para más detalles.

## Referencias
Quilis, A. (1996). *Métrica española*. Barcelona: Ariel. Publicado originalmente en 1984.
