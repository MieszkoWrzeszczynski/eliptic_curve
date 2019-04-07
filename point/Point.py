
# This one point is the Point At Infinity for all purposes:
#INFINITY = Point(None, None, None)

class Point(object):
  def __init__(self, curve, x, y):
    self.__curve = curve
    self.__x = x
    self.__y = y

  def __eq__(self, other):
    if self.__curve == other.__curve \
       and self.__x == other.__x \
       and self.__y == other.__y:
      return True
    else:
      return False

  def x(self):
    return self.__x

  def y(self):
    return self.__y

  def curve(self):
    return self.__curve