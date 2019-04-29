from eliptic_point import Point

class ElipticCurve(object):
  def __init__(self, p, a, b):
    """The curve of points satisfying y^2 = x^3 + a*x + b (mod p)."""
    self.__p = p
    self.__a = a
    self.__b = b

  def p(self):
    return self.__p

  def a(self):
    return self.__a

  def b(self):
    return self.__b
  
  def yPointCoordinateFromCurve(self, x):
    return pow(self.getCurveValue(x), (self.__p + 1) // 4, self.__p)

  def getCurveValue(self, x):
    return (pow(x, 3, self.__p) + (self.__a * x) + self.__b) % self.__p
    
  def contains_point(self, p):
    """Is the point (x,y) on this curve?"""
    if p == INFINITY:
      return True
    
    return (p.y() * p.y() - (p.x() * p.x() * p.x() + self.__a * p.x() + self.__b)) % self.__p == 0

  def isNotQuatraticResidue(self, x):
    return pow(self.getCurveValue(x), (self.__p - 1) // 2, self.__p) != 1

  def __str__(self):
    return "ElipticCurve(p=%d, a=%d, b=%d)" % (self.__p, self.__a, self.__b)

INFINITY = Point(None, None, None)