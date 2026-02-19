from __future__ import annotations

class JaccardEdges:
    """
    Distance-only metric (normalized to [0,1]).
    """

    def distance(self, a, b) -> float:
        A = set(getattr(a, "edges", []))
        B = set(getattr(b, "edges", []))

        if not A and not B:
            return 0.0

        return 1.0 - (len(A & B) / max(1, len(A | B)))
