import struct

M = [
  [1, 2, 3],
  [10, 20, 30],
  [100, 200, 300]
]

if __name__ == "__main__":
  with open("matrix.bin", "wb") as f:
    f.write(struct.pack('i', len(M)))
    f.write(struct.pack('i', len(M[0])))
    [f.write(struct.pack('f', e)) for l in M for e in l]