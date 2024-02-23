"""
Application entry-point. Launch this module to get an interactive CLI system.
@author Francesco Mecatti.
"""

from typing import NoReturn
from repl import REPL
from model import Model
import signal, sys

def goodbye(signum, _):
  print("Goodbye!")
  sys.exit(0)

def main() -> NoReturn:
  signal.signal(signal.SIGINT, goodbye)
  model = Model()
  cli = REPL(model)

  while True:
    cli.loop_async()

if __name__ == "__main__":
  main()