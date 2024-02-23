from config import *
from model import *
from typing import List, Any
from sys import exit
import config

class REPL:
  """
  Read-Evaluate-Print-Loop that keeps CLI state and defines user interactions
  """
  def __init__(self, model: Model):
    self.__model = model
    self.__home_choices = [
      'u. Users (view and interact with calendars)',
      'a. Add user',
      's. Save binary backup',
      'l. Load binary backup',
      'e. Exit'
    ]
    self.__callbacks = {
      'u': self.users_routine,
      'a': self.add_user_routine,
      's': self.save_backup_routine,
      'l': self.load_backup_routine,
      'e': lambda: exit(0),
    }
  
  @staticmethod
  def __blocking_input(prompt = '>> ', cast_fun = str) -> Any:
    val = input(prompt)
    type_ok = True

    try: val = cast_fun(val)
    except: type_ok = False

    while not type_ok:
      val = input("Invalid input. Try again " + prompt)

      try: val = cast_fun(val)
      except: type_ok = False
      else: type_ok = True
    
    return val

  @staticmethod
  def __choose_option(opts: List[str], admitted_choices: List[Any], prompt = '>> ', cast_fun = str) -> Any:
    """
    Print a list of options (each on a different line) and read the chosen option
    """
    print(*opts, sep='\n')
    
    ch = input(prompt)
    type_ok = True

    try: ch = cast_fun(ch)
    except: type_ok = False

    while ch not in admitted_choices or not type_ok:
      ch = input("Invalid input. Try again " + prompt)

      try: ch = cast_fun(ch)
      except: type_ok = False
      else: type_ok = True
    
    return ch

  def dispatcher(self, choice: str) -> None | Exception:
    self.__callbacks[choice]()

  def save_backup_routine(self) -> None:
    from pickle import dump  # Lazy load of pickle. Unless the user needs it, don't load it.
    with open(BIN_FILENAME, 'wb') as fd:
      dump(self.__model, fd)
  
  def load_backup_routine(self) -> None:
    from pickle import load  # Lazy load of pickle. Unless the user needs it, don't load it.
    with open(BIN_FILENAME, 'rb') as fd:
      self.__model = load(fd)
    
  def add_user_routine(self) -> None | Exception:
    u = User()
    u.name = input("Name: ")
    if not u.name:
      print("No user added. Exiting from the routine")
      return
    self.__model.add_user(u)
    print(f"Create user with ID {u.uid}")

  def users_routine(self) -> None | Exception:
    if not self.__model.users:
      print("No user in the DB")
      return
  
    print(User.get_header())
    uid = self.__choose_option(
      self.__model.users,
      [*map(lambda u: u.uid, self.__model.users)],
      "User ID: ",
      int
    )

    ch = ''
    while ch != 'h':
      u = self.__model.get_user(uid)
      # print(f"\nUSER {u.name} [{u.uid}] CALENDAR")
      events = self.__model.get_user_events(uid)
      owned_events = self.__model.get_owned_events(uid)
      
      print()
      ch = self.__choose_option(
        ["a. Add event", "d. Delete event", 'g. Invite guest', 'v. View all events', "f. Filter events (by date or range)", "h. Home (go back)"],
        ['a', 'd', 'g', 'v', 'f', 'h']
      )

      if ch == 'a':  # Add event for the user
        e = Event()
        e.name = input("Event name: ")
        if not e.name:
          print("No event created")
          continue
        
        e.date = self.__blocking_input(
         "Event date [dd-mm-YYYY]: ",
          lambda d: datetime.strptime(d, config.DATE_FORMAT)
        )
        e.owner = u
        self.__model.add_event(e)
        print(f"Created event with ID {e.eid}")
      elif ch == 'd':  # Delete event for the user
        if not owned_events:
          print(f"{u.name} is not owner of any event")
          continue
        
        print("Events you can delete")
        eid = self.__choose_option(
          owned_events,
          [*map(lambda e: e.eid, owned_events)],
          "Event ID: ",
          int
        )
        self.__model.remove_event(eid)
        print(f"Deleted event {eid}")
      elif ch == 'g':  # Add guest to event
        if not owned_events:
          print(f"{u.name} is not owner of any event")
          continue
        
        eid = self.__choose_option(
          owned_events,
          [*map(lambda e: e.eid, owned_events)],
          "Event ID: ",
          int
        )

        invitable_users = list(self.__model.users)[:]
        invitable_users.remove(u)
        guest_uid = self.__choose_option(
          invitable_users,
          [*map(lambda u: u.uid, invitable_users)],
          "Guest user ID: ",
          int
        )

        self.__model.add_guest(eid, guest_uid)
      elif ch == 'f':  # Filter by data or range
        self.view_events_routine(uid)
      elif ch == 'v':  # View all events
        if not events:
          print("No events for this user. Try to add one")
        else:
          print(Event.get_header())
          print(*events, sep='\n')

  def view_events_routine(self, uid: int) -> None | Exception:
    start_date = self.__blocking_input(
      "Start date [dd-mm-YYYY]: ",
      lambda d: datetime.strptime(d, config.DATE_FORMAT)
    )
    end_date = self.__blocking_input(
      "End date [dd-mm-YYYY] [enter to omit]: ",
      lambda d: datetime.strptime(d, config.DATE_FORMAT) if d else d
    )

    if not end_date: end_date = start_date

    events = self.__model.get_events_in_range(uid, start_date, end_date)
    
    if not events:
      print("No events for this range")
      return
    
    events = sorted(events, key=lambda e: e.date)

    print(Event.get_header())
    prev_day = events[0].date
    print(f"\nLISTING {datetime.strftime(prev_day, config.DATE_FORMAT)} EVENTS")
    for e in events:
      if e.date != prev_day:
        prev_day = e.date
        print(f"\nLISTING {datetime.strftime(prev_day, config.DATE_FORMAT)} EVENTS")
      print(e)

  def loop_async(self) -> None:
    print()
    ch = self.__choose_option(
      self.__home_choices,
      self.__callbacks.keys()
    )

    try:
      self.dispatcher(ch)
    except Exception as e:
      print(e)
