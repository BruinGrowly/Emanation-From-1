"""Small statistical helpers for experiment reports."""

from __future__ import annotations

from math import sqrt


def mean(values: list[float]) -> float:
    """Return the arithmetic mean."""
    if not values:
        raise ValueError("mean requires at least one value")
    return sum(values) / len(values)


def pearson_correlation(xs: list[float], ys: list[float]) -> float | None:
    """Return Pearson correlation, or None when either side has zero variance."""
    if len(xs) != len(ys):
        raise ValueError("correlation inputs must have equal length")
    if len(xs) < 2:
        raise ValueError("correlation requires at least two paired values")

    x_mean = mean(xs)
    y_mean = mean(ys)
    x_centered = [x - x_mean for x in xs]
    y_centered = [y - y_mean for y in ys]
    numerator = sum(x * y for x, y in zip(x_centered, y_centered))
    x_norm = sqrt(sum(x * x for x in x_centered))
    y_norm = sqrt(sum(y * y for y in y_centered))

    if x_norm == 0 or y_norm == 0:
        return None
    return numerator / (x_norm * y_norm)

