"""
Contare la frequenza con cui compare ogni lettera in 10
stringhe molto lunghe, usando il paradigma map-reduce
"""
from functools import reduce, partial

initial_strings = ["abba a doggo", "dogga fresca", "lorem ipsum"]

# Attenzione: non puoi modificare il valore di d nella lambda (funzione pura)

res = reduce( 
  lambda x, y: {k: x.get(k, 0) + y.get(k, 0) for k in x.keys() | y.keys()},
  map(
    partial(lambda f, i, s: reduce(f, s, i), lambda d, c: d | {c: d.get(c, 0)+1}, dict()),
    initial_strings
  ),
  dict()
)

print(res)