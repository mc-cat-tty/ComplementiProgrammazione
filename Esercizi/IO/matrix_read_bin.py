import struct

if __name__ == "__main__":
  with open("matrix.bin", "rb") as f:
    bytes = f.read()
    (rows,) = struct.unpack('i', bytes[:4])
    (cols,) = struct.unpack('i', bytes[4:8])
    Mb = struct.unpack(f'{(len(bytes)-8) // 4}f', bytes[8:])
    M = [list(Mb[i*(cols):(i+1)*(cols)]) for i in range(rows)]

  print(M)
  print(M[0][1] * M[2][2])