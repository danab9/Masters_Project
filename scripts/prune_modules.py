import argparse
import pickle
from pyscenic.prune import prune2df, df2regulons
from ctxcore.rnkdb import FeatherRankingDatabase as RankingDatabase
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prune Modules and Predict Regulons")
    parser.add_argument("--adjacencies", required=True, help="Path to adjacencies file")
    parser.add_argument("--db", required=True, help="Path to ranking database")
    parser.add_argument("--motifs", required=True, help="Path to motif annotation file")
    parser.add_argument("--motifs_output", required=True, help="Output path for pruned motifs")
    parser.add_argument("--regulons_output", required=True, help="Output path for regulons")

    args = parser.parse_args()

    # Load inputs
    adjacencies = pd.read_csv(args.adjacencies, sep="\t")
    ranking_db = [RankingDatabase(fname=args.db, name="RankingDB")]

    # Prune modules and predict regulons
    pruned_df = prune2df(ranking_db, adjacencies, motif_annotations_fname=args.motifs)
    regulons = df2regulons(pruned_df)

    # Save outputs
    pruned_df.to_csv(args.motifs_output, index=False)
    with open(args.regulons_output, "wb") as f:
        pickle.dump(regulons, f)

    print(f"Pruned motifs saved to: {args.motifs_output}")
    print(f"Regulons saved to: {args.regulons_output}")
