if __name__ == "__main__":
  m = []
  with open("matrix.txt", "r") as f:
    [m.append(list(map(int, l.split()))) for l in f]
  print(m)
  print(m[0][1] * m[2][2])