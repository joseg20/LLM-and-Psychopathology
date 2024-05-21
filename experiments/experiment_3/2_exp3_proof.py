# Verify that the complete code provided works correctly in this environment
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os
# Current work
print(os.getcwd())
# Change directory 2 level up
os.chdir("..")
os.chdir("..")
print(os.getcwd())
# Look for the file in the directory
print(os.listdir())

model = "mistral"
temperature = 0.3

# Load the data
react_dolphin_data = pd.read_csv(f'experiments/experiment_3/results/distances_metrics/{model}/exp3_react_{model}_{temperature}_distancess.csv')
human_data = pd.read_csv('experiments/experiment_3/results/distances_metrics/human_distances.csv')
chain_dolphin_data = pd.read_csv(f'experiments/experiment_3/results/distances_metrics/{model}/exp3_chain_{model}_{temperature}_distancess.csv')
naive_dolphin_data = pd.read_csv(f'experiments/experiment_3/results/distances_metrics/{model}/exp3_naive_{model}_{temperature}_distancess.csv')

# Calculate means for each group
means = {
    'Human - Control': human_data[human_data['Label'] == 'control']['Average Sequential Distance Word 0'].mean(),
    'Dolphin - Control': react_dolphin_data[react_dolphin_data['Label'] == 'control']['Average Sequential Distance Word 0'].mean(),
    'Human - Patient': human_data[human_data['Label'] == 'patient']['Average Sequential Distance Word 0'].mean(),
    'Dolphin - Patient': react_dolphin_data[react_dolphin_data['Label'] == 'patient']['Average Sequential Distance Word 0'].mean()
}

means_naive = {
    'Human - Control': human_data[human_data['Label'] == 'control']['Average Sequential Distance Word 0'].mean(),
    'Dolphin - Control': naive_dolphin_data[naive_dolphin_data['Label'] == 'control']['Average Sequential Distance Word 0'].mean(),
    'Human - Patient': human_data[human_data['Label'] == 'patient']['Average Sequential Distance Word 0'].mean(),
    'Dolphin - Patient': naive_dolphin_data[naive_dolphin_data['Label'] == 'patient']['Average Sequential Distance Word 0'].mean()
}

means_chain = {
    'Human - Control': human_data[human_data['Label'] == 'control']['Average Sequential Distance Word 0'].mean(),
    'Dolphin - Control': chain_dolphin_data[chain_dolphin_data['Label'] == 'control']['Average Sequential Distance Word 0'].mean(),
    'Human - Patient': human_data[human_data['Label'] == 'patient']['Average Sequential Distance Word 0'].mean(),
    'Dolphin - Patient': chain_dolphin_data[chain_dolphin_data['Label'] == 'patient']['Average Sequential Distance Word 0'].mean()
}

# Adjust means for grouping
means_naive_adjusted = {
    'Control - Human': means_naive['Human - Control'],
    'Control - Dolphin': means_naive['Dolphin - Control'],
    'Patient - Human': means_naive['Human - Patient'],
    'Patient - Dolphin': means_naive['Dolphin - Patient']
}

means_chain_adjusted = {
    'Control - Human': means_chain['Human - Control'],
    'Control - Dolphin': means_chain['Dolphin - Control'],
    'Patient - Human': means_chain['Human - Patient'],
    'Patient - Dolphin': means_chain['Dolphin - Patient']
}

means_react_adjusted = {
    'Control - Human': means['Human - Control'],
    'Control - Dolphin': means['Dolphin - Control'],
    'Patient - Human': means['Human - Patient'],
    'Patient - Dolphin': means['Dolphin - Patient']
}

# Combine the means for each category and technique
means_naive_combined = {
    'Control': [means_naive['Human - Control'], means_naive['Dolphin - Control']],
    'Patient': [means_naive['Human - Patient'], means_naive['Dolphin - Patient']]
}

means_chain_combined = {
    'Control': [means_chain['Human - Control'], means_chain['Dolphin - Control']],
    'Patient': [means_chain['Human - Patient'], means_chain['Dolphin - Patient']]
}

means_react_combined = {
    'Control': [means['Human - Control'], means['Dolphin - Control']],
    'Patient': [means['Human - Patient'], means['Dolphin - Patient']]
}

# Define colors
colors_human_dolphin = ['#9bd73f', '#2c6c8c', '#9bd73f', '#2c6c8c']
bar_width = 0.4
positions_control = np.array([0, 0.4])
positions_patient = np.array([1, 1.4])

# Create bar plots for each technique with improved dashed lines using Line2D and updated legend
fig, axs = plt.subplots(3, 1, figsize=(15, 15))

# Font sizes
title_fontsize = 30
label_fontsize = 25
text_fontsize = 20
legend_fontsize = 20

# Function to add dashed lines using Line2D with black outlines
def add_dashed_line(ax, positions, values, colors):
    for pos, val, color in zip(positions, values, colors):
        line = Line2D([pos, pos + 0.8], [val, val], linestyle='--', color=color, linewidth=4, alpha=0.7, zorder=1)
        ax.add_line(line)

# Plot for Naive technique
bars_naive_control = axs[0].bar(positions_control, means_naive_combined['Control'], color=colors_human_dolphin[:2], width=bar_width)
bars_naive_patient = axs[0].bar(positions_patient, means_naive_combined['Patient'], color=colors_human_dolphin[2:], width=bar_width)
add_dashed_line(axs[0], positions_control, means_naive_combined['Control'], colors_human_dolphin[:2])
axs[0].set_ylabel('Semantic Distance', fontsize=label_fontsize-4)
axs[0].text(1.815, max(means_naive_combined['Patient']) * 0.95, 'Naive', fontsize=text_fontsize, verticalalignment='top', horizontalalignment='right')
axs[0].set_xticks([])
axs[0].grid(False)

# Plot for Chain technique
bars_chain_control = axs[1].bar(positions_control, means_chain_combined['Control'], color=colors_human_dolphin[:2], width=bar_width)
bars_chain_patient = axs[1].bar(positions_patient, means_chain_combined['Patient'], color=colors_human_dolphin[2:], width=bar_width)
add_dashed_line(axs[1], positions_control, means_chain_combined['Control'], colors_human_dolphin[:2])
axs[1].set_ylabel('Semantic Distance', fontsize=label_fontsize-4)
axs[1].text(1.815, max(means_chain_combined['Patient']) * 0.95, 'Chain', fontsize=text_fontsize, verticalalignment='top', horizontalalignment='right')
axs[1].set_xticks([])
axs[1].grid(False)

# Plot for React technique
bars_react_control = axs[2].bar(positions_control, means_react_combined['Control'], color=colors_human_dolphin[:2], width=bar_width)
bars_react_patient = axs[2].bar(positions_patient, means_react_combined['Patient'], color=colors_human_dolphin[2:], width=bar_width)
add_dashed_line(axs[2], positions_control, means_react_combined['Control'], colors_human_dolphin[:2])
axs[2].set_ylabel('Semantic Distance', fontsize=label_fontsize-4)
axs[2].text(1.815, max(means_react_combined['Patient']) * 0.95, 'React', fontsize=text_fontsize, verticalalignment='top', horizontalalignment='right')
axs[2].set_xticks([0.2, 1.2])
axs[2].set_xticklabels(['Control', 'Patient'], fontsize=label_fontsize)
axs[2].grid(False)

# Set overall title
fig.suptitle('Proof of Concept', fontsize=title_fontsize, fontweight='bold')

if model == "mistral":
    model_tag = "Mistral"
elif model == "llama":
    model_tag = "LlaMA-2 hf"
elif model == "dolphin":
    model_tag = "Dolphin"
elif model == "gpt-3.5-turbo":
    model_tag = "GPT-3.5 Turbo"
elif model == "gemma":
    model_tag = "Gemma"

# Create the legend above the first row
legend_elements = [
    Line2D([0], [0], color=colors_human_dolphin[0], linestyle='--', linewidth=4, label='Human Reference', alpha=0.7),
    Line2D([0], [0], color=colors_human_dolphin[1], linestyle='--', linewidth=4, label=f'{model_tag} Reference', alpha=0.7),
    Line2D([0], [0], color=colors_human_dolphin[0], marker='s', linestyle='None', markersize=10, label='Human', markerfacecolor=colors_human_dolphin[0]),
    Line2D([0], [0], color=colors_human_dolphin[1], marker='s', linestyle='None', markersize=10, label=f'{model_tag}', markerfacecolor=colors_human_dolphin[1])
]
fig.legend(handles=legend_elements, loc='upper center', ncol=4, fontsize=legend_fontsize, bbox_to_anchor=(0.5, 0.95))

# Show the plot
plt.tight_layout(rect=[0, 0.03, 1, 0.94])

# Save the plot
plt.savefig(f'experiments/experiment_3/figs/{model}/exp3_{model}_{temperature}.png')