# Functions to handle loading of Seurat files and some basic data extraction.

library(SeuratDisk)
library(dplyr)
library(Seurat)
library(Matrix)

# Function to load a Seurat object
# returns Seurat object
load_seurat <- function(input_file) {
  # check file existence
  if (!file.exists(input_file)) {
    stop(paste("The file does not exist:", input_file))
  }

  sdata <- LoadH5Seurat(input_file)
  return(sdata)
}

# Function to extract raw counts from Seurat object
# returns data frame
extract_raw_counts <- function(seurat_obj, output_file) {
  raw_counts <- seurat_obj[["RNA"]]@counts
  raw_counts_df <- raw_counts %>% as.matrix %>% t %>% as.data.frame

  return(raw_counts_df)
}

# Function to save counts data frame to CSV
save_to_csv <- function(data, output_file) {
  write.csv(data, output_file, row.names = TRUE)
  message("Data saved to: ", output_file)
}

# Function to load cell type annotations from Seurat object
# returns data frame
load_cell_types <- function(seurat_obj) {
  cell_types_df <- as.data.frame(seurat_obj@active.ident)
  colnames(cell_types_df) <- c("type")
  return(cell_types_df)
}
