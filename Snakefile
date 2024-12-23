# Snakefile: SCENIC pipeline

# Load config
configfile: "config.yaml"


rule create_results_dir:
    output:
        directory(config["results_dir"])
    shell:
        "mkdir -p {output}"


rule grn_inference:
    input:
        expression_matrix=config["data"]["expression_matrix"],
        tf_list=config["data"]["tf_list"]
    output:
        adjacencies="{results_dir}/run_{run_num}/adjacencies.csv",
        modules="{results_dir}/run_{run_num}/modules.pkl"
    params:
        run_num=lambda wildcards: wildcards.run_num
    shell:
        """
        python scripts/grn_inference.py --expression {input.expression_matrix} --tf {input.tf_list} \
            --adjacencies {output.adjacencies} --modules {output.modules}
        """

rule prune_modules:
    input:
        adjacencies="{results_dir}/run_{run_num}/adjacencies.csv",
        ranking_db=config["data"]["ranking_db"],
        motif_annotations=config["data"]["motif_annotations"]
    output:
        motifs="{results_dir}/run_{run_num}/motifs.csv",
        regulons="{results_dir}/run_{run_num}/regulons.pkl"
    shell:
        """
        python scripts/prune_modules.py --adjacencies {input.adjacencies} --db {input.ranking_db} \
            --motifs {input.motif_annotations} --motifs_output {output.motifs} \
            --regulons_output {output.regulons}
        """

rule auc_enrichment:
    input:
        expression_matrix=config["data"]["expression_matrix"],
        regulons="{results_dir}/run_{run_num}/regulons.pkl"
    output:
        auc_matrix="{results_dir}/run_{run_num}/AUCell_mat.csv"
    shell:
        """
        python scripts/auc_enrichment.py --expression {input.expression_matrix} \
            --regulons {input.regulons} --output {output.auc_matrix}
        """

rule generate_heatmap:
    input:
        auc_matrix="{results_dir}/run_{run_num}/AUCell_mat.csv",
        cell_types=config["data"]["cell_types"]
    output:
        heatmap="{results_dir}/run_{run_num}/AUCell_heatmap.png"
    shell:
        """
        python scripts/generate_heatmap.py --auc {input.auc_matrix} --cell_types {input.cell_types} \
            --output {output.heatmap}
        """
