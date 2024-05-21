# Experiment 1

This directory contains the necessary files and scripts used for the first experiment as detailed in our paper. Below is a brief description of the contents of each subdirectory and script.

## Directory Structure

- **data/**: Contains all the raw data or human dataused in the experiment.
- **figs/**: Contains the figures generated for the paper.
- **notebooks/**: Contains Jupyter notebooks with preprocessing steps and demonstrations of the final plots.
- **results/**: Contains the CSV files with the results of the experiment.

## Scripts

- **0_exp1_get_data.py**: Script to fetch and prepare the data required for the experiment.
- **0_react_exp1_get_data.py**: Alternate script variant for data fetching.
- **1_exp1_check_data.py**: Script to validate and check the integrity of the data.
- **2_exp1_scoring_llms.py**: Script to score the language models as part of the experiment.
- **3_rsa_llms.py**: Script to perform RSA (Representational Similarity Analysis) on the language models.

## Running the Scripts

To run any of the experiment scripts, navigate to the `experiment_1` directory and execute the desired script using Python. For example:

```bash
cd experiments/experiment_1
python 0_exp1_get_data.py
```