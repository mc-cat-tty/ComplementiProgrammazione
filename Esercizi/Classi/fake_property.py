class fake_property:
  def __init__(self, getf):
    self.getf = getf
  
  def __get__(self, obj, objtype = None):
    return self.getf(obj)

  def setter(self, setf):
    self.setf = setf
  
  def __set__(self, obj, value):
    self.setf(obj, value)


class Prop:
  def __init__(self):
    self.__var = 10
  
  @property
  def var(self):
    return self.__var
  
  @var.setter
  def var(self, value):
    self.__var  = value

class FakeProp:
  def __init__(self):
    self.__var = 10
  
  @fake_property
  def var(self):
    return self.__var

  @var.setter
  def var(self, value):
    self.__var = value
  
fp = FakeProp()
p = Prop()

p.var = 20
fp.var = 30

print(p.var)
print(fp.var)
