from typing import Dict, List
from datetime import datetime
from user import User
from event import Event

class Model:
  """
  In-memory representation of a system for managing shared calendars
  """
  def __init__(self):
    # __last_xxx instance attributes allow to save the entire state of the system
    # and get it back without loosing the uniqueness of the IDs
    self.__last_uid = 0  # Last User ID
    self.__last_eid = 100  # Last Event ID
    self.__users: Dict[int, User] = dict()
    self.__events: Dict[int, Event] = dict()

  @property
  def last_user_id(self):
    """
    Generator-like function to get the last user ID (so that they are unique)
    """
    self.__last_uid += 1
    return self.__last_uid

  @property
  def last_event_id(self):
    """
    Generator-like function to get the last event ID (so that they are unique)
    """
    self.__last_eid += 1
    return self.__last_eid
  
  @property
  def users(self) -> List[User]:
    return self.__users.values()
  
  @property
  def events(self) -> List[Event]:
    return self.__events.values()

  def add_user(self, u: User) -> None:
    if u.uid == -1: u.uid = self.last_user_id
    self.__users |= {u.uid: u}
  
  def add_event(self, e: Event) -> None:
    if e.eid == -1: e.eid = self.last_event_id
    self.__events |= {e.eid: e}
  
  def get_user(self, uid: int) -> User | KeyError:
    if uid not in self.__users:
      raise KeyError("User doesn't exist")
    
    return self.__users[uid]
  
  def get_event(self, eid: int) -> Event | KeyError:
    if eid not in self.__events:
      raise KeyError("Event doesn't exist")
    
    return self.__events[eid]

  def remove_event(self, eid: int) -> None | KeyError:
    if eid not in self.__events:
      raise KeyError("User doesn't exist")
    
    del self.__events[eid]

  def get_user_events(self, uid: int) -> List[Event] | KeyError:
    u = self.get_user(uid)
    return list(
      sorted(
        filter(lambda e: u in e.guests or u is e.owner, self.events),
        key=lambda e: e.date
      )
    )

  def get_owned_events(self, uid: int) -> List[Event] | KeyError:
    u = self.get_user(uid)
    return list(
      sorted(
        filter(lambda e: u is e.owner, self.events),
        key=lambda e: e.date
      )
    )
  
  def get_events_in_range(self, uid:int, start_date: datetime, end_date: datetime) -> List[Event]:
    return list(
      sorted(
        filter(
          lambda e: e.date >= start_date and e.date <= end_date,
          self.get_user_events(uid)
        ),
        key=lambda e: e.date
      )
    )
  
  def add_guest(self, eid: int, guest_uid: int) -> None | KeyError:
    gu = self.get_user(guest_uid)
    e = self.get_event(eid)
    e.guests.append(gu)
