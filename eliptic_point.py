
class Point(object):
  def __init__(self, x, y, curve):
    self.__x = x
    self.__y = y
    self.__curve = curve

  def __add__(self, other):
    if other == INFINITY:
      return self
    if self == INFINITY:
      return other

    if self.__x == other.__x:
      if (self.__y + other.__y) % self.__curve.p() == 0:
        return INFINITY
      else:
        return self.double()

    p = self.__curve.p()

    l = ((other.__y - self.__y) * \
         self.inverse_mod(other.__x - self.__x, p)) % p

    x3 = (l * l - self.__x - other.__x) % p
    y3 = (l * (self.__x - x3) - self.__y) % p

    return Point(x3, y3, self.__curve)

  def double(self):
    if self == INFINITY:
      return INFINITY

    p = self.__curve.p()
    a = self.__curve.a()

    l = ((3 * self.__x * self.__x + a) * \
         self.inverse_mod(2 * self.__y, p)) % p

    x3 = (l * l - 2 * self.__x) % p
    y3 = (l * (self.__x - x3) - self.__y) % p

    return Point(x3, y3, self.__curve)

  def inverse_mod(self, a, m):
    if a < 0 or m <= a:
        a = a % m

    c, d = a, m
    uc, vc, ud, vd = 1, 0, 0, 1
    while c != 0:
        q, c, d = divmod(d, c) + (c,)
        uc, vc, ud, vd = ud - q * uc, vd - q * vc, uc, vc

    assert d == 1
    if ud > 0:
        return ud
    else:
        return ud + m

  def x(self):
    return self.__x

  def y(self):
    return self.__y
    
INFINITY = Point(None, None, None)
