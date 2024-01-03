"""
Scrivere una calcolatrice che permetta di valutare espressione
mediante la funzione built-in eval()
"""

print("Espressione:", end=" ")
expr = input()

while (expr):
  print(eval(expr))
  print("Espressione:", end=" ")
  expr = input()