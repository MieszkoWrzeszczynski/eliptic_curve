from eliptic_point import Point

class ElipticCurve(object):
  def __init__(self, p, a, b, x):
    """The curve of points satisfying y^2 = x^3 + a*x + b (mod p)."""
    self.__p = p
    self.__a = a
    self.__b = b
    self.__x = x

  def p(self):
    return self.__p

  def a(self):
    return self.__a

  def b(self):
    return self.__b

  def x(self):
    return self.__x
  
  def yPointCoordinateFromCurve(self):
    return pow(self.getCurveValue(self.__x), (self.__p + 1) // 4, self.__p)

  def getCurveValue(self, x):
    return (pow(x, 3, self.__p) + (self.__a * x) + self.__b) % self.__p
    
  def contains_point(self, p):
    """Is the point (x,y) on this curve?"""
    if p == INFINITY:
      return True
    return (p.y() * p.y() - (p.x() * p.x() * p.x() + self.__a * p.x() + self.__b)) % self.__p == 0

  def isNotQuatraticResidue(self):
    return pow(self.getCurveValue(self .__x), (self.__p - 1) // 2, self.__p) != 1

  def __str__(self):
    return "ElipticCurve(p=%d, a=%d, b=%d, x=%d)" % (self.__p, self.__a, self.__b, self.__x)

INFINITY = Point(None, None, None)