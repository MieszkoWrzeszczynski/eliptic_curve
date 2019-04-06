#!/usr/bin/python3

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

    delta = lambda a, b: ((4 * pow(a, 3, p)) % p) + ((27 * pow(b, 2, p)) % p )
    elipticCurve = lambda a, b, x: (pow(x, 3, p) + (a * x) + b) % p

    while (delta(a, b) % p == 0):
        createElipticCurve(p)
    else:
        return elipticCurve, a, b, x

def main():
    p = randomP()
    elipticCurve, a, b, x = createElipticCurve(p)

    if pow(elipticCurve(a,b,x), (p - 1) // 2, p) != 1:
        print('f nie jest reszta kwadratowa p')
        main()
        return

    y = pow(elipticCurve(a,b,x), (p + 1) // 4, p)

    print(f'y: {y}')

    print(f'Punkt({x},{y})')

    print(elipticCurve)
    print(pow(y, 2, p))
    print(pow(y, 2, p) ==  elipticCurve(a,b,x))

main()