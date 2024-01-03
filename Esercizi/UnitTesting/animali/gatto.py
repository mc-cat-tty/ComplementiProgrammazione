from animali.animale import Animale

class Gatto(Animale):
  def __init__(self, eta):
    super().__init__("Miao")
    self.eta = eta

if __name__ == "__main__":
  g = Gatto(15)
  g.faiVerso()