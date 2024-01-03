"""
Partendo da una stringa molto lunga di caratteri minuscoli scrivere un
programma che tenga conto solo delle consonanti e le renda maiuscole
"""

import string
from functools import reduce

VOWELS = {'a', 'e', 'i', 'o', 'u'}
CONSONANTS = {c for c in string.ascii_lowercase if c not in VOWELS}

chars = "ZAZabadgdafydstyoiASDGVuiouhrt?!o.,ertsdr"
res = reduce(
  str.__add__,
  map(
    str.upper,
    filter(
      CONSONANTS.__contains__,
      chars
    )
  )
)
print(res)