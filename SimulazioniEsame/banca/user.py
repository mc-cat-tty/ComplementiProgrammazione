from operation import *
from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
  id: int = -1
  name: str = ""
  surname: str = ""
  operations: List[Operation] = field(default_factory=list)

  def __str__(self) -> str:
    return f"{self.id}.\t{self.name}\t{self.surname}"

  @staticmethod
  def get_header():
    return "ID\tNAME\tSURNAME"

  def add_op(self, op: Operation):
    self.operations.append(op)
