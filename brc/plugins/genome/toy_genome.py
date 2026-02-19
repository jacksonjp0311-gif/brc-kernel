class ToyGenome:
    def __init__(self, edges):
        self.edges = set(edges)

    def to_dict(self):
        return {"edges": list(self.edges)}
