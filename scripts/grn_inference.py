import argparse
import pandas as pd
from arboreto.algo import grnboost2
from pyscenic.utils import modules_from_adjacencies
import pickle

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GRN Inference")
    parser.add_argument("--expression", required=True, help="Path to expression matrix")
    parser.add_argument("--tf", required=True, help="Path to transcription factor list")
    parser.add_argument("--adjacencies", required=True, help="Output path for adjacencies")
    parser.add_argument("--modules", required=True, help="Output path for modules")

    args = parser.parse_args()

    # Load input data
    ex_matrix = pd.read_csv(args.expression, index_col=0)
    tf_list = [line.strip() for line in open(args.tf)]

    # GRN inference
    adjacencies = grnboost2(ex_matrix, tf_list, verbose=True)
    modules = list(modules_from_adjacencies(adjacencies, ex_matrix))

    # Save outputs
    adjacencies.to_csv(args.adjacencies, index=False, sep='\t')
    with open(args.modules, 'wb') as f:
        pickle.dump(modules, f)

    print(f"GRN inference completed. Outputs: {args.adjacencies}, {args.modules}")
