from user import User
from chat import Chat
from typing import List, Dict

class Model:
  """
  In-memory users and chats database. Defines interactions between users.
  """
  def __init__(self):
    self.__users: Dict[int, User] = dict()
    self.__last_uid = 0  # Last user ID
    self.__last_cid = 100  # Last chat ID
  
  @property
  def users(self):
    return self.__users.values()

  @property
  def last_user_id(self):
    self.__last_uid += 1
    return self.__last_uid
  
  @property
  def last_chat_id(self):
    self.__last_cid += 1
    return self.__last_cid

  def add_user(self, u: User) -> None:
    u.uid = self.last_user_id
    self.__users |= {u.uid: u}
  
  def get_user(self, uid: int) -> User | KeyError:
    if not uid in self.__users:
      raise KeyError("User doesn't exist")
    return self.__users[uid]
  
  def get_chats(self, uid: int) -> List[Chat] | KeyError:
    return self.get_user(uid).chats

  def add_chat(self, uid:int, chat: Chat) -> None | KeyError:
    # Chat already exists?
    if chat.cid <= 0: chat.cid = self.last_chat_id
    self.get_user(uid).chats.append(chat)
