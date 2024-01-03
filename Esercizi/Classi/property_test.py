class A:
  def __init__(self):
    self.a = 10

class B:
  @property
  def b(self):
    print("b")

def f():
  print("f")

print(dir(B))
print(dir(B.b))
print(dir(f))
print(dir(A.a))  # Error expected cause it's not an object