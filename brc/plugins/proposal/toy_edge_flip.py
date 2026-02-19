import random
from brc.plugins.genome.toy_genome import ToyGenome

class ToyEdgeFlipProposer:
    def propose(self, genome, step):
        edges = set(genome.edges)
        if random.random() < 0.5:
            edges.add((random.randint(0,5), random.randint(0,5)))
        elif edges:
            edges.pop()
        return ToyGenome(list(edges))
