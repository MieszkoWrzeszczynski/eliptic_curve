#!/usr/bin/python3
import inspect as i
from Crypto.Util import number
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
    elipticCurve = lambda a, b, x: (pow(x, 3, p) + (a * x) + b) % p

    while (delta(a, b) % p == 0):
        createElipticCurve(p)
    else:
        return elipticCurve, a, b, x

def main():
    p = randomP()
    elipticCurve, a, b, x = createElipticCurve(p)

    if pow(elipticCurve(a,b,x), (p - 1) // 2, p) != 1:
        print('This is not quadratic residue')
        main()
        return

    y = pow(elipticCurve(a,b,x), (p + 1) // 4, p)

    print(f'Point({x},{y})')
    print('Eliptic curves coefficients')
    print(f'X: {x}')
    print(f'A: {a}')
    print(f'B: {b}')

main()