"""Origin-facing measurements for positive integers."""

from __future__ import annotations

from dataclasses import dataclass
from math import log, sqrt

from .number_theory import divisor_count, factor, radical

PHI = (1 + sqrt(5)) / 2


@dataclass(frozen=True)
class OriginProfile:
    """A compact profile of how an integer differentiates from 1."""

    n: int
    factors: tuple[int, ...]
    emanation_depth: int
    distinct_factor_depth: int
    radical: int
    divisor_count: int
    log_distance: float
    phi_attenuation: float
    return_path: tuple[int, ...]


def return_path_to_one(n: int) -> list[int]:
    """Trace n back to 1 by removing the smallest factor layer first."""
    if n < 1:
        raise ValueError("return paths are defined for positive integers")
    if n == 1:
        return [1]

    path = [n]
    current = n
    for prime in factor(n):
        current //= prime
        path.append(current)
    return path


def origin_profile(n: int) -> OriginProfile:
    """Return the Origin Frame profile for n."""
    if n < 1:
        raise ValueError("origin profiles are defined for positive integers")

    factors = tuple(factor(n))
    depth = len(factors)

    return OriginProfile(
        n=n,
        factors=factors,
        emanation_depth=depth,
        distinct_factor_depth=len(set(factors)),
        radical=radical(n),
        divisor_count=divisor_count(n),
        log_distance=0.0 if n == 1 else log(n),
        phi_attenuation=PHI ** (-depth),
        return_path=tuple(return_path_to_one(n)),
    )


def profile_range(limit: int) -> list[OriginProfile]:
    """Return origin profiles for 1..limit."""
    if limit < 1:
        raise ValueError("limit must be >= 1")
    return [origin_profile(n) for n in range(1, limit + 1)]

