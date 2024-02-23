from config import *
from model import *
from typing import List, Any
from sys import exit

class REPL:
  """
  Read-Evaluate-Print-Loop that keeps CLI state and defines user interactions
  """
  def __init__(self, model: Model):
    self.__model = model
    self.__home_choices = [
      's. Save binary backup',
      'l. Load binary backup',
      't. Save textual backup',
      'e. Exit'
    ]
    self.__callbacks = {
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
      print(self.__model, file = fd)

  def loop_async(self) -> None:
    ch = self.__choose_option(
      self.__home_choices,
      self.__callbacks.keys()
    )

    try:
      self.dispatcher(ch)
    except Exception as e:
      print(e)
