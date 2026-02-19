class JaccardEdges:
    def compute(self, prev, cand, base):
        a = set(prev.edges)
        b = set(cand.edges)

        if not a and not b:
            d = 0
        else:
            d = 1 - len(a & b) / max(1, len(a | b))

        R = 1 - d
        Delta = d
        S = R - Delta

        return {"R": R, "Delta": Delta, "S": S}
