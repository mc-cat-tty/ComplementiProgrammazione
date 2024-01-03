"""
Contare la frequenza con cui compare ogni lettara in una stringa
"""
from functools import reduce

initial_str = "abba a doggo"

# Attenzione: non puoi modificare il valore di d nella lambda (funzione pura)

res = reduce(
  lambda d, c: d | {c: d.get(c, 0)+1},
  initial_str,
  dict()
)

print(res)