from dataclasses import dataclass, field
from typing import List
from chat import Chat

@dataclass
class User:
  uid: int = -1
  name: str = ""
  chats: List[Chat] = field(default_factory=list)

  def __str__(self):
    return f"{self.uid}.\t{self.name}"

  @staticmethod
  def get_header():
    return "USER ID\tNAME"