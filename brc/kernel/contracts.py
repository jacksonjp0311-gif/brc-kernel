from __future__ import annotations
from typing import Protocol, Any, runtime_checkable


# ============================================================
# METRIC CONTRACT
# ============================================================

@runtime_checkable
class Metric(Protocol):
    """
    Metric must return normalized distance in [0,1].
    Deterministic for identical inputs.
    """

    def distance(self, a: Any, b: Any) -> float:
        ...


# ============================================================
# GENOME CONTRACT
# ============================================================

@runtime_checkable
class Genome(Protocol):
    """
    Genome must provide stable serialization.
    """

    def to_dict(self) -> dict:
        ...


# ============================================================
# PROPOSER CONTRACT
# ============================================================

@runtime_checkable
class Proposer(Protocol):
    """
    Proposer must be deterministic when provided RNG.
    """

    def propose(self, genome: Genome, step: int, rng: Any) -> Genome:
        ...


# ============================================================
# VALIDATION HELPERS
# ============================================================

def assert_metric(value: float) -> None:
    v = float(value)
    if not (0.0 <= v <= 1.0):
        raise ValueError("Metric must return normalized value in [0,1]")


def assert_genome(obj: Any) -> None:
    if not hasattr(obj, "to_dict"):
        raise TypeError("Genome must implement to_dict()")


def assert_proposer(obj: Any) -> None:
    if not hasattr(obj, "propose"):
        raise TypeError("Proposer must implement propose()")
