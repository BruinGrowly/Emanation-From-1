"""Finite scans for conjecture-shaped prime phenomena."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

from .number_theory import first_n_primes, sieve


@dataclass(frozen=True)
class GilbreathCheck:
    """Result of a finite Gilbreath scan."""

    prime_count: int
    rows_checked: int
    failures: tuple[tuple[int, int], ...]

    @property
    def verified(self) -> bool:
        return not self.failures


def absolute_difference_row(row: list[int]) -> list[int]:
    """Return the absolute differences of adjacent entries."""
    return [abs(right - left) for left, right in zip(row, row[1:])]


def gilbreath_rows(prime_count: int) -> list[list[int]]:
    """Build the prime row and all repeated absolute-difference rows."""
    if prime_count < 1:
        raise ValueError("prime_count must be >= 1")

    rows = [first_n_primes(prime_count)]
    while len(rows[-1]) > 1:
        rows.append(absolute_difference_row(rows[-1]))
    return rows


def gilbreath_check(prime_count: int) -> GilbreathCheck:
    """Check whether finite Gilbreath rows begin with 1 after the prime row."""
    rows = gilbreath_rows(prime_count)
    failures = tuple(
        (index, row[0])
        for index, row in enumerate(rows[1:], start=1)
        if row[0] != 1
    )
    return GilbreathCheck(
        prime_count=prime_count,
        rows_checked=max(0, len(rows) - 1),
        failures=failures,
    )


def gilbreath_row_metrics(prime_count: int, max_rows: int = 16) -> list[dict[str, float | int]]:
    """Return compact metrics for the first Gilbreath rows."""
    rows = gilbreath_rows(prime_count)
    metrics: list[dict[str, float | int]] = []

    for index, row in enumerate(rows[:max_rows]):
        metrics.append(
            {
                "row": index,
                "length": len(row),
                "first": row[0],
                "min": min(row),
                "max": max(row),
                "ones": row.count(1),
                "zeros": row.count(0),
                "mean": mean(row),
            }
        )

    return metrics


def goldbach_pairs(n: int, primes: list[int] | None = None) -> list[tuple[int, int]]:
    """Return prime pairs p <= q with p + q = n."""
    if n < 4 or n % 2:
        raise ValueError("Goldbach pair scans require an even n >= 4")

    if primes is None:
        primes = sieve(n)
    prime_set = set(primes)

    return [
        (prime, n - prime)
        for prime in primes
        if prime <= n // 2 and (n - prime) in prime_set
    ]


def goldbach_scan(limit: int) -> dict[str, object]:
    """Scan even numbers up to limit for Goldbach witnesses."""
    if limit < 4:
        raise ValueError("limit must be >= 4")

    primes = sieve(limit)
    failures: list[int] = []
    richest_even = 4
    richest_count = 0

    for n in range(4, limit + 1, 2):
        pair_count = len(goldbach_pairs(n, primes))
        if pair_count == 0:
            failures.append(n)
        if pair_count > richest_count:
            richest_even = n
            richest_count = pair_count

    return {
        "limit": limit,
        "evens_checked": ((limit - 4) // 2) + 1,
        "failures": tuple(failures),
        "richest_even": richest_even,
        "richest_pair_count": richest_count,
    }


def twin_prime_pairs(limit: int) -> list[tuple[int, int]]:
    """Return twin prime pairs <= limit."""
    primes = sieve(limit)
    prime_set = set(primes)
    return [(prime, prime + 2) for prime in primes if prime + 2 in prime_set]

