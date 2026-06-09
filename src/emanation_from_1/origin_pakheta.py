"""First Origin-Pakheta calculus primitives for positive integers."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import log
from typing import Callable, Iterable

from .number_theory import factor_counter, is_prime, radical


IntegerContext = Callable[[int], int]


@dataclass(frozen=True)
class PathCommutator:
    """Compare two ordered paths through the same integer contexts."""

    n: int
    left_name: str
    right_name: str
    left_after_right: int
    right_after_left: int
    ratio: Fraction

    @property
    def commutes(self) -> bool:
        return self.left_after_right == self.right_after_left

    @property
    def log_abs_gap(self) -> float:
        if self.ratio == 1:
            return 0.0
        return abs(log(self.ratio.numerator) - log(self.ratio.denominator))


def least_prime_factor(n: int) -> int:
    """Return the least prime factor of n."""
    if n < 2:
        raise ValueError("least prime factor requires n >= 2")
    return min(factor_counter(n))


def compression_context(n: int) -> int:
    """Collapse repeated prime layers to the squarefree skeleton rad(n)."""
    if n < 1:
        raise ValueError("compression context is defined for positive integers")
    return radical(n)


def return_min_context(n: int) -> int:
    """Return one least-prime layer toward 1."""
    if n < 1:
        raise ValueError("return context is defined for positive integers")
    if n == 1:
        return 1
    return n // least_prime_factor(n)


def return_prime_context(prime: int) -> IntegerContext:
    """Return a context that removes one selected prime layer if present."""
    if not is_prime(prime):
        raise ValueError("selected return context requires a prime")

    def return_prime(n: int) -> int:
        if n < 1:
            raise ValueError("return context is defined for positive integers")
        if n % prime == 0:
            return n // prime
        return n

    return return_prime


def _validated_prime_set(primes: Iterable[int]) -> tuple[int, ...]:
    selected_primes = tuple(sorted(set(primes)))
    if any(not is_prime(prime) for prime in selected_primes):
        raise ValueError("selected return set requires primes")
    return selected_primes


def return_prime_set_context(primes: Iterable[int]) -> IntegerContext:
    """Return a context that removes one layer for each selected prime present."""
    selected_primes = _validated_prime_set(primes)

    def return_prime_set(n: int) -> int:
        if n < 1:
            raise ValueError("return context is defined for positive integers")
        divisor = 1
        for prime in selected_primes:
            if n % prime == 0:
                divisor *= prime
        return n // divisor

    return return_prime_set


def gather_context(prime: int) -> IntegerContext:
    """Return a context that gathers one prime facet onto n."""
    if not is_prime(prime):
        raise ValueError("gather context requires a prime")

    def gather(n: int) -> int:
        if n < 1:
            raise ValueError("gather context is defined for positive integers")
        return n * prime

    return gather


def path_commutator(
    n: int,
    left: IntegerContext,
    left_name: str,
    right: IntegerContext,
    right_name: str,
) -> PathCommutator:
    """Return the path commutator for left(right(n)) vs right(left(n))."""
    if n < 1:
        raise ValueError("path commutators are defined for positive integers")

    left_after_right = left(right(n))
    right_after_left = right(left(n))
    return PathCommutator(
        n=n,
        left_name=left_name,
        right_name=right_name,
        left_after_right=left_after_right,
        right_after_left=right_after_left,
        ratio=Fraction(left_after_right, right_after_left),
    )


def compression_return_commutator(n: int) -> PathCommutator:
    """Compare compress-after-return with return-after-compress."""
    return path_commutator(
        n,
        compression_context,
        "C",
        return_min_context,
        "R_min",
    )


def compression_return_gap_factor(n: int) -> int:
    """Return the exact C/R_min path gap factor."""
    if n < 1:
        raise ValueError("path gap factor is defined for positive integers")
    if n == 1:
        return 1

    counter = factor_counter(n)
    least_prime = min(counter)
    if counter[least_prime] > 1:
        return least_prime
    return 1


def compression_prime_return_commutator(n: int, prime: int) -> PathCommutator:
    """Compare compress-after-return_p with return_p-after-compress."""
    return path_commutator(
        n,
        compression_context,
        "C",
        return_prime_context(prime),
        f"R_{prime}",
    )


def compression_prime_return_gap_factor(n: int, prime: int) -> int:
    """Return the exact C/R_p path gap factor."""
    if n < 1:
        raise ValueError("path gap factor is defined for positive integers")
    if not is_prime(prime):
        raise ValueError("selected return path gap requires a prime")

    exponent = factor_counter(n).get(prime, 0)
    if exponent > 1:
        return prime
    return 1


def compression_prime_set_return_commutator(
    n: int,
    primes: Iterable[int],
) -> PathCommutator:
    """Compare compress-after-return_S with return_S-after-compress."""
    selected_primes = _validated_prime_set(primes)
    label = ",".join(str(prime) for prime in selected_primes)
    return path_commutator(
        n,
        compression_context,
        "C",
        return_prime_set_context(selected_primes),
        f"R_{{{label}}}",
    )


def compression_prime_set_return_gap_factor(
    n: int,
    primes: Iterable[int],
) -> int:
    """Return the exact C/R_S path gap factor."""
    if n < 1:
        raise ValueError("path gap factor is defined for positive integers")

    counter = factor_counter(n)
    gap = 1
    for prime in _validated_prime_set(primes):
        if counter.get(prime, 0) > 1:
            gap *= prime
    return gap


def compression_gather_commutator(n: int, prime: int) -> PathCommutator:
    """Compare compress-after-gather_p with gather_p-after-compress."""
    return path_commutator(
        n,
        compression_context,
        "C",
        gather_context(prime),
        f"G_{prime}",
    )


def compression_gather_gap_factor(n: int, prime: int) -> Fraction:
    """Return the exact C/G_p path gap factor."""
    if n < 1:
        raise ValueError("path gap factor is defined for positive integers")
    if not is_prime(prime):
        raise ValueError("gather path gap requires a prime")
    if n % prime == 0:
        return Fraction(1, prime)
    return Fraction(1, 1)
