from user import *
from request import *
from operator import itemgetter

class Model:
  """
  Users and requests in-memory database that exposes helper methods to interact with the user-base
  """
  last_uid = 0
  last_rid = 100

  def __init__(self):
    self.__users = dict()
    self.requests = list()

  @property
  def users(self):
    return self.__users.values()
  
  def add(self, user: User):
    if user.role == Role.SUBORDINATE and user.director not in self.__users:
      raise KeyError("Director does not exists")
    
    Model.last_uid += 1
    user.id = Model.last_uid
    self.__users |= {user.id: user}
    return user.id
  
  def get(self, uid: int):
    if uid not in self.__users:
      raise KeyError("User does not exists")

    return self.__users[uid]

  def get_total_pay(self, uid: int):
    user = self.get(uid)
    ar = self.get_accepted_requests(uid)
    return sum(map(lambda r: r.hours, ar)) * user.salary
  
  def request_payment(self, uid: int, hours: int):
    self.requests.append(Request(Model.last_rid, uid, State.PENDING, hours))
    Model.last_rid += 1

  def get_requests(self, uid: int):
    if self.__users[uid].role == Role.SUBORDINATE:
      res = [*filter(lambda r: r.uid == uid, self.requests)]
    else:
      res = [*filter(lambda r: self.__users[r.uid].director == uid, self.requests)]
    if not res: raise KeyError("User has no requests")
    return res
  
  def get_request(self, rid: int):
    return next(filter(lambda r: r.id == rid, self.requests))

  def get_accepted_requests(self, uid: int):
    res = [*filter(lambda r: r.uid == uid and r.state == State.ACCEPTED, self.requests)]
    if not res: raise KeyError("User has no accepted requests")
    return res
  
  def __repr__(self):
    return repr(self.__users) + '\n' + repr(self.requests)