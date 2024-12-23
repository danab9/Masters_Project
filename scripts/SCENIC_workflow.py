import os
import pickle
from datetime import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from arboreto.algo import grnboost2
from arboreto.utils import load_tf_names
from pyscenic.utils import modules_from_adjacencies
from pyscenic.prune import prune2df, df2regulons
from pyscenic.aucell import aucell
from ctxcore.rnkdb import FeatherRankingDatabase as RankingDatabase

# utility functions
def setup_directories(base_dir, run_num):
    """Ensure the directory structure is ready for results"""
    results_dir = os.path.join(base_dir, f"run_{run_num}")
    os.makedirs(results_dir, exist_ok=True)
    return results_dir

def save_pickle(data, path):
    """Save data to a pickle file."""
    with open(path, 'wb') as f:
        pickle.dump(data, f)
    print(f"Saved Pickle: {path}")


def grn_inference(expression_matrix, tf_list, run_dir):
    """SCENIC Phase 1: GRN Inference and Module Generation."""
    adjacencies = grnboost2(expression_matrix, tf_list, verbose=True)
    modules = list(modules_from_adjacencies(adjacencies, expression_matrix))

    adjacencies.to_csv()

def regulon_prediction(modules, ranking_db, motif_annotaions):
    """SCENIC Phase 2+3: Predict Regulons"""
    regulons_df = prune2df(ranking_db, modules, motif_annotations_fname=motif_annotaions) # Prune modules for targets with cis regulatory footprints (RcisTarget)
    regulons = df2regulons(regulons_df) # convert data frame to rergulons
    return regulons

def cellular_enrichment(expression_matrix, regulons, num_workers=1):
    "SCCENIC Phase 4: Cellular Enrichment"
    auc_mtx = aucell(expression_matrix, regulons, num_workers)
    return auc_mtx