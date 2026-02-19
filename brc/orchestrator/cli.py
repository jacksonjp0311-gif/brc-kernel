from __future__ import annotations

import argparse

from brc.plugins.genome.toy_genome import ToyGenome
from brc.plugins.proposal.toy_edge_flip import ToyEdgeFlipProposer
from brc.plugins.metrics.jaccard_edges import JaccardEdges

from brc.orchestrator.run import run


def main():
    parser = argparse.ArgumentParser(prog="brc-run")
    parser.add_argument("--root", default=".")
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--run-id", default=None, help="Optional explicit run_id")
    args = parser.parse_args()

    base = ToyGenome([])
    proposer = ToyEdgeFlipProposer()
    metric = JaccardEdges()

    meta = run(args.root, base, proposer, metric, steps=args.steps, seed=args.seed, run_id=args.run_id)
    print(json.dumps(meta, indent=2, sort_keys=True))


if __name__ == "__main__":
    import json
    main()
