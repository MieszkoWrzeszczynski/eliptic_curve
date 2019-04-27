import numbertheory

class Point(object):
  def __init__(self, x, y, curve, order = None):
    self.__x = x
    self.__y = y
    self.__curve = curve
    self.__order = order

  def __str__(self):
    return "ElipticPoint(x=%d, y=%d)" % (self.__x, self.__y)

  def __eq__(self, other):
    """Return True if the points are identical, False otherwise."""
    if self.__curve == other.__curve \
       and self.__x == other.__x \
       and self.__y == other.__y:
      return True
    else:
      return False


  def __add__(self, other):
    if other == INFINITY:
      return self
    if self == INFINITY:
      return other

    assert self.__curve == other.__curve
    if self.__x == other.__x:
      if (self.__y + other.__y) % self.__curve.p() == 0:
        return INFINITY
      else:
        return self.double()

    p = self.__curve.p()

    l = ((other.__y - self.__y) * \
         numbertheory.inverse_mod(other.__x - self.__x, p)) % p

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
    """Inverse of a mod m."""

    if a < 0 or m <= a:
      a = a % m

    # From Ferguson and Schneier, roughly:

    c, d = a, m
    uc, vc, ud, vd = 1, 0, 0, 1
    while c != 0:
      q, c, d = divmod(d, c) + (c,)
      uc, vc, ud, vd = ud - q * uc, vd - q * vc, uc, vc

    # At this point, d is the GCD, and ud*a+vd*m = d.
    # If d == 1, this means that ud is a inverse.

    assert d == 1
    if ud > 0:
      return ud
    else:
      return ud + m

  def __mul__(self, other):
    def leftmost_bit(x):
      assert x > 0
      result = 1
      while result <= x:
        result = 2 * result
      return result // 2

    e = other
    if self.__order:
      e = e % self.__order
    if e == 0:
      return INFINITY
    if self == INFINITY:
      return INFINITY
    assert e > 0

    e3 = 3 * e
    negative_self = Point(self.__x, -self.__y, self.__curve, self.__order)
    i = leftmost_bit(e3) // 2
    result = self
    while i > 1:
      result = result.double()
      if (e3 & i) != 0 and (e & i) == 0:
        result = result + self
      if (e3 & i) == 0 and (e & i) != 0:
        result = result + negative_self
      i = i // 2

    return result

  def x(self):
    return self.__x

  def y(self):
    return self.__y
    
  def curve(self):
    return self.__curve
    
INFINITY = Point(None, None, None)
