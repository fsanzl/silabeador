<h2 align="center">Silabeador</h2>
<h3 align="center">Una librería de Python para la división silábica y detección de acentos</h2>


*silabeador* es una librería de métodos y funciones para la la división silábica palabras y localización de acentos prosódicos.

La librería surge para facilitar la división silábica para la escansión métrica de versos del Siglo de Oro, independientemente de si se reconocen como españolas. Esto es, debe ser capaz de tratar caracteres propios de otras lenguas como el italiano, el francés o el portugués, tales como 'à' u 'õ', así como grupos consonánticos ajenos al español, pero comunes en esas lenguas o el latín, p.ej. 'stella'.   


[Instalación](#Instalación)
[Uso](#Uso)
[Descripción](#Descripción)
[Problemas](#Problemas)
[Licencia](#Licencia)

## Instalación

## Uso

La librería provee funciones y métodos que pueden ser llamados de forma independiente.:

```python
>>> import silabeador
```

La función para dividir en sílabas una palabra acepta una cadena de caracteres como argumento y devuelve una lista de sílabas.
```
>>> silabeador.silabea('Uvulopalatofaringoplastia')
['U', 'vu', 'lo', 'pa', 'la', 'to', 'fa', 'rin', 'go', 'plas', 'tia']
```

La función para recuperar el índice de la sílaba tónica acepta como argumento una cadena de caracteres y devuelve el índice de la sílaba tónica en la lista de sílabas.

```
>>> silabeador.tonica('Uvulopalatofaringoplastia')
-2
```

Alternativamente, puede crearse un objeto con los mismo valores:

```
>>> objeto_silabas = silabeador.silabas('Uvulopalatofaringoplastia')
>>> objeto_silabas.silabas
['Ui', 'vu', 'lo', 'pa', 'la', 'to', 'fa', 'rin', 'go', 'plas', 'tia']
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
