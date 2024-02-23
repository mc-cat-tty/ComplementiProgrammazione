from dataclasses import dataclass
from typing import List
import argparse
from pickle import load
import sys

@dataclass
class Message:
  sndr: str
  sndrid: int
  msg: str

  def __str__(self):
    return f"{self.sndr}: {self.msg}"

  @staticmethod
  def get_header():
    return "SENDER: MESSAGE"

@dataclass
class Chat:
  cid: int
  u1: str
  uid1: int
  u2: str
  uid2: str
  msgs: List[Message]

  def __str__(self):
    return f"{self.cid}.\t[{self.uid1}]\t\t{self.u1}\t[{self.uid2}]\t\t{self.u2}"

  @staticmethod
  def get_header():
    return "CHAT ID\t[USER ID 1]\tUSER 1\t[USER ID 2]\tUSER 2"
  
def main() -> None:
  p = argparse.ArgumentParser(description="Utility module to export a textual chat from its binary backup")
  p.add_argument('-b', '--backup-filename', help='Binary backup input filename', required=True)
  p.add_argument('-t', '--textual-filename', help='Textual backup output filename', required=True)
  p.add_argument('-c', '--chat-id', help='Textual backup output filename', required=True, type=int)
  args = p.parse_args()

  with open(args.backup_filename, 'rb') as fd:
    user = load(fd)
  
  chats = user.chats
  cid = args.chat_id
  try:
    chat = next(filter(lambda c: c.cid == cid, chats))
  except StopIteration:
    print("Specified chat ID doesn't exist")
    sys.exit(1)

  with open(args.textual_filename, 'w') as fd:
    print(Chat.get_header(), file=fd)
    print(chat, file=fd)

if __name__ == '__main__':
  main()