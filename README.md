[![License: LGPL](https://img.shields.io/github/license/fsanzl/silabeador)](https://opensource.org/licenses/LGPL-2.1)
[![Version: 1.0.2-15](https://img.shields.io/github/v/tag/fsanzl/silabeador)](https://pypi.org/project/silabeador/)
[![Python versions: 3.5, 3.6, 3.7, 3.8, 3.9](https://img.shields.io/pypi/pyversions/silabeador)](https://pypi.org/project/silabeador/)


<h2 align="center">Silabeador</h2>
<h3 align="center">A Python library for syllabic division and stress detection for Spanish</h2>


*silabeador* is a Python library of methods and functions for syllabic division and prosodic stress detecting for Spanish.

This library is part of the research project [Sound and Meaning in Spanish Golden Age Literature](https://soundandmeaning.univie.ac.at/). Automatic verse scansion required a syllable separator tolerant to non-Spanish consonant clusters and unusual and non-Spanish diacritics. Other libraries available take for granted that the words are well-constructed according to the Spanish grammar. This is not always the case in particular text types, as in *ü* as regularly used or as a metric diacritic (e.g., *Si-güen-za* vs *crü-el*).

## Instalation

```bash
pip3 install silabeador
```

## Use

The library provides functions and methods that can be called idependently:


```python
>>> import silabeador
```

The syllabic division function accepts a string as a single argument and returns a list of syllables

```python
>>> silabeador.silabea('Uvulopalatofaringoplastia')
['U', 'vu', 'lo', 'pa', 'la', 'to', 'fa', 'rin', 'go', 'plas', 'tia']
```

The function to recover the stressed syllable's index takes a string as s single argument and returns the stressed syllable's index.

```python
>>> silabeador.tonica('Uvulopalatofaringoplastia')
-2
```

An alternative version accepts a list of syllables and returns the stressed syllable's index.

```python
>>> silabeador.tonica_s(['U', 'vu', 'lo', 'pa', 'la', 'to', 'fa', 'rin', 'go', 'plas', 'tia'])
-2
```

An object with those values can also be created:

```python
>>> objeto_silabas = silabeador.silabas('Uvulopalatofaringoplastia')
>>> objeto_silabas.palabra
'Uvulopalatofaringoplastia'
>>> objeto_silabas.silabas
['U', 'vu', 'lo', 'pa', 'la', 'to', 'fa', 'rin', 'go', 'plas', 'tia']
>>> objeto_silabas.tonica
-2
``` 

## Description

### Sillabification

The syllabic division follows the principles described by Quilis (1984/2013, p. 47-49).

Firstly, syllabic nuclei are detected looking for the vowels. Unstressed close vowels join the adjacent vowels in coda or onset to form a diphthong or a triphthong, whilst stressed ones are considered standalone syllabic nuclei. Contiguous consonants are grouped to be parsed apart.

Secondly, consonant clusters are divided considering whether their components are separable and joined to the neighbour nuclei in coda or onset accordingly. 


### Prosodic stress

Prosodic stress detection follows the Spanish rules. Proparoxytone words are always orthographically signalled with an acute accent on the nucleic vowel of the antepenultimate syllable. Paroxytones are not marked unless the word ends with *n*, *s* or vowel, in which case they have an acute accent on the nucleic vowel of the penultimate syllable. Oxytone words are only marked if they end in *n*, *s* or vowel with an acute accent on the nucleic vowel of the last syllable. 

## Known problems

Adverbs in *-mente* have primary and secondary stress. Therefore, they must be divided, and each of their parts parsed  independently.


## Contributions

Feel free to contribute using the [GitHub Issue Tracker](https://github.com/fsanzl/silabeador/issues) for feedback, suggestions, or bug reports.


## Licence

This project is under GNU LGPL 2.1 See [LICENSE](https://github.com/fsanzl/silabeador/LICENSE) for details.

## References

Quilis, Antonio, *Métrica española*. 1984. Barcelona, Ariel, 1996.
