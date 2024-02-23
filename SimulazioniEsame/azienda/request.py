from enum import Enum, auto
from dataclasses import dataclass
import argparse
from pickle import load

class State(Enum): PENDING = auto(); ACCEPTED = auto(); DENIED = auto()

@dataclass
class Request:
  id: int
  uid: int
  state: State
  hours: int

  def __str__(self):
    return f"{self.id}. {self.hours}h {self.state.name.lower()}"
  
def main() -> None:
  p = argparse.ArgumentParser(description="Convert binary requests into a textual representation")
  p.add_argument('-b', '--backup-filename', help='Binary backup input filename', required=True)
  p.add_argument('-t', '--textual-filename', help='Textual backup output filename', required=True)
  p.add_argument('-u', '--user-id', help='User id', required=True)
  args = p.parse_args()
  with open(args.backup_filename, 'rb') as fd:
    model = load(fd)
  with open(args.textual_filename, 'w') as fd:
    print(repr(model.requests), file = fd)

if __name__ == '__main__':
  main()