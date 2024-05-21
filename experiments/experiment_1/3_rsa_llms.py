import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau, pointbiserialr

def load_data(file_path):
    data = pd.read_csv(file_path)
    data = data.drop(columns=['Induced Pathology'])
    return data

def flatten_data(data):
    flattened_vectors = data.drop(columns=['Iteration']).values.reshape(-1, 9*10)
    flattened_df = pd.DataFrame(flattened_vectors)
    return flattened_df

def calculate_row_correlation(df1, df2, model1, model2, correlation_type='pearson'):
    correlations = []
    for i in range(df1.shape[0]):
        print(f"Calculating correlation between {model1} and {model2} at row {i}")
        if correlation_type == 'pearson':
            correlation, _ = pearsonr(df1.iloc[i], df2.iloc[i])
        elif correlation_type == 'spearman':
            correlation, _ = spearmanr(df1.iloc[i], df2.iloc[i])
        elif correlation_type == 'kendall':
            correlation, _ = kendalltau(df1.iloc[i], df2.iloc[i])
        elif correlation_type == 'biserial':
            correlation, _ = pointbiserialr(df1.iloc[i], df2.iloc[i])
        else:
            raise ValueError(f"Invalid correlation type: {correlation_type}")
        correlations.append(correlation)
    average_correlation = np.mean(correlations)
    return average_correlation

def generate_correlation_matrix(dfs, model_labels):
    model_names = {
        'gpt-3.5-turbo': 'GPT 3.5 Turbo',
        'mistral': 'Mistral',
        'dolphin': 'Dolphin',
        'llama': 'LLaMA-2 HF',
        'gemma': 'Gemma',
        'human': 'Human'
    }

    correlation_matrix = [[None] * len(dfs) for _ in range(len(dfs))]
    for i in range(len(dfs)):
        for j in range(len(dfs)):
            if i == j:
                correlation_matrix[i][j] = 1
            elif correlation_matrix[j][i] is None:
                correlation_matrix[i][j] = calculate_row_correlation(dfs[i], dfs[j], model_labels[i], model_labels[j], correlation_type='pearson')
                correlation_matrix[j][i] = correlation_matrix[i][j]

    model_labels = [model_names.get(model, model) for model in model_labels]
    df_correlations = pd.DataFrame(correlation_matrix, index=model_labels, columns=model_labels)

    human_correlations = df_correlations.loc['Human'].drop('Human')
    sorted_models = human_correlations.sort_values(ascending=False).index.tolist()
    sorted_models.insert(0, 'Human')

    df_correlations = df_correlations.loc[sorted_models, sorted_models]

    return df_correlations, sorted_models

def visualize_heatmap(df_correlations, title, mode, ax):
    sns.set(font_scale=1.2)
    heatmap = sns.heatmap(df_correlations, annot=True, cmap='viridis', fmt=".2f", annot_kws={"size": 16}, ax=ax, square=True, cbar=False)
    heatmap.set_xticklabels(heatmap.get_xticklabels(), fontsize=16, rotation=45, ha='right')
    heatmap.set_yticklabels(heatmap.get_yticklabels(), fontsize=16, rotation=0)
    ax.set_title(title, fontsize=20, pad=24)
    ax.tick_params(labelsize=18)

def main():
    os.chdir("..")
    os.chdir("..")
    print(os.getcwd())

    temperatures = [0.3, 0.7, 0.9]

    for temperature in temperatures:
        file_paths = {
            'gpt-3.5-turbo': f'experiments/experiment_1/results/gpt-3.5-turbo/scores_{{mode}}_gpt-3.5-turbo_{temperature}.csv',
            'gemma': f'experiments/experiment_1/results/gemma/scores_{{mode}}_gemma_{temperature}.csv',
            'dolphin': f'experiments/experiment_1/results/dolphin/scores_{{mode}}_dolphin_{temperature}.csv',
            'mistral': f'experiments/experiment_1/results/mistral/scores_{{mode}}_mistral_{temperature}.csv',
            'llama': f'experiments/experiment_1/results/llama/scores_{{mode}}_llama_{temperature}.csv',
            'human': 'experiments/experiment_1/results/human/human_data.csv'
        }

        fig, axs = plt.subplots(1, 3, figsize=(30, 12))
        plt.subplots_adjust(wspace=0.5, left=0.1, right=0.92, bottom=0.1, top=0.95)
        plt.suptitle(f"RSA ({temperature})", fontsize=30, y=0.89)

        for i, mode in enumerate(['naive', 'chain', 'react']):
            dfs = []
            model_labels = []
            for model, file_path in file_paths.items():
                data = load_data(file_path.format(mode=mode))
                flattened_df = flatten_data(data)
                dfs.append(flattened_df)
                model_labels.append(model)

            df_correlations, model_labels = generate_correlation_matrix(dfs, model_labels)
            if mode == "naive":
                mode_title = "Naive"
            elif mode == "chain":
                mode_title = "Chain"
            elif mode == "react":
                mode_title = "React"

            visualize_heatmap(df_correlations, f"Prompt Technique: {mode_title}", mode, axs[i])

        cbar_ax = fig.add_axes([0.94, 0.1, 0.02, 0.8])
        fig.colorbar(axs[2].collections[0], cax=cbar_ax)
        plt.savefig(f'experiments/experiment_1/figs/rsa/rsa_{temperature}.png', bbox_inches='tight')
        plt.show()

if __name__ == '__main__':
    main()