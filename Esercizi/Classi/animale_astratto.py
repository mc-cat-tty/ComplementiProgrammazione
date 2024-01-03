from abc import ABC, abstractmethod

class Malato:
  def __init__(self):
    pass

  def __get__(self, obj, objtype = None):
    return obj.__dict__['malato'] if not obj.spavaldo else False

  def __set__(self, obj, value):
    obj.__dict__['malato'] = value  # Nota l'utilizzo del dizionario

class Animale(ABC):
  malato = Malato()

  def __init__(self, sesso, zampe = 4, malato = False, spavaldo = False):
    self.sesso = sesso
    self.zampe = zampe
    self.__spavaldo = spavaldo
    self.malato = False
  
  @property
  def spavaldo(self):
    return self.__spavaldo
  
  @spavaldo.setter
  def spavaldo(self, value):
    self.__spavaldo = value
  
  def cammina(self):
    print("cammina")
  
  def corri(self):
    print("corri")
  
  @abstractmethod
  def fai_verso(self):
    ...
  
  def __add__(self, other):
    if self.sesso != other.sesso and type(self) == type(other):
      return type(self)("M")
    raise Exception("Animali non compatibili")

  def __str__(self):
    m = self.malato
    return f"{self.sesso} spavaldo: {self.spavaldo} malato: {m}"


class Cane(Animale):
  counter = 0
  
  def __init__(self, *args, **kwargs):
    self.__private = 101
    super().__init__(*args, *kwargs)
  
  def fai_verso(self):
    print("abbiaiato")


class Gatto(Animale):
  def fai_verso(self):
    print("miagolato")


c = Cane('M')
print(c._Cane__private)
c.malato = True
c.spavaldo = True
print(c.malato)
print(c.spavaldo)

cm = Cane("F")
cf = Cane("M")
print(cm+cf)

gm = Gatto('M')
gf = Gatto('F')
print(gm+gf)

# print(gm+cf)  # Animali non compatibili

gm.fai_verso()
cm.fai_verso()