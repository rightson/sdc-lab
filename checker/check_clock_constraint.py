#!/usr/bin/env python3
"""Small deterministic checker for the Day 2 create_clock experiment."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


CLOCK_RE = re.compile(
    r"create_clock\s+.*?-period\s+(?P<period>[0-9.]+)"
    r".*?-waveform\s+\{(?P<rise>[0-9.]+)\s+(?P<fall>[0-9.]+)\}"
    r".*?\[get_ports\s+(?P<port>[^\]\s]+)\]"
)


@dataclass(frozen=True)
class ClockIntent:
    period: float
    rise: float
    fall: float
    port: str

    @property
    def setup_edge_separation(self) -> float:
        return self.period

    @property
    def hold_edge_separation(self) -> float:
        return 0.0


def parse_clock(path: Path) -> ClockIntent:
    text = path.read_text(encoding="utf-8")
    match = CLOCK_RE.search(text)
    if not match:
        raise ValueError("no supported create_clock command found")
    return ClockIntent(
        period=float(match.group("period")),
        rise=float(match.group("rise")),
        fall=float(match.group("fall")),
        port=match.group("port"),
    )


def validate(clock: ClockIntent, expected_port: str = "clk") -> list[str]:
    errors: list[str] = []
    if clock.period <= 0:
        errors.append("clock period must be positive")
    if not (0 <= clock.rise < clock.fall < clock.period):
        errors.append("waveform edges must satisfy 0 <= rise < fall < period")
    if clock.port != expected_port:
        errors.append(
            f"clock target resolves to '{clock.port}', expected top-level port '{expected_port}'"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("sdc", type=Path)
    parser.add_argument("--expected-port", default="clk")
    args = parser.parse_args()

    clock = parse_clock(args.sdc)
    errors = validate(clock, args.expected_port)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"clock target : {clock.port}")
    print(f"period       : {clock.period:.3f} ns")
    print(f"waveform     : rise {clock.rise:.3f} ns, fall {clock.fall:.3f} ns")
    print(f"setup edges  : {clock.setup_edge_separation:.3f} ns apart")
    print(f"hold edges   : {clock.hold_edge_separation:.3f} ns apart")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
