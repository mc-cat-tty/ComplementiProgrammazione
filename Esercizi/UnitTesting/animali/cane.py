from animali.animale import Animale 

class Cane(Animale):
  def __init__(self, razza):
    super().__init__("Bau")
    self.razza = razza

if __name__ ==  "__main__":
  c = Cane("Pastore australiano")
  c.faiVerso()