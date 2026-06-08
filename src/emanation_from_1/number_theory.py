"""Small, dependency-free number theory utilities."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from math import gcd, isqrt, lcm, log


@dataclass(frozen=True)
class PrimePowerReturnComponent:
    """Carmichael-return data for one prime-power component."""

    prime: int
    exponent: int
    modulus: int
    phi: int
    lambda_value: int
    local_defect: Fraction


@dataclass(frozen=True)
class ModularReturnDecomposition:
    """Exact decomposition of lambda(n) / phi(n) into return pressures."""

    n: int
    shell_depth: int
    component_count: int
    odd_component_count: int
    radical: int
    radical_ratio: Fraction
    radical_compression: Fraction
    components: tuple[PrimePowerReturnComponent, ...]
    local_defect_ratio: Fraction
    overlap_penalty: Fraction
    lambda_phi_ratio: Fraction

    @property
    def minimum_odd_overlap_penalty(self) -> int:
        """Return the forced power-of-two overlap from odd components."""
        if self.odd_component_count == 0:
            return 1
        return 2 ** (self.odd_component_count - 1)

    @property
    def odd_distinct_prime_bound(self) -> Fraction:
        """Return 2^(1-omega_odd(n)) as an exact ratio."""
        return Fraction(1, self.minimum_odd_overlap_penalty)


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


def prime_power_modulus(prime: int, exponent: int) -> int:
    """Return p**a after validating a prime-power descriptor."""
    if not is_prime(prime):
        raise ValueError("prime-power component requires a prime base")
    if exponent < 1:
        raise ValueError("prime-power exponent must be >= 1")
    return prime**exponent


def prime_power_phi(prime: int, exponent: int) -> int:
    """Return phi(p**a) for a prime-power component."""
    modulus = prime_power_modulus(prime, exponent)
    return modulus - (modulus // prime)


def prime_power_lambda(prime: int, exponent: int) -> int:
    """Return lambda(p**a) for a prime-power component."""
    prime_power_modulus(prime, exponent)
    if prime == 2 and exponent >= 3:
        return 2 ** (exponent - 2)
    return (prime - 1) * (prime ** (exponent - 1))


def prime_power_return_component(
    prime: int,
    exponent: int,
) -> PrimePowerReturnComponent:
    """Return exact return data for p**a."""
    modulus = prime_power_modulus(prime, exponent)
    phi_value = prime_power_phi(prime, exponent)
    lambda_value = prime_power_lambda(prime, exponent)
    return PrimePowerReturnComponent(
        prime=prime,
        exponent=exponent,
        modulus=modulus,
        phi=phi_value,
        lambda_value=lambda_value,
        local_defect=Fraction(lambda_value, phi_value),
    )


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


def modular_idempotent_count(n: int) -> int:
    """Return the number of solutions to x**2 == x mod n."""
    if n < 1:
        raise ValueError("modular idempotent count is defined for positive integers")
    return 2 ** len(factor_counter(n))


def modular_involution_count(n: int) -> int:
    """Return the number of solutions to x**2 == 1 mod n."""
    if n < 1:
        raise ValueError("modular involution count is defined for positive integers")

    total = 1
    for prime, exponent in factor_counter(n).items():
        if prime == 2:
            if exponent == 1:
                total *= 1
            elif exponent == 2:
                total *= 2
            else:
                total *= 4
        else:
            total *= 2
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
        component = prime_power_lambda(prime, power)
        exponent = lcm(exponent, component)
    return exponent


def lambda_phi_ratio(n: int) -> Fraction:
    """Return lambda(n) / phi(n) as an exact ratio."""
    if n < 1:
        raise ValueError("lambda/phi ratio is defined for positive integers")
    return Fraction(carmichael_lambda(n), euler_totient(n))


def modular_return_decomposition(n: int) -> ModularReturnDecomposition:
    """Decompose lambda(n) / phi(n) into local defect and lcm overlap terms."""
    if n < 1:
        raise ValueError("modular return decomposition is defined for positive integers")

    counter = factor_counter(n)
    components = tuple(
        prime_power_return_component(prime, exponent)
        for prime, exponent in sorted(counter.items())
    )
    local_defect_ratio = Fraction(1, 1)
    component_product = 1
    component_lcm = 1
    for component in components:
        local_defect_ratio *= component.local_defect
        component_product *= component.lambda_value
        component_lcm = lcm(component_lcm, component.lambda_value)

    overlap_penalty = Fraction(component_product, component_lcm)
    radical_value = radical(n)
    radical_ratio = Fraction(radical_value, n)
    return ModularReturnDecomposition(
        n=n,
        shell_depth=sum(counter.values()),
        component_count=len(counter),
        odd_component_count=sum(1 for prime in counter if prime % 2 == 1),
        radical=radical_value,
        radical_ratio=radical_ratio,
        radical_compression=1 - radical_ratio,
        components=components,
        local_defect_ratio=local_defect_ratio,
        overlap_penalty=overlap_penalty,
        lambda_phi_ratio=local_defect_ratio / overlap_penalty,
    )


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
