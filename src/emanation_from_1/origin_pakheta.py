"""First Origin-Pakheta calculus primitives for positive integers."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import log
from typing import Callable

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
