from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from .contracts import assert_metric


@dataclass(frozen=True)
class Stats:
    R: float
    Delta: float
    S: float

    def as_dict(self) -> Dict[str, float]:
        return {"R": float(self.R), "Delta": float(self.Delta), "S": float(self.S)}


class BRC:
    """
    BRC kernel computes stability stats from a distance-only metric.

    Metric contract:
      metric.distance(a, b) -> float in [0, 1]
    """

    def __init__(self, metric: Any):
        self.metric = metric

    def evaluate(self, gamma_prev: Any, gamma_curr: Any, gamma_base: Any) -> Dict[str, float]:
        d_base = float(self.metric.distance(gamma_curr, gamma_base))
        d_step = float(self.metric.distance(gamma_curr, gamma_prev))

        assert_metric(d_base)
        assert_metric(d_step)

        R = 1.0 - d_base
        Delta = d_step
        S = R - Delta

        return Stats(R=R, Delta=Delta, S=S).as_dict()
