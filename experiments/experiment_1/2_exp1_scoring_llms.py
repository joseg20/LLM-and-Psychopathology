import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_and_process_data(models, techniques, temperature):
    all_data = pd.DataFrame()
    for model in models:
        for technique in techniques:
            file_path = f'experiments/experiment_1/results/{model}/scores_{technique}_{model}_{temperature}.csv'
            model_data = pd.read_csv(file_path)
            model_data['Model'] = model
            model_data['Technique'] = technique
            all_data = pd.concat([all_data, model_data], ignore_index=True)
            print(model, technique)
    return all_data

def process_model_technique_data(all_data, models, techniques, pathologies_i):
    model_technique_specific_scores = {}
    for model in models:
        for technique in techniques:
            df = all_data[(all_data['Model'] == model) & (all_data['Technique'] == technique)]

            cols_to_include = df.select_dtypes(include=[np.number]).columns.tolist()
            df_means = df.groupby('Induced Pathology')[cols_to_include].mean().reset_index()
            df_stds = df.groupby('Induced Pathology')[cols_to_include].std().reset_index()

            df_means['Induced Pathology'] = pd.Categorical(df_means['Induced Pathology'], categories=pathologies_i, ordered=True)
            df_means.sort_values('Induced Pathology', inplace=True)
            df_means.reset_index(drop=True, inplace=True)

            df_stds['Induced Pathology'] = pd.Categorical(df_stds['Induced Pathology'], categories=pathologies_i, ordered=True)
            df_stds.sort_values('Induced Pathology', inplace=True)
            df_stds.reset_index(drop=True, inplace=True)

            df_no_no_pathology = df_means[df_means['Induced Pathology'] != 'No Pathology']
            no_pathology_row = df_means.loc[df_means['Induced Pathology'] == 'No Pathology']
            no_pathology_scores_corrected = no_pathology_row.iloc[0][1:-1]

            pathologies = df_no_no_pathology['Induced Pathology']
            own_pathology_scores = df_no_no_pathology.apply(lambda row: row[row['Induced Pathology']], axis=1)
            own_pathology_scores = own_pathology_scores.reset_index(drop=True)

            std_errors = df_stds[df_stds['Induced Pathology'] != 'No Pathology'].reset_index(drop=True)
            std_errors = std_errors.apply(lambda row: row[row['Induced Pathology']], axis=1)
            no_pathology_std = df_stds.loc[df_stds['Induced Pathology'] == 'No Pathology'].iloc[0, 1:-1]

            model_technique_specific_scores[(model, technique)] = {
                'own_pathology_scores': own_pathology_scores,
                'std_errors': std_errors,
                'no_pathology_std': no_pathology_std,
                'no_pathology_scores_corrected': no_pathology_scores_corrected
            }

            print(f"Model: {model}, Technique: {technique}")
    return model_technique_specific_scores

def create_final_dataframe(model_technique_specific_scores, pathologies):
    data_for_csv = []
    for (model, technique), data in model_technique_specific_scores.items():
        for pathology in pathologies:
            index = pathologies.index(pathology)
            own_score = data['own_pathology_scores'][index]
            std_error = data['std_errors'][index]
            row = {
                'Model': model,
                'Technique': technique,
                'Pathology': pathology,
                'Own Pathology Score': own_score,
                'Standard Error': std_error
            }
            if 'no_pathology_scores_corrected' in data:
                row['No Pathology Score'] = data['no_pathology_scores_corrected'].get(pathology, None)
                row['No Pathology Standard Error'] = data['no_pathology_std'].get(pathology, None)

            data_for_csv.append(row)

    final_df = pd.DataFrame(data_for_csv)
    return final_df

def prepare_data_for_plotting(df):
    pathologies = df['Pathology'].unique()
    data = {
        'naive': {'own': {}, 'no': {}, 'own_err': {}, 'no_err': {}},
        'chain': {'own': {}, 'no': {}, 'own_err': {}, 'no_err': {}},
        'react': {'own': {}, 'no': {}, 'own_err': {}, 'no_err': {}}
    }
    for _, row in df.iterrows():
        technique = row['Technique']
        pathology = row['Pathology']
        model = row['Model']
        own_score = row['Own Pathology Score']
        own_err = row['Standard Error']
        no_score = row['No Pathology Score']
        no_err = row['No Pathology Standard Error']
        if pathology not in data[technique]['own']:
            data[technique]['own'][pathology] = {}
            data[technique]['no'][pathology] = {}
            data[technique]['own_err'][pathology] = {}
            data[technique]['no_err'][pathology] = {}
        data[technique]['own'][pathology][model] = own_score
        data[technique]['no'][pathology][model] = no_score
        data[technique]['own_err'][pathology][model] = own_err
        data[technique]['no_err'][pathology][model] = no_err
    return data, pathologies

def create_plot(data, pathologies, df, temperature):
    fig, axs = plt.subplots(3, 1, figsize=(20, 18), sharex=True)
    group_spacing = 1.0
    cmap = plt.cm.viridis
    alturas_indicadores = {
        'Depression': 0.5,
        'Trait Anxiety': 0.3,
        'Eating Disorder': 0.256,
        'Alcohol Addiction': 0.5,
        'Impulsivity': 0.467,
        'Schizophrenia': 0.461,
        'Obsessive Compulsive Disorder': 0.399,
        'Apathy': 0.389,
        'Social Anxiety': 0.444
    }
    for i, technique in enumerate(['naive', 'chain', 'react']):
        ax = axs[i]
        x_positions = [j * (len(df['Model'].unique()) * 2 + group_spacing) for j in range(len(pathologies))]
        for j, pathology in enumerate(pathologies):
            own_scores = [data[technique]['own'][pathology][model] for model in df['Model'].unique()]
            own_errors = [data[technique]['own_err'][pathology][model] for model in df['Model'].unique()]
            no_scores = [data[technique]['no'][pathology][model] for model in df['Model'].unique()]
            no_errors = [data[technique]['no_err'][pathology][model] for model in df['Model'].unique()]
            x_own = [x_positions[j] + k * 0.8 for k in range(len(own_scores))]
            x_no = [x_positions[j] + len(own_scores) * 0.8 + k * 0.8 for k in range(len(no_scores))]
            for k, model in enumerate(df['Model'].unique()):
                own_color = cmap(k / (len(df['Model'].unique()) - 1))
                no_color = cmap(k / (len(df['Model'].unique()) - 1))
                ax.bar(x_own[k], own_scores[k], width=0.8, color=own_color, yerr=np.array([[0], [own_errors[k]]]), capsize=0, error_kw={'elinewidth': 1, 'capthick': 1}, bottom=0, label=model if i == 0 and j == 0 else "", zorder=2)
                ax.bar(x_no[k], no_scores[k], width=0.8, color=no_color, yerr=np.array([[0], [no_errors[k]]]), capsize=0, error_kw={'elinewidth': 1, 'capthick': 1}, bottom=0, hatch='///', edgecolor='white', zorder=2)
            ax.plot([x_own[0] - 0.3, x_no[-1] + 0.3], [alturas_indicadores[pathology], alturas_indicadores[pathology]], color='red', linewidth=1.5, label="Diagnostic Reference" if i == 0 and j == 0 else "", zorder=3)

        ax.set_xticks([x + len(df['Model'].unique()) * 0.7 for x in x_positions])
        labels = ['OCD' if pathology == 'Obsessive Compulsive Disorder' else pathology for pathology in pathologies]
        labels = [label.replace(' ', '\n') if len(label.split()) > 1 else label for label in labels]
        ax.set_xticklabels(labels, rotation=0, ha='center', fontsize=19)
        ax.tick_params(axis='y', labelsize=17)
        if technique == 'naive':
            technique_label = "Naive"
        elif technique == 'chain':
            technique_label = "Chain"
        elif technique == 'react':
            technique_label = "React"
        ax.text(0.98, 0.95, technique_label, transform=ax.transAxes, ha='right', va='top', fontsize=20)
        ax.set_ylim(bottom=0)

    fig.text(0.015, 0.56, 'Pathology Scoring', ha='center', va='center', rotation='vertical', fontsize=24)
        

    legend_elements = [plt.Rectangle((0, 0), 1, 1, facecolor='gray', edgecolor='white', hatch='///', label='No Pathology')]
    model_names = {
        'gpt-3.5-turbo': 'GPT 3.5 Turbo',
        'mistral': 'Mistral',
        'dolphin': 'Dolphin',
        'llama': 'LLaMA-2 HF',
        'gemma': 'Gemma'
    }

    legend_elements.extend([plt.Rectangle((0, 0), 1, 1, facecolor=cmap(k / (len(df['Model'].unique()) - 1)), edgecolor='black', label=model_names.get(model, model)) for k, model in enumerate(df['Model'].unique())])
    legend_elements.append(plt.Line2D([0], [0], color='red', lw=1.5, label='Diagnostic Reference'))

    axs[0].legend(handles=legend_elements, bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=len(df['Model'].unique()) + 2, mode="expand", borderaxespad=0., fontsize=17)
    axs[0].set_title(f'Pathology Scoring ({temperature})', fontsize=24, y=1.25)

    plt.tight_layout()
    plt.subplots_adjust(top=0.88, bottom=0.1, left=0.055)
    plt.savefig(f'experiments/experiment_1/figs/scoring/scoring_{temperature}.png')
    plt.show()


def main():
    print(os.getcwd())
    os.chdir("..")
    os.chdir("..")
    print(os.getcwd())
    print(os.listdir())

    models = ["gpt-3.5-turbo", "mistral", "dolphin", "llama", "gemma"]
    techniques = ["naive", "chain", "react"]
    temperatures = [0.7, 0.9, 0.3]
    for temperature in temperatures:

        pathologies_i = [
            "No Pathology",
            "Depression",
            "Trait Anxiety",
            "Eating Disorder",
            "Alcohol Addiction",
            "Impulsivity",
            "Schizophrenia",
            "Obsessive Compulsive Disorder",
            "Apathy",
            "Social Anxiety",
        ]

        all_data = load_and_process_data(models, techniques, temperature)
        model_technique_specific_scores = process_model_technique_data(all_data, models, techniques, pathologies_i)
        pathologies = [path for path in all_data['Induced Pathology'].unique() if path != 'No Pathology']
        final_df = create_final_dataframe(model_technique_specific_scores, pathologies)
        data, pathologies = prepare_data_for_plotting(final_df)
        create_plot(data, pathologies, final_df, temperature=temperature)

if __name__ == "__main__":
    main()