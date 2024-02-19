from ctypes import *

if __name__ == '__main__':
  lib = CDLL('fast_functions.so')
  print(lib.double_square(10))