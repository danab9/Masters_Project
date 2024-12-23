import argparse
import pickle
import pandas as pd
from pyscenic.aucell import aucell

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AUCell Enrichment")
    parser.add_argument("--expression", required=True, help="Path to expression matrix")
    parser.add_argument("--regulons", required=True, help="Path to regulons file")
    parser.add_argument("--output", required=True, help="Output path for AUC matrix")

    args = parser.parse_args()

    # Load inputs
    ex_matrix = pd.read_csv(args.expression, index_col=0)
    with open(args.regulons, "rb") as f:
        regulons = pickle.load(f)

    # Calculate AUC
    auc_mtx = aucell(ex_matrix, regulons, num_workers=4)

    # Save AUC matrix
    auc_mtx.to_csv(args.output)
    print(f"AUC matrix saved to: {args.output}")
