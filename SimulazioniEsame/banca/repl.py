from config import *
from model import *
from typing import List, Any
from sys import exit
from user import User
from operation import Operation
from datetime import datetime

class REPL:
  """
  Read-Evaluate-Print-Loop that keeps CLI state and defines user interactions
  """
  def __init__(self, model: Model):
    self.__model = model
    self.__home_choices = [
      'u. Users',
      'a. Add new users',
      's. Save binary backup',
      'l. Load binary backup',
      't. Save textual backup',
      'e. Exit',
    ]
    self.__callbacks = {
      'u': self.users_routine,
      'a': self.add_user_routine,
      's': self.save_backup_routine,
      'l': self.load_backup_routine,
      't': self.save_textual_routine,
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
  
  def save_textual_routine(self) -> None:
    with open(TXT_FILENAME, 'w') as fd:
      for u in self.__model.users:
        print(u, file = fd)
        print(*u.operations, sep = '\n', file = fd)
        print(file = fd)
    
  def users_routine(self) -> None:
    if not self.__model.users:
      print("No user in the DB")
      return
    
    print(User.get_header())
    uid = self.__choose_option(
      self.__model.users,
      [*map(lambda u: u.id, self.__model.users)],
      'User ID: ',
      int
    )
    user = self.__model.get_user(uid)

    ch = self.__choose_option(
      ['v. Versamento', 'p. Prelievo', 's. Storico operazioni'],
      ['v', 'p', 's'],
    )

    if ch == 's':
      if not user.operations:
        print("No operations for this user")
        return

      sd = self.__blocking_input("Start filter date [dd-mm-YYYY or enter to skip]: ", lambda d: datetime.strptime(d, "%d-%m-%Y") if d else d)
      ed = self.__blocking_input("End filter date [dd-mm-YYYY or enter to skip]: ", lambda d: datetime.strptime(d, "%d-%m-%Y") if d else d)

      filtered_ops = filter(lambda o: (not sd or o.date >= sd) and (not ed or o.date <= ed), user.operations)
      filtered_ops = [*filtered_ops]
      print(Operation.get_header())
      print(*filtered_ops, sep='\n')

      totalch = self.__choose_option(
        [],
        ['y', 'n'],
        "View total [y/n]? "
      )

      if totalch == 'y':
        total = sum(map(lambda o: o.amount if o.type == OperationType.DEPOSIT else -o.amount, filtered_ops))
        print(f"Total: {total}")

    elif ch in ('v', 'p'):
      a = self.__blocking_input("Amount: ", float)
      d = self.__blocking_input("Date [dd-mm-YYYY]: ", lambda d: datetime.strptime(d, "%d-%m-%Y"))

      if ch == 'v': op = OperationType.DEPOSIT
      elif ch == 'p': op = OperationType.WITHDRAW
      
      self.__model.get_user(uid).add_op(Operation(self.__model.last_operation_id, a, d, op))
  
  def add_user_routine(self) -> None:
    u = User()
    u.name = self.__blocking_input('Name: ')
    u.surname = self.__blocking_input('Surname: ')
    uid = self.__model.add_user(u)
    print(f"Udded User with ID {uid}")

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
