#!/usr/bin/env python3
"""Deterministic checker for the Day 3 generated-clock lineage experiment."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


BASE_RE = re.compile(
    r"create_clock\s+.*?-name\s+(?P<name>\S+)\s+.*?-period\s+(?P<period>[0-9.]+)"
    r".*?\[get_ports\s+(?P<port>[^\]\s]+)\]",
    re.S,
)

GEN_RE = re.compile(
    r"create_generated_clock\s+.*?-name\s+(?P<name>\S+)"
    r".*?-source\s+\[get_ports\s+(?P<source>[^\]\s]+)\]"
    r".*?-divide_by\s+(?P<divide>[0-9.]+)"
    r".*?\[get_pins\s+(?P<target>[^\]\s]+)\]",
    re.S,
)

INDEPENDENT_RE = re.compile(
    r"create_clock\s+.*?-name\s+div2_clk\s+.*?-period\s+(?P<period>[0-9.]+)"
    r".*?\[get_pins\s+(?P<target>[^\]\s]+)\]",
    re.S,
)


@dataclass(frozen=True)
class Evidence:
    root_name: str
    root_period: float
    root_port: str
    mode: str
    target: str
    source_port: str | None = None
    divide_by: float | None = None
    independent_period: float | None = None

    @property
    def lineage_preserved(self) -> bool:
        return self.mode == "generated"

    @property
    def generated_period(self) -> float | None:
        if self.mode == "generated" and self.divide_by is not None:
            return self.root_period * self.divide_by
        return self.independent_period

    @property
    def source_edge_indices(self) -> tuple[int, int, int] | None:
        if self.mode == "generated" and self.divide_by == 2:
            return (1, 3, 5)
        return None


def parse(path: Path) -> Evidence:
    text = path.read_text(encoding="utf-8")
    base = BASE_RE.search(text)
    if not base:
        raise ValueError("root create_clock not found")

    generated = GEN_RE.search(text)
    if generated:
        return Evidence(
            root_name=base.group("name"),
            root_period=float(base.group("period")),
            root_port=base.group("port"),
            mode="generated",
            source_port=generated.group("source"),
            divide_by=float(generated.group("divide")),
            target=generated.group("target"),
        )

    independent = INDEPENDENT_RE.search(text)
    if independent:
        return Evidence(
            root_name=base.group("name"),
            root_period=float(base.group("period")),
            root_port=base.group("port"),
            mode="independent",
            independent_period=float(independent.group("period")),
            target=independent.group("target"),
        )

    raise ValueError("no supported div2 clock definition found")


def validate(e: Evidence) -> list[str]:
    errors: list[str] = []
    if e.root_name != "root_clk":
        errors.append("expected root clock named root_clk")
    if e.root_port != "clk":
        errors.append("root clock must target top-level port clk")
    if e.target != "u_div/Q":
        errors.append("derived clock must target divider output pin u_div/Q")

    if e.mode != "generated":
        errors.append(
            "derived divider clock is modeled with create_clock; source/master lineage is missing"
        )
        return errors

    if e.source_port != "clk":
        errors.append("generated clock source must resolve to top-level port clk")
    if e.divide_by != 2:
        errors.append("this experiment expects divide_by 2")
    if e.generated_period != 20.0:
        errors.append("expected generated period is 20 ns")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("sdc", type=Path)
    args = parser.parse_args()

    evidence = parse(args.sdc)
    errors = validate(evidence)

    print(f"root clock      : {evidence.root_name} @ {evidence.root_port}")
    print(f"root period     : {evidence.root_period:.3f} ns")
    print(f"derived target  : {evidence.target}")
    print(f"definition mode : {evidence.mode}")
    print(f"derived period  : {evidence.generated_period:.3f} ns")
    print(f"lineage kept    : {evidence.lineage_preserved}")
    if evidence.source_edge_indices:
        print(
            "source edges    : "
            + " ".join(str(i) for i in evidence.source_edge_indices)
            + "  (rise/fall/rise)"
        )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
