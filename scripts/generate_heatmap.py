import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Heatmap for AUCell Results")
    parser.add_argument("--auc", required=True, help="Path to AUC matrix")
    parser.add_argument("--cell_types", required=True, help="Path to cell type annotations")
    parser.add_argument("--output", required=True, help="Output path for heatmap image")

    args = parser.parse_args()

    # Load inputs
    auc_matrix = pd.read_csv(args.auc, index_col=0)
    cell_types = pd.read_csv(args.cell_types, index_col=0)

    # Map cell types to colors
    lut = dict(zip(cell_types.type.unique(), sns.color_palette("hls", len(cell_types.type.unique()))))
    cell_colors = cell_types.type.map(lut)
    row_colors = auc_matrix.merge(cell_colors, how="left", left_index=True, right_index=True).type

    # Generate and save heatmap
    ax = sns.clustermap(auc_matrix, figsize=(12, 12), yticklabels=True, xticklabels=True, row_colors=row_colors)
    ax.savefig(args.output)
    print(f"Heatmap saved to: {args.output}")
