#!/usr/bin/python3
import inspect as i
from Crypto.Util import number
INIT_PRIME_SIZE = 256


class Point(object):
  def __init__(self, x, y, p, a):
    self.__x = x
    self.__y = y
    self.__p = p
    self.__a = a

  def __add__(self, other):
    if other == INFINITY:
      return self
    if self == INFINITY:
      return other

    if self.__x == other.__x:
      if (self.__y + other.__y) % self.__p == 0:
        return INFINITY
      else:
        return self.double()

    p = self.__p()

    l = ((other.__y - self.__y) * \
         self.inverse_mod(other.__x - self.__x, p)) % p

    x3 = (l * l - self.__x - other.__x) % p
    y3 = (l * (self.__x - x3) - self.__y) % p

    return Point(x3, y3, p , 0)

  def double(self):
    if self == INFINITY:
      return INFINITY

    p = self.__p
    a = self.__a

    l = ((3 * self.__x * self.__x + a) * \
         self.inverse_mod(2 * self.__y, p)) % p

    x3 = (l * l - 2 * self.__x) % p
    y3 = (l * (self.__x - x3) - self.__y) % p

    return Point(x3, y3, p, a)

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

  def curve(self):
    return self.__curve


def randomP():
    p = number.getPrime(INIT_PRIME_SIZE)

    while(p % 4 != 3):
        p = number.getPrime(INIT_PRIME_SIZE)
    return p

def createElipticCurve(p):
    getRandom = lambda p: number.getRandomRange(0, p - 1)
    a = getRandom(p)
    b = getRandom(p)
    x = getRandom(p)

    delta = lambda a, b: (4 * pow(a, 3, p)) + (27 * pow(b, 2, p))
    elipticCurve = lambda a, b, x: (pow(x, 3, p) + (a * x) + b) % p

    while (delta(a, b) % p == 0):
        createElipticCurve(p)
    else:
        return elipticCurve, a, b, x

INFINITY = Point(None, None, None, None)

def main():

    p = randomP()
    c = p
    elipticCurve, a, b, x = createElipticCurve(p)

    if pow(elipticCurve(a,b,x), (p - 1) // 2, p) != 1:
        print('This is not quadratic residue')
        main()
        return

    y = pow(elipticCurve(a,b,x), (p + 1) // 4, p)

    # print(f'Point({x},{y})')
    # print('Eliptic curves coefficients')
    # print(f'X: {x}')
    # print(f'A: {a}')
    # print(f'B: {b}')

    p = Point(x, y, p, a)
    r = Point(x, y, p, a)
    q = p.__add__(r)

    print(q.x(), q.y())

    ya = pow(q.y(), 2, c)
    print(ya == elipticCurve(a, b, q.x()))


main()



