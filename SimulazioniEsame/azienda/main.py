from typing import NoReturn
from repl import REPL
from model import Model

def main() -> NoReturn:
  model = Model()
  cli = REPL(model)

  while True:
    cli.loop_async()

if __name__ == "__main__":
  main()