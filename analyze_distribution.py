#!/usr/bin/env python3
"""
Analyze the distribution of dice rolls from Cairo roller output
Copyright (C) 2025 [Zachary Blake]

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import numpy as np
from collections import Counter
import sys
import re


def parse_dice_rolls_from_input():
    """Parse dice rolls from stdin input"""
    rolls = []

    try:
        # Read all input from stdin
        input_text = sys.stdin.read()

        # Extract all numbers from the input (assumes dice rolls are integers 1-6)
        # This regex finds all integers in the input
        numbers = re.findall(r"\b[1-6]\b", input_text)

        # Convert to integers
        rolls = [int(num) for num in numbers]

        if not rolls:
            print("Error: No valid dice rolls found in input.", file=sys.stderr)
            print("Expected integers 1-6 in the piped input.", file=sys.stderr)
            sys.exit(1)

        return rolls

    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)


def analyze_distribution(rolls):
    """Analyze the distribution of dice rolls"""
    print("=== DICE ROLL DISTRIBUTION ANALYSIS ===")
    print(f"Total rolls: {len(rolls)}")
    print()

    # Count frequencies
    counts = Counter(rolls)

    # Expected frequency for fair dice (total_rolls/6)
    expected_freq = len(rolls) / 6

    print("FREQUENCY ANALYSIS:")
    print("Face | Count | Percentage | Expected | Deviation")
    print("-" * 50)

    total_chi_square = 0

    for face in range(1, 7):
        count = counts[face]
        percentage = (count / len(rolls)) * 100
        deviation = count - expected_freq
        chi_square_component = (deviation**2) / expected_freq
        total_chi_square += chi_square_component

        print(
            f"  {face}  |  {count:3d}  |   {percentage:5.1f}%   |  {expected_freq:5.1f}  |  {deviation:+6.1f}"
        )

    print("-" * 50)
    print(f"Chi-square statistic: {total_chi_square:.3f}")
    print(f"Critical value (5% significance, 5 df): 11.070")

    if total_chi_square < 11.070:
        print("✅ Distribution appears fair (fails to reject null hypothesis)")
    else:
        print("⚠️  Distribution may not be fair (rejects null hypothesis)")

    print()

    # Additional statistics
    mean = np.mean(rolls)
    median = np.median(rolls)
    std_dev = np.std(rolls, ddof=1)

    print("STATISTICAL MEASURES:")
    print(f"Mean: {mean:.3f} (expected: 3.500)")
    print(f"Median: {median:.1f} (expected: 3.500)")
    print(f"Standard deviation: {std_dev:.3f} (expected: ~1.708)")
    print(f"Min: {min(rolls)}, Max: {max(rolls)}")

    # Range analysis
    ranges = {
        "1-2 (low)": len([r for r in rolls if r in [1, 2]]),
        "3-4 (mid)": len([r for r in rolls if r in [3, 4]]),
        "5-6 (high)": len([r for r in rolls if r in [5, 6]]),
    }

    print()
    print("RANGE ANALYSIS:")
    for range_name, count in ranges.items():
        percentage = (count / len(rolls)) * 100
        print(f"{range_name}: {count} rolls ({percentage:.1f}%)")

    # Consecutive patterns
    consecutive_same = 0
    max_consecutive = 1
    current_consecutive = 1

    for i in range(1, len(rolls)):
        if rolls[i] == rolls[i - 1]:
            current_consecutive += 1
            max_consecutive = max(max_consecutive, current_consecutive)
        else:
            if current_consecutive > 1:
                consecutive_same += 1
            current_consecutive = 1

    print()
    print("PATTERN ANALYSIS:")
    print(f"Maximum consecutive same number: {max_consecutive}")
    print(f"Total consecutive same occurrences: {consecutive_same}")


if __name__ == "__main__":
    # Check if we're receiving piped input
    if sys.stdin.isatty():
        print("Usage: scarb execute | python3 analyze_distribution.py", file=sys.stderr)
        print(
            "This script expects dice roll data to be piped from scarb execute.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Parse dice rolls from stdin
    rolls = parse_dice_rolls_from_input()

    # Run the analysis
    analyze_distribution(rolls)
