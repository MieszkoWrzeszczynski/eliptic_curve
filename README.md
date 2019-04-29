# Elliptic Curve implementation

>  Elliptic-curve cryptography (ECC) is an approach to public-key cryptography based on the algebraic structure of elliptic curves over finite fields. ECC requires smaller keys compared to non-EC cryptography (based on plain Galois fields) to provide equivalent security. Elliptic curves are applicable for key agreement, digital signatures, pseudo-random generators and other tasks. Indirectly, they can be used for encryption by combining the key agreement with a symmetric encryption scheme. They are also used in several integer factorization algorithms based on elliptic curves that have applications in cryptography, such as Lenstra elliptic-curve factorization. - https://en.wikipedia.org/wiki/Elliptic-curve_cryptography

## Requirements
```
  pip install -r requirements.txt
```

## Addition of points
```python
  p = Point(x, y, elipticCurve)
  r = Point(x, y, elipticCurve)
  q = p + r
```

## Multiplication of point
```python
  q2 = Point(x, y, elipticCurve)
  q3 = q2 * 100
```

## Checking if curve contains point
```python
  elipticCurve.contains_point(point)
```


## Elliptic-curve Diffie–Hellman
```python
  secret_point = createDiffieHellman(elipticCurve, q2, 2500)
```