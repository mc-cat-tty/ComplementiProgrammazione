import unittest, io, sys
from animali import *

class TestGatto(unittest.TestCase):
  def setUp(self):
    self.g = gatto.Gatto(10)

  def testVerso(self):
    capturedOut = io.StringIO()
    sys.stdout = capturedOut
    self.g.faiVerso()
    self.assertEqual(capturedOut.getvalue(), "Miao\n")
    sys.stdout = sys.__stdout__
  
  def testEta(self):
    self.assertIsInstance(self.g.eta, int)
  
  def testNotRazza(self):
    with self.assertRaises(AttributeError):
      self.g.razza
    
  @unittest.skip
  def testNotRazza(self):
    with self.assertRaises(AttributeError):
      self.g.eta

class TestCane(unittest.TestCase):
  def setUp(self):
    self.c = cane.Cane("Labrador")
  
  def testVerso(self):
    capturedOut = io.StringIO()
    sys.stdout = capturedOut
    self.c.faiVerso()
    self.assertEqual(capturedOut.getvalue(), "Bau\n")
    sys.stdout = sys.__stdout__
  
  def testRazza(self):
    self.assertIsInstance(self.c.razza, str)
  
  def testNotEta(self):
    with self.assertRaises(AttributeError):
      self.eta

if __name__ == "__main__":
  unittest.main()