# Experiment 2

This directory contains the necessary files and scripts used for the second experiment as detailed in our paper. Below is a brief description of the contents of each subdirectory and script.

## Directory Structure

- **data/**: Contains all the raw data or human data used in the experiment.
- **figs/**: Contains the figures generated for the paper.
- **notebooks/**: Contains Jupyter notebooks with preprocessing steps and demonstrations of the final plots.
- **results/**: Contains the CSV files with the results of the experiment.
- **results_with_distances/**: Contains the results including calculated distances.

## Scripts

- **0_exp2_querying.py**: Script to query and prepare the data required for the experiment.
- **0_react_llama_exp2_querying.py**: Alternate script variant for querying data.
- **2_get_distances.py**: Script to calculate distances as part of the experiment.
- **3_distances_category.py**: Script chart categorize distances.
- **3_distances_pathology.py**: Script chart distances based on pathology.

## Running the Scripts

To run any of the experiment scripts, navigate to the `experiment_2` directory and execute the desired script using Python. For example:

```bash
cd experiments/experiment_2
python 0_exp2_querying.py
```