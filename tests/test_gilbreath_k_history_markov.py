from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from emanation_from_1.conjectures import (  # noqa: E402
    certified_lock_scan,
    markov_gap_sequence,
    markov_gap_sequence_with_history,
)
from emanation_from_1.number_theory import first_n_primes  # noqa: E402


class GilbreathKHistoryMarkovTests(unittest.TestCase):
    def test_history_one_matches_existing_markov_generator(self) -> None:
        primes = first_n_primes(128)

        old_sequence = markov_gap_sequence(primes, seed=41000)
        new_sequence = markov_gap_sequence_with_history(primes, history=1, seed=41000)

        self.assertEqual(new_sequence, old_sequence)

    def test_k_history_sequence_preserves_initial_history_gaps(self) -> None:
        primes = first_n_primes(128)
        sequence = markov_gap_sequence_with_history(primes, history=3, seed=41000)

        prime_gaps = [right - left for left, right in zip(primes, primes[1:])]
        generated_gaps = [
            right - left for left, right in zip(sequence, sequence[1:])
        ]

        self.assertEqual(len(sequence), len(primes))
        self.assertEqual(generated_gaps[:3], prime_gaps[:3])

    def test_k_history_control_remains_scannable(self) -> None:
        primes = first_n_primes(256)
        sequence = markov_gap_sequence_with_history(primes, history=2, seed=41000)
        scan = certified_lock_scan(sequence)

        self.assertEqual(scan.length, 256)
        self.assertGreater(scan.rows_scanned, 0)
        self.assertTrue(scan.certified or scan.first_failure is not None)

    def test_invalid_history_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            markov_gap_sequence_with_history([2, 3, 5], history=0, seed=41000)


if __name__ == "__main__":
    unittest.main()
