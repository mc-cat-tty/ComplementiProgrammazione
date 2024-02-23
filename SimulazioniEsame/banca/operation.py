from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import argparse
from pickle import load

class OperationType(Enum): DEPOSIT = "versamento"; WITHDRAW = "prelievo"

@dataclass
class Operation:
  id: int
  amount: float
  date: datetime
  type: OperationType

  def __str__(self):
    return f"{self.id}.\t{self.amount}\t{datetime.strftime(self.date, '%d-%m-%Y')}\t{self.type.value}"

  @staticmethod
  def get_header():
    return "ID\tAMOUNT\tDATE\tTYPE"

def main() -> None:
  p = argparse.ArgumentParser(description="Convert binary opreations between two dates into a textual representation")
  p.add_argument('-b', '--backup-filename', help='Binary backup input filename', required=True)
  p.add_argument('-t', '--textual-filename', help='Textual backup output filename', required=True)
  p.add_argument('-s', '--start-date', help='Start date in %dd-%mm-%YYYY format', required=True)
  p.add_argument('-e', '--end-date', help='End date in %dd-%mm-%YYYY format', required=True)
  args = p.parse_args()

  sd = datetime.strptime(args.start_date, "%d-%m-%Y")
  ed = datetime.strptime(args.end_date, "%d-%m-%Y")

  with open(args.backup_filename, 'rb') as fd:
    model = load(fd)

  with open(args.textual_filename, 'w') as fd:
    for u in model.users:
      print(u, file = fd)
      filtered_ops = filter(lambda o: o.date >= sd and o.date <= ed, u.operations)
      print(*filtered_ops, sep = '\n', file = fd)
      print(file = fd)

if __name__ == '__main__':
  main()