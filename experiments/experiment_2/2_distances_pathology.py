import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from sklearn.preprocessing import MinMaxScaler
import os
import matplotlib.lines as mlines
import matplotlib.patheffects as path_effects
import numpy as np
# Current work
print(os.getcwd())
# Change directory 2 level up
os.chdir("..")
os.chdir("..")
print(os.getcwd())
# Look for the file in the directory
print(os.listdir())

pathologies_induced = [
    "No Pathology",
    "Depression",
    "Trait Anxiety",
    "Eating Disorder",
    "Alcohol Addiction",
    "Impulsivity", 
    "Schizophrenia",
    "Obsessive Compulsive Disorder",
    "Apathy",
    "Social Anxiety"
]

palette = {
    'Semantic Distance': '#9bd73f',
    'Simplex Volume': '#2c6c8c',
}

temp = 0.3
model = "llama"
ruta_guardado = 'experiments/experiment_2/figs/'    

file_naive = f'experiments/experiment_2/results_with_distances/{model}/results_with_distances_naive_{model}_{temp}_distances.csv'
file_chain = f'experiments/experiment_2/results_with_distances/{model}/results_with_distances_chain_{model}_{temp}_distances.csv'
file_react = f'experiments/experiment_2/results_with_distances/{model}/results_with_distances_react_{model}_{temp}_distances.csv'

df_naive = pd.read_csv(file_naive)
df_chain = pd.read_csv(file_chain)
df_react = pd.read_csv(file_react)

def process_and_normalize(df, label):
    df_std = df[['Average Sequential Distance', 'Simplex Volume']].copy()

    scaler_std = MinMaxScaler()
    df_std[['Average Sequential Distance', 'Simplex Volume']] = scaler_std.fit_transform(
        df_std[['Average Sequential Distance', 'Simplex Volume']]
    )

    grouped_stds = df_std.groupby(df['Induced Pathology'])[['Average Sequential Distance', 'Simplex Volume']].std().reset_index()

    grouped_means = df.groupby('Induced Pathology')[['Average Sequential Distance', 'Simplex Volume']].mean().reset_index()

    scaler = MinMaxScaler()
    grouped_means[['Average Sequential Distance', 'Simplex Volume']] = scaler.fit_transform(
        grouped_means[['Average Sequential Distance', 'Simplex Volume']]
    )

    grouped_ordered = grouped_means.melt(id_vars='Induced Pathology', value_vars=['Average Sequential Distance', 'Simplex Volume'])

    grouped_ordered['Induced Pathology'] = pd.Categorical(grouped_ordered['Induced Pathology'], categories=[p.replace('\n', ' ') for p in pathologies_induced], ordered=True)

    grouped_ordered['Dataset'] = label

    stds_ordered = grouped_stds.melt(id_vars='Induced Pathology', value_vars=['Average Sequential Distance', 'Simplex Volume'])
    stds_ordered['Induced Pathology'] = pd.Categorical(stds_ordered['Induced Pathology'], categories=[p.replace('\n', ' ') for p in pathologies_induced], ordered=True)
    stds_ordered['Dataset'] = label

    return grouped_ordered, stds_ordered

data_naive, stds_naive = process_and_normalize(df_naive, 'Naive')
data_chain, stds_chain = process_and_normalize(df_chain, 'Chain')
data_react, stds_react = process_and_normalize(df_react, 'React')

data = pd.concat([data_naive, data_chain, data_react], axis=0, ignore_index=True)
stds = pd.concat([stds_naive, stds_chain, stds_react], axis=0, ignore_index=True)

datasets = ['Naive', 'Chain', 'React']

fig = plt.figure(figsize=(20, 18))
gs = GridSpec(3, 1, figure=fig, height_ratios=[1, 1, 1])
fig.suptitle('Semantic Expansion', fontsize=24, fontweight='bold', y=0.995)

for i, dataset in enumerate(datasets):
    ax_dataset = fig.add_subplot(gs[i, 0]) 
    data_filtered = data[data['Dataset'] == dataset]
    stds_filtered = stds[stds['Dataset'] == dataset]

    values_dict = {}
    for pathology in pathologies_induced:
        values_dict[pathology] = {}
        for metric in ['Average Sequential Distance', 'Simplex Volume']:
            value = data_filtered[(data_filtered['Induced Pathology'] == pathology.replace('\n', ' ')) & (data_filtered['variable'] == metric)]['value'].values
            values_dict[pathology][metric] = value[0] if len(value) > 0 else 0

    bar_width = 0.35
    x = range(len(pathologies_induced))
    lines = []  
    for k, metric in enumerate(['Average Sequential Distance', 'Simplex Volume']):
        values = [values_dict[pathology][metric] for pathology in pathologies_induced]
        stds_values = stds_filtered[(stds_filtered['Induced Pathology'].isin([p.replace('\n', ' ') for p in pathologies_induced])) & (stds_filtered['variable'] == metric)]['value'].tolist()

        if metric == 'Average Sequential Distance':
            label = f'Semantic Distance'
        else:
            label = f'{metric}'
        color = palette[label]
        ax_dataset.bar([xi + k * bar_width for xi in x], values, width=bar_width, label=label, color=color, yerr=[np.zeros_like(stds_values), stds_values], capsize=4)

        no_pathology_index = pathologies_induced.index('No Pathology')
        no_pathology_value = values_dict['No Pathology'][metric]
        line = mlines.Line2D([no_pathology_index + k * bar_width, len(pathologies_induced)],
                             [no_pathology_value, no_pathology_value],
                             color=color, linestyle='--', linewidth=1.5, label=f'No Pathology Reference - {label}',
                             path_effects=[path_effects.Stroke(linewidth=2, foreground='black'), path_effects.Normal()])
        lines.append(line)

    ax_dataset.set_xticks([xi + bar_width / 2 for xi in x])
    labels = [pathology.replace(' ', '\n') for pathology in pathologies_induced]
    labels = ['OCD' if label == 'Obsessive\nCompulsive\nDisorder' else label for label in labels]
    ax_dataset.set_xticklabels(labels, rotation=0, ha='center', fontsize=18)

    if i != 2: 
        ax_dataset.tick_params(labelbottom=False)  
    ax_dataset.set_ylabel('Normalized Values', fontsize=18)
    ax_dataset.tick_params(axis='y', labelsize=14)

    ax_dataset.text(0.94, 0.98, dataset, transform=ax_dataset.transAxes, ha='left', va='top', fontsize=18)

    for line in lines:
        ax_dataset.add_line(line)

handles, labels = ax_dataset.get_legend_handles_labels()
handles.extend(lines)  
fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.98), ncol=2, fontsize=16)

plt.tight_layout()
plt.subplots_adjust(top=0.93)

plt.savefig(f'{ruta_guardado}{model}/{temp}/exp2_pathology_{model}_{temp}.png')