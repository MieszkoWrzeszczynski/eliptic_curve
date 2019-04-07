#! /usr/bin/env python
from __future__ import division

from six import python_2_unicode_compatible
from ..utils import numbertheory

class Point(object):
  """A point on an elliptic curve. Altering x and y is forbidding,
     but they can be read by the x() and y() methods."""
  def __init__(self, curve, x, y, order=None):
    """curve, x, y, order; order (optional) is the order of this point."""
    self.__curve = curve
    self.__x = x
    self.__y = y
    self.__order = order
    # self.curve is allowed to be None only for INFINITY:
    if self.__curve:
      assert self.__curve.contains_point(x, y)
    if order:
      assert self * order == INFINITY

  def __eq__(self, other):
    """Return True if the points are identical, False otherwise."""
    if self.__curve == other.__curve \
       and self.__x == other.__x \
       and self.__y == other.__y:
      return True
    else:
      return False

  def __add__(self, other):
    """Add one point to another point."""

    # X9.62 B.3:

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

    return Point(self.__curve, x3, y3)

  def __mul__(self, other):
    """Multiply a point by an integer."""

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

    # From X9.62 D.3.2:

    e3 = 3 * e
    negative_self = Point(self.__curve, self.__x, -self.__y, self.__order)
    i = leftmost_bit(e3) // 2
    result = self
    # print_("Multiplying %s by %d (e3 = %d):" % (self, other, e3))
    while i > 1:
      result = result.double()
      if (e3 & i) != 0 and (e & i) == 0:
        result = result + self
      if (e3 & i) == 0 and (e & i) != 0:
        result = result + negative_self
      # print_(". . . i = %d, result = %s" % ( i, result ))
      i = i // 2

    return result

  def __rmul__(self, other):
    """Multiply a point by an integer."""

    return self * other

  def __str__(self):
    if self == INFINITY:
      return "infinity"
    return "(%d,%d)" % (self.__x, self.__y)

  def double(self):
    """Return a new point that is twice the old."""

    if self == INFINITY:
      return INFINITY

    # X9.62 B.3:

    p = self.__curve.p()
    a = self.__curve.a()

    l = ((3 * self.__x * self.__x + a) * \
         numbertheory.inverse_mod(2 * self.__y, p)) % p

    x3 = (l * l - 2 * self.__x) % p
    y3 = (l * (self.__x - x3) - self.__y) % p

    return Point(self.__curve, x3, y3)

  def x(self):
    return self.__x

  def y(self):
    return self.__y

  def curve(self):
    return self.__curve

  def order(self):
    return self.__order


# This one point is the Point At Infinity for all purposes:
INFINITY = Point(None, None, None)