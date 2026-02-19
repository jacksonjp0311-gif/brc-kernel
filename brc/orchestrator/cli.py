import argparse

from brc.plugins.genome.toy_genome import ToyGenome
from brc.plugins.proposal.toy_edge_flip import ToyEdgeFlipProposer
from brc.plugins.metrics.jaccard_edges import JaccardEdges

from brc.orchestrator.run import run

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--steps", type=int, default=20)
    args = parser.parse_args()

    base = ToyGenome([])
    proposer = ToyEdgeFlipProposer()
    metric = JaccardEdges()

    run(args.root, base, proposer, metric, steps=args.steps)

if __name__ == "__main__":
    main()
