#!/usr/bin/env python3
"""Minimal deterministic timing model for SDC Lab Day 1."""

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class TimingResult:
    arrival: float
    required: float
    slack: float

    @property
    def meets_timing(self) -> bool:
        return self.slack >= 0


def analyze(period: float, delay: float, launch: float = 0.0) -> TimingResult:
    if period <= 0:
        raise ValueError("clock period must be > 0")
    if delay < 0:
        raise ValueError("path delay must be >= 0")

    arrival = launch + delay
    required = launch + period
    return TimingResult(
        arrival=arrival,
        required=required,
        slack=required - arrival,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--period", type=float, required=True)
    parser.add_argument("--delay", type=float, required=True)
    parser.add_argument("--launch", type=float, default=0.0)
    args = parser.parse_args()

    result = analyze(args.period, args.delay, args.launch)
    print(f"arrival  = {result.arrival:.3f} ns")
    print(f"required = {result.required:.3f} ns")
    print(f"slack    = {result.slack:.3f} ns")
    print("status   = PASS" if result.meets_timing else "status   = FAIL")


if __name__ == "__main__":
    main()
