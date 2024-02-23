from config import *
from model import *
from typing import List, Any
from sys import exit
from user import User
from chat import Chat, Message

class REPL:
  """
  Read-Evaluate-Print-Loop that keeps CLI state and defines user interactions
  """
  def __init__(self, model: Model):
    self.__model = model
    self.__home_choices = [
      'u. Users',
      'a. Add user',
      's. Save binary backup of a user',
      'l. Load binary backup of a user',
      't. Save textual backup of a chat',
      'e. Exit'
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

    # print(admitted_choices)

    while ch not in admitted_choices or not type_ok:
      ch = input("Invalid input. Try again " + prompt)
      # print(ch, type(ch), type_ok)

      try: ch = cast_fun(ch)
      except: type_ok = False
      else: type_ok = True
    
    return ch

  def dispatcher(self, choice: str) -> None | Exception:
    self.__callbacks[choice]()

  def save_backup_routine(self) -> None:
    from pickle import dump  # Lazy load of pickle. Unless the user needs it, don't load it.
    print("SAVE BINARY BACKUP OF A USER BY SELECTING IT")
    uid = self.__choose_option(
      self.__model.users,
      [*map(lambda u: u.uid, self.__model.users)],
      "User ID: ",
      int
    )
    with open(BIN_FILENAME, 'wb') as fd:
      dump(self.__model.get_user(uid), fd)
  
  def load_backup_routine(self) -> None:
    from pickle import load  # Lazy load of pickle. Unless the user needs it, don't load it.
    with open(BIN_FILENAME, 'rb') as fd:
      user = load(fd)
      self.__model.add_user(user)
  
  def save_textual_routine(self) -> None:
    print("SAVE TEXTUAL REPRESENTATION OF A CHAT BY CHOOSING A USER AND ONE OF HIS CHATS")
    uid = self.__choose_option(
      self.__model.users,
      [*map(lambda u: u.uid, self.__model.users)],
      "User ID: ",
      int
    )
    cid = self.__choose_option(
      self.__model.get_chats(uid),
      [*map(lambda c: c.cid, self.__model.get_chats(uid))],
      "Chat ID: ",
      int
    )

    with open(TXT_FILENAME, 'w') as fd:
      chat = next(filter(lambda c: c.cid == cid, self.__model.get_chats(uid)))
      print(Message.get_header(), file = fd)
      print(*chat.msgs, sep='\n', file = fd)
    
  def __send_messages(self, c: Chat, sndr_id: int, prompt: str) -> None:
      msg = input(prompt)
      while msg:
        c.msgs.append(Message(
          self.__model.get_user(sndr_id).name,
          sndr_id,
          msg
        ))
        msg = input(prompt)

  def users_routine(self):
    ch = ''
    id = -1
    while ch != 'b':
      if not self.__model.users:
        print("No users in the system")
        return
      
      if id == -1:
        print(User.get_header())
        id = self.__choose_option(
          self.__model.users,
          [*map(lambda u: u.uid, self.__model.users)],
          "User ID: ",
          int
        )

      chats = self.__model.get_chats(id)
      if not chats:
        print(f"No chat for user {id}")
      else:
        print(Chat.get_header())
        print(*chats, sep='\n')

      ch = self.__choose_option(
        ['e. Enter a chat', 'n. New chat', 'b. Go back'],
        ['e', 'n', 'b']
      )

      if ch == 'n':
        print("New chat with? ")
        toid = self.__choose_option(
          self.__model.users,
          [*map(lambda u: u.uid, self.__model.users)],
          "User ID: ",
          int
        )

        c = Chat(
          -1,
          self.__model.get_user(id).name, id,
          self.__model.get_user(toid).name, toid,
          []
        )

        self.__model.add_chat(id, c)
        self.__model.add_chat(toid, c)

        self.__send_messages(c, id, "Send your first message [enter to skip]: ")
      elif ch == 'e':
        cid = self.__choose_option(
          [],
          [*map(lambda c: c.cid, self.__model.get_chats(id))],
          "Chat ID: ",
          int
        )

        chat = next(filter(lambda c: c.cid == cid, self.__model.get_chats(id)))
        print(Message.get_header())
        print(*chat.msgs, sep='\n')
        self.__send_messages(chat, id, "Send your message [enter to skip]: ")
  
  def add_user_routine(self):
    u = User()
    u.name = self.__blocking_input("Name: ")
    self.__model.add_user(u)
    print(f"Crated user with ID {u.uid}")

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
