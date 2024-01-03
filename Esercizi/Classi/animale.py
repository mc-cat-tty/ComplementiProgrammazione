class Animale:
  def __init__(self, sesso, zampe = 4, malato = False, spavaldo = False):
    self.sesso = sesso
    self.zampe = zampe
    self.__malato = malato
    self.__spavaldo = spavaldo
  
  @property
  def malato(self):
    return self.__malato if not self.__spavaldo else False
    
  @property
  def spavaldo(self):
    return self.__spavaldo
  
  @malato.setter
  def malato(self, value):
    self.__malato = value
  
  @spavaldo.setter
  def spavaldo(self, value):
    self.__spavaldo = value
  
  def cammina(self):
    print("cammina")
  
  def corri(self):
    print("corri")
  
  def __add__(self, other):
    if self.sesso != other.sesso and type(self) == type(other):
      return type(self)("M")
    raise Exception("Animali non compatibili")

  def __str__(self):
    return f"{self.sesso} spavaldo: {self.spavaldo} malato: {self.malato}"


class Cane(Animale):
  counter = 0
  
  def __init__(self, *args, **kwargs):
    self.__private = 101
    super().__init__(*args, *kwargs)
  
  def abbaia(self):
    print("abbiaiato")


class Gatto(Animale):
  def miagola(self):
    print("miagolato")


c = Cane('M')
print(c._Cane__private)
c.malato = True
c.spavaldo = False
print(c.malato)
print(c.spavaldo)

cm = Cane("F")
cf = Cane("M")
print(cm+cf)

gm = Gatto('M')
gf = Gatto('F')
print(gm+gf)

print(gm+cf)  # Animali non compatibili

