from dataclasses import dataclass

@dataclass
class User:
  """
  User representation. UID must be unique.
  """
  uid: int = -1
  name: str = -1

  @staticmethod
  def get_header() -> str:
    return "USER ID\tNAME"

  def __str__(self) -> str:
    return f"{self.uid}.\t{self.name}"
