from user import *
from operation import *

class Model:
  """
  In-memory user database; defines helper functions to manage users and their operations
  """
  last_uid = 0
  last_oid = 100

  def __init__(self):
    self.__users = dict()  # Users indexed by user id
  
  @property
  def last_user_id(self):
    Model.last_uid += 1
    return Model.last_uid

  @property
  def last_operation_id(self):
    Model.last_oid += 1
    return Model.last_oid

  def add_user(self, u: User):
    u.id = self.last_user_id
    self.__users |= {u.id: u}
    return u.id

  def get_user(self, uid: int):
    return self.__users[uid]
  
  @property
  def users(self) -> List[User]:
    return sorted(self.__users.values(), key=lambda u: u.id)