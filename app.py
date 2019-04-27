#!/usr/bin/python3
from Crypto.Util import number
from eliptic_curve import ElipticCurve
from eliptic_point import Point

INIT_PRIME_SIZE = 256

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
    elipticCurve = ElipticCurve(p, a, b, x)

    while (delta(a, b) % p == 0):
        createElipticCurve(p)
    else:
        return elipticCurve, x


def createDiffieHellman(elipticCurve, point, p):
    aliceKa = number.getRandomRange(0, p)
    bobKb = number.getRandomRange(0, p)

    alicePa = point.__mul__(point, aliceKa)
    bobPb = point.__mul__(point, bobKb)
    bobPoint= alicePa.__mul__(alicePa, bobKb)
    alicePoint = bobPb.__mul__(bobPb, aliceKa)

    if(not bobPoint.__eq__(alicePoint)):
        print("Points are not equal")

    if(not elipticCurve.contains_point(bobPoint)):
        print("Point is not on a curve")

    return bobPoint


def main():
    p = randomP()
    elipticCurve, x = createElipticCurve(p)

    if elipticCurve.isQuatraticResidue():
        print('This is not quadratic residue')
        main()
        return
    
    y = elipticCurve.y()

    #Addition  
    p = Point(x, y, elipticCurve)
    r = Point(x, y, elipticCurve)
    q = p.__add__(r)

    print(elipticCurve.contains_point(q))

    #Double
    q1 = Point(x, y, elipticCurve)
    q1 = q1.double()    
    print(elipticCurve.contains_point(q1))

    #multiplication
    q2 = Point(x, y, elipticCurve)
    q3 = q2.__mul__(q2, 10)
    print(elipticCurve.contains_point(q3))

    #Diffiego-Hellmana
    secret_point = createDiffieHellman(elipticCurve, q2, 250)
    print("Secret point is:", secret_point)

main()