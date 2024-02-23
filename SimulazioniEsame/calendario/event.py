"""
Event definition module. Launch it standalone to extract text informations from binary backup.
"""
from typing import List
from datetime import datetime
from dataclasses import dataclass, field
from typing import List
from user import User
import config
import argparse
from pickle import load
import sys

@dataclass
class Event:
  """
  Event ('appuntamento') representation. EID must be unique.
  """
  eid: int = -1
  name: str = ""
  date: datetime = None
  owner: User = None
  guests: List[User] = field(default_factory=list)

  @staticmethod
  def get_header() -> str:
    return "EVENT ID\tNAME\t\tDATE\t\tOWNER\t\tGUESTS"
  
  def __str__(self) -> str:
    guests_name = map(lambda u: u.name, self.guests)
    return f"{self.eid}.\t\t{self.name}\t{datetime.strftime(self.date, config.DATE_FORMAT)}\t{self.owner.name}\t{list(guests_name)}"
  

def main() -> None:
  p = argparse.ArgumentParser(description="Utility module to extract textual data from binary backup.")
  p.add_argument('-b', '--backup-filename', help='Binary backup input filename', required=True)
  p.add_argument('-t', '--textual-filename', help='Textual backup output filename', required=True)
  p.add_argument('-u', '--user-id', help='User ID', required=True, type=int)
  p.add_argument('-d', '--day', help='Day of the event in dd-mm-YYYY format', required=True)
  args = p.parse_args()

  with open(args.backup_filename, 'rb') as fd:
    model = load(fd)
  
  try:
    events = model.get_user_events(args.user_id)
  except KeyError:
    print("User doesn't exist")
    sys.exit(1)
  
  try:
    day = datetime.strptime(args.day, config.DATE_FORMAT)
  except:
    print("Wrong format for day")
    sys.exit(2)
  
  events = list(
    filter(
      lambda e: e.date == day,
      events
    )
  )

  with open(args.textual_filename, 'w') as fd:
    if not events:
      print("No events for selected user and day")
    else:
      print(Event.get_header(), file=fd)
      print(*events, sep='\n', file=fd)
      print("Done!")

if __name__ == '__main__':
  main()