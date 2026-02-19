from __future__ import annotations

import random
from brc.plugins.genome.toy_genome import ToyGenome


class ToyEdgeFlipProposer:
    """
    Deterministic proposer when supplied an rng (random.Random seeded upstream).

    Contract (preferred):
      propose(genome, step, rng) -> genome

    Backward compatible:
      if rng omitted, falls back to module random (not recommended for production).
    """

    def propose(self, genome, step, rng=None):
        r = rng if rng is not None else random

        edges = set(genome.edges)

        if r.random() < 0.5:
            edges.add((r.randint(0, 5), r.randint(0, 5)))
        elif edges:
            # deterministic pop with RNG: convert to tuple-sorted list
            ordered = sorted(list(edges))
            idx = r.randint(0, len(ordered) - 1)
            edges.remove(ordered[idx])

        return ToyGenome(list(edges))
