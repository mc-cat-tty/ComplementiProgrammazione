M = [
  [1, 2, 3],
  [10, 20, 30],
  [100, 200, 300]
]

if __name__ == "__main__":
  with open("matrix.txt", "w") as f:
    [print(*l, file=f, sep=" ") for l in M]