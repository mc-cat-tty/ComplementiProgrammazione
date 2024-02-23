from typing import List
from enum import Enum, auto
from model import Model
from user import *
from request import *
from operator import itemgetter
from dataclasses import fields, asdict
import os
from pickle import load, dump

BIN_FILENAME = "backup.bin"
TXT_FILENAME = "export.txt"

class SubMenu(Enum): HOME = auto(); SELECT = auto(); CREATE = auto(); BACKUP = auto()

class REPL:
  """
  Read Evaluate Print Loop that keeps CLI state and defines interactions
  """
  def __init__(self, model: Model):
    self.__model = model

  @property
  def menu_entries(self) -> List[str]:
    return ["c. Crea un nuovo utente", "s. Seleziona un utente", "b. Salva backup", "l. Carica backup", "t. Textual export", "e. Esci"]    
  
  def dispatcher(self, input: str):
    if input == 'c':
      self.create_routine()
    elif input == 's':
      self.select_routine()
    elif input == 'b':
      self.backup_routine()
    elif input == 'l':
      self.load_routine()
    elif input == 't':
      self.textual_export_routine()
    elif input == 'e':
      exit(0)
    else:
      raise RuntimeError("Invalid option selected")
  
  def textual_export_routine(self):
    with open(TXT_FILENAME, 'w') as fd:
      print(self.__model, file = fd)
    print("Done!")

  def backup_routine(self):
    with open(BIN_FILENAME, "wb") as fd:
      dump(self.__model, fd)
    print("Done!")

  def load_routine(self):
    with open(BIN_FILENAME, "rb") as fd:
      self.__model = load(fd)
    print("Done!")
  
  def create_routine(self):
    u = User()
    u.name = input('name [str]: ')
    u.salary = float(input('salary [float]: '))
    u.role = Role[input('role [director | subordinate]: ').upper()]
    if u.role == Role.SUBORDINATE:
      u.director = int(input("director id [int]: "))
    

    uid = self.__model.add(u)
    print(f"{u.name} creato con id {uid}")
  
  def select_routine(self) -> str:
    print(*self.__model.users, sep='\n')
    uid = int(input("id: "))

    
    if self.__model.get(uid).role == Role.SUBORDINATE:
      self.subordinate_select(uid)
    else:
      self.director_select(uid)
    
  
  def subordinate_select(self, uid: int):
    ch = ''
    while ch != 'i':
      # os.system('clear')
      print(*["r. Richiedi pagamento", "v. Visualizza richieste", "a. Visualizza ore accettate" if self.__model.get(uid).role == Role.SUBORDINATE else None, "i. Indietro"], sep='\n')
      ch = input(">> ")

      if ch == 'r':
        h = int(input("hours: "))
        self.__model.request_payment(uid, h)
        print("Richiesta inviata")
      elif ch == 'v':
        print(*self.__model.get_requests(uid), sep='\n')
      elif ch == 'a':
        ar = self.__model.get_accepted_requests(uid)
        print(*ar, sep='\n')
        print(f"Total: {self.__model.get_total_pay(uid)}")
      elif ch == 'i':
        continue
      else:
        raise RuntimeError("Invalid option")
      
  def director_select(self, uid: int):
    ch = ''
    while ch != 'i':
      print("Richieste dipendenti: ")
      print(*self.__model.get_requests(uid), sep='\n')
      rid = int(input('>> '))

      # os.system('clear')
      print(*["a. Accept", "d. Deny", "i. Indietro"], sep='\n')
      ch = input(">> ")
      if ch == 'i': continue
      self.__model.get_request(rid).state = State.ACCEPTED if ch == 'a' else State.DENIED

  def loop_async(self) -> None:
    # os.system("clear")
    print(*self.menu_entries, sep='\n')
    choice = input(">> ")

    try:
      self.dispatcher(choice)
      input()
    except Exception as e:
      print(e)
