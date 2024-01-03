import pickle

if __name__ == "__main__":
  with open("matrix.bin", "rb") as f:
    m = pickle.load(f)

  print(m)
  print(m[0][1] * m[2][2])