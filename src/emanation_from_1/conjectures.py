"""Finite scans for conjecture-shaped prime phenomena."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
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


@dataclass(frozen=True)
class SequenceBoundaryCheck:
    """Result of a finite first-column check for any sequence."""

    name: str
    length: int
    rows_checked: int
    verified: bool
    first_failure: tuple[int, int] | None
    first_column_prefix: tuple[int, ...]


@dataclass(frozen=True)
class DifferenceRowSummary:
    """Compact diagnostics for one absolute-difference row."""

    row_index: int
    length: int
    first: int
    max_value: int
    odd_count: int
    certificate_defects: int
    is_certificate: bool


@dataclass(frozen=True)
class CertifiedLockScan:
    """Streaming scan for first failure or first certified lock."""

    length: int
    rows_scanned: int
    certified_lock_row: int | None
    first_failure: tuple[int, int] | None

    @property
    def certified(self) -> bool:
        return self.certified_lock_row is not None


def absolute_difference_row(row: list[int]) -> list[int]:
    """Return the absolute differences of adjacent entries."""
    return [abs(right - left) for left, right in zip(row, row[1:])]


def difference_rows(initial: list[int]) -> list[list[int]]:
    """Build all repeated absolute-difference rows from an initial sequence."""
    if not initial:
        raise ValueError("initial sequence must not be empty")

    rows = [initial]
    while len(rows[-1]) > 1:
        rows.append(absolute_difference_row(rows[-1]))
    return rows


def first_column(rows: list[list[int]]) -> list[int]:
    """Return the first entry of each non-empty row."""
    return [row[0] for row in rows if row]


def row_certificate_defects(row: list[int]) -> int:
    """Return how far a row is from the finite Gilbreath certificate shape."""
    if not row:
        raise ValueError("row must not be empty")

    first_defect = 0 if row[0] == 1 else 1
    tail_defects = sum(1 for value in row[1:] if value not in (0, 2))
    return first_defect + tail_defects


def is_certificate_row(row: list[int]) -> bool:
    """Return True when row begins with 1 and all tail values are 0 or 2."""
    return row_certificate_defects(row) == 0


def first_certificate_row(rows: list[list[int]], start: int = 1) -> int | None:
    """Return the first certificate row index, or None if no row qualifies."""
    for index, row in enumerate(rows[start:], start=start):
        if is_certificate_row(row):
            return index
    return None


def certified_lock_scan(initial: list[int]) -> CertifiedLockScan:
    """Stream rows until first boundary failure or first certificate row."""
    if len(initial) < 2:
        raise ValueError("initial sequence must have at least two values")

    row = initial
    for row_index in range(1, len(initial)):
        row = absolute_difference_row(row)
        if row[0] != 1:
            return CertifiedLockScan(
                length=len(initial),
                rows_scanned=row_index,
                certified_lock_row=None,
                first_failure=(row_index, row[0]),
            )
        if is_certificate_row(row):
            return CertifiedLockScan(
                length=len(initial),
                rows_scanned=row_index,
                certified_lock_row=row_index,
                first_failure=None,
            )

    return CertifiedLockScan(
        length=len(initial),
        rows_scanned=len(initial) - 1,
        certified_lock_row=None,
        first_failure=None,
    )


def difference_row_summaries(rows: list[list[int]]) -> list[DifferenceRowSummary]:
    """Return row-level diagnostics for a finite difference triangle."""
    return [
        DifferenceRowSummary(
            row_index=index,
            length=len(row),
            first=row[0],
            max_value=max(row),
            odd_count=sum(1 for value in row if value % 2 == 1),
            certificate_defects=row_certificate_defects(row),
            is_certificate=is_certificate_row(row),
        )
        for index, row in enumerate(rows)
    ]


def boundary_return_check(
    initial: list[int],
    name: str = "sequence",
    first_column_limit: int = 24,
) -> SequenceBoundaryCheck:
    """Check whether every generated difference row starts with 1."""
    rows = difference_rows(initial)
    failure = next(
        (
            (index, row[0])
            for index, row in enumerate(rows[1:], start=1)
            if row[0] != 1
        ),
        None,
    )
    return SequenceBoundaryCheck(
        name=name,
        length=len(initial),
        rows_checked=max(0, len(rows) - 1),
        verified=failure is None,
        first_failure=failure,
        first_column_prefix=tuple(first_column(rows)[:first_column_limit]),
    )


def gilbreath_rows(prime_count: int) -> list[list[int]]:
    """Build the prime row and all repeated absolute-difference rows."""
    if prime_count < 1:
        raise ValueError("prime_count must be >= 1")

    return difference_rows(first_n_primes(prime_count))


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


def consecutive_odd_sequence(length: int) -> list[int]:
    """Return 2, 3, 5, 7, ... with the requested length."""
    if length < 2:
        raise ValueError("length must be >= 2")
    return [2] + [2 * n + 1 for n in range(1, length)]


def odd_arithmetic_after_boundary(length: int, gap: int) -> list[int]:
    """Return 2, 3, 3+gap, 3+2*gap, ... for an even gap."""
    if length < 2:
        raise ValueError("length must be >= 2")
    if gap <= 0 or gap % 2:
        raise ValueError("gap must be a positive even integer")

    values = [2, 3]
    while len(values) < length:
        values.append(values[-1] + gap)
    return values


def random_odd_small_gap_sequence(
    length: int,
    max_gap_units: int,
    seed: int,
) -> list[int]:
    """Return 2, 3, then odd values with random gaps in {2, ..., 2*max_gap_units}."""
    if length < 2:
        raise ValueError("length must be >= 2")
    if max_gap_units < 1:
        raise ValueError("max_gap_units must be >= 1")

    rng = Random(seed)
    values = [2, 3]
    while len(values) < length:
        values.append(values[-1] + 2 * rng.randint(1, max_gap_units))
    return values


def sequence_from_gaps(start: int, gaps: list[int]) -> list[int]:
    """Build a sequence from a starting value and consecutive gaps."""
    values = [start]
    for gap in gaps:
        values.append(values[-1] + gap)
    return values


def shuffled_tail_gap_sequence(initial: list[int], seed: int) -> list[int]:
    """Return a sequence with the first gap fixed and all later gaps shuffled."""
    if len(initial) < 2:
        raise ValueError("initial sequence must have at least two values")

    gaps = [right - left for left, right in zip(initial, initial[1:])]
    if len(gaps) <= 1:
        return initial[:]

    rng = Random(seed)
    tail = gaps[1:]
    rng.shuffle(tail)
    return sequence_from_gaps(initial[0], [gaps[0], *tail])


def block_shuffled_tail_gap_sequence(
    initial: list[int],
    block_size: int,
    seed: int,
) -> list[int]:
    """Shuffle prime-gap blocks after preserving the first gap."""
    if len(initial) < 2:
        raise ValueError("initial sequence must have at least two values")
    if block_size < 1:
        raise ValueError("block_size must be >= 1")

    gaps = [right - left for left, right in zip(initial, initial[1:])]
    if len(gaps) <= 1:
        return initial[:]

    tail = gaps[1:]
    blocks = [tail[index : index + block_size] for index in range(0, len(tail), block_size)]
    rng = Random(seed)
    rng.shuffle(blocks)
    shuffled_tail = [gap for block in blocks for gap in block]
    return sequence_from_gaps(initial[0], [gaps[0], *shuffled_tail])


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
