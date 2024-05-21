import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

print(os.getcwd())
os.chdir("..")
os.chdir("..")
print(os.getcwd())
print(os.listdir())

model = "llama"
temperatures = [0.3,0.7,0.9]


def calculate_sem(data):
    return np.std(data, ddof=1) / np.sqrt(len(data))

for temperature in temperatures:
    human_df = pd.read_csv('/experiments/experiment_3/results/distances_metrics/human.csv')
    naive_df = pd.read_csv(f'experiments/experiment_3/results/distances_metrics/{model}/exp3_naive_{model}_{temperature}_distances.csv')
    chain_df = pd.read_csv(f'experiments/experiment_3/results/distances_metrics/{model}/exp3_chain_{model}_{temperature}_distances.csv')
    react_df = pd.read_csv(f'experiments/experiment_3/results/distances_metrics/{model}/exp3_react_{model}_{temperature}_distances.csv')

    fig, axs = plt.subplots(1, 4, figsize=(24, 6), sharey=True)
    fig.subplots_adjust(left=0.2, right=0.9)

    metrics = ['Average Sequential Distance', 'Average Pairwise Distance Word 0', 'Average Pairwise Distance Category']
    colors = ['red', 'blue', 'green']
    metric_labels = ['Sequential Distance', 'Pairwise Distance First Word', 'Pairwise Distance "Animal"']

    def add_data_to_ax(ax, group, label, show_legend=False):
        means = {}
        for i, label in enumerate(['Control', 'Patient']):
            subgroup = group[group['Label'] == label.lower()]
            for j, metric in enumerate(metrics):
                color = colors[j]
                sem = calculate_sem(subgroup[metric])
                mean_val = subgroup[metric].mean()
                ax.errorbar(i + (j - 1) * 0.2, mean_val, yerr=sem, fmt='o', color='black', alpha=0.7, capsize=5)
                if i == 0:
                    means[metric] = mean_val
                else:
                    ax.plot([0 + (j - 1) * 0.2, 1 + (j - 1) * 0.2], [means[metric], means[metric]], linestyle='--', color=color)
                    ax.plot([1 + (j - 1) * 0.2, 1 + (j - 1) * 0.2], [means[metric], mean_val], linestyle='--', color=color)
                for k in range(len(subgroup)):
                    if k == 0 and show_legend:  
                        ax.scatter(i + (j - 1) * 0.2 + np.random.uniform(-0.05, 0.05), subgroup.iloc[k][metric], color=color, marker='o', alpha=0.7, label=metric_labels[j])
                    else:
                        ax.scatter(i + (j - 1) * 0.2 + np.random.uniform(-0.05, 0.05), subgroup.iloc[k][metric], color=color, marker='o', alpha=0.7)
        ax.grid(False)

    add_data_to_ax(axs[0], human_df, 'Human', show_legend=True)
    axs[0].set_title('Human', fontsize=20)

    add_data_to_ax(axs[1], naive_df, 'Naive')
    axs[1].set_title('Naive', fontsize=20)

    add_data_to_ax(axs[2], chain_df, 'Chain')
    axs[2].set_title('Chain', fontsize=20)

    add_data_to_ax(axs[3], react_df, 'React')
    axs[3].set_title('React', fontsize=20)

    for ax in axs:
        ax.set_xticks([0, 1])
        ax.set_xticklabels(['Control', 'Patient'], fontsize=20)
        ax.tick_params(axis='y', labelsize=16)

    handles, labels = axs[0].get_legend_handles_labels()
    unique_labels = dict(zip(labels, handles))
    axs[0].legend(unique_labels.values(), unique_labels.keys(), fontsize=16, bbox_to_anchor=(-0.2, 1), loc='upper right')

    axs[0].set_ylabel('Value', fontsize=18)
    plt.savefig(f"experiments/experiment_3/figs/{model}/exp3_{model}_{temperature}.png")
