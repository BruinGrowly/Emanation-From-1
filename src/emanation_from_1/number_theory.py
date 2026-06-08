"""Small, dependency-free number theory utilities."""

from __future__ import annotations

from collections import Counter
from math import gcd, isqrt, lcm, log


def sieve(limit: int) -> list[int]:
    """Return all primes <= limit."""
    if limit < 2:
        return []

    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"

    for candidate in range(2, isqrt(limit) + 1):
        if flags[candidate]:
            start = candidate * candidate
            count = ((limit - start) // candidate) + 1
            flags[start : limit + 1 : candidate] = b"\x00" * count

    return [n for n in range(2, limit + 1) if flags[n]]


def first_n_primes(count: int) -> list[int]:
    """Return the first ``count`` primes."""
    if count < 0:
        raise ValueError("count must be non-negative")
    if count == 0:
        return []

    if count < 6:
        limit = 15
    else:
        limit = int(count * (log(count) + log(log(count)))) + 3

    while True:
        primes = sieve(limit)
        if len(primes) >= count:
            return primes[:count]
        limit *= 2


def is_prime(n: int) -> bool:
    """Return True when n is prime."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    factor = 3
    stop = isqrt(n)
    while factor <= stop:
        if n % factor == 0:
            return False
        factor += 2
    return True


def factor(n: int) -> list[int]:
    """Return prime factors of n with multiplicity."""
    if n < 1:
        raise ValueError("factorization is defined here for positive integers")
    if n == 1:
        return []

    factors: list[int] = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    candidate = 3
    while candidate * candidate <= n:
        while n % candidate == 0:
            factors.append(candidate)
            n //= candidate
        candidate += 2

    if n > 1:
        factors.append(n)

    return factors


def factor_counter(n: int) -> Counter[int]:
    """Return a prime-factor counter for n."""
    return Counter(factor(n))


def radical(n: int) -> int:
    """Return the product of distinct prime factors of n."""
    product = 1
    for prime in factor_counter(n):
        product *= prime
    return product


def divisor_count(n: int) -> int:
    """Return the number of positive divisors of n."""
    if n < 1:
        raise ValueError("divisor_count is defined for positive integers")

    total = 1
    for exponent in factor_counter(n).values():
        total *= exponent + 1
    return total


def euler_totient(n: int) -> int:
    """Return Euler's totient function."""
    if n < 1:
        raise ValueError("totient is defined for positive integers")

    result = n
    for prime in factor_counter(n):
        result = (result // prime) * (prime - 1)
    return result


def carmichael_lambda(n: int) -> int:
    """Return the Carmichael exponent of the multiplicative group modulo n."""
    if n < 1:
        raise ValueError("Carmichael lambda is defined for positive integers")
    if n == 1:
        return 1

    exponent = 1
    for prime, power in factor_counter(n).items():
        if prime == 2 and power >= 3:
            component = 2 ** (power - 2)
        else:
            component = (prime - 1) * (prime ** (power - 1))
        exponent = lcm(exponent, component)
    return exponent


def multiplicative_order(a: int, n: int) -> int:
    """Return the least positive k with a**k == 1 mod n."""
    if n < 2:
        raise ValueError("multiplicative order requires modulus >= 2")
    if gcd(a, n) != 1:
        raise ValueError("multiplicative order requires a and n to be coprime")

    order = carmichael_lambda(n)
    for prime in factor_counter(order):
        while order % prime == 0 and pow(a, order // prime, n) == 1:
            order //= prime
    return order


def goldbach_singular_factor(n: int) -> float:
    """Return the n-dependent Hardy-Littlewood Goldbach singular factor shape."""
    if n < 1:
        raise ValueError("singular factor is defined for positive integers")

    factor_value = 1.0
    for prime in factor_counter(n):
        if prime > 2:
            factor_value *= (prime - 1) / (prime - 2)
    return factor_value


def prime_gaps(limit: int) -> list[int]:
    """Return gaps between consecutive primes <= limit."""
    primes = sieve(limit)
    return [b - a for a, b in zip(primes, primes[1:])]
