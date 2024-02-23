from enum import Enum, auto
from dataclasses import dataclass

class Role(Enum): SUBORDINATE = auto(); DIRECTOR = auto()

@dataclass
class User:
  id: int = 0
  name: str = ''
  salary: float = 0.0
  role: Role = Role.SUBORDINATE
  director: int | None = -1

  def __str__(self):
    return f"{self.id}. {self.name}"
  