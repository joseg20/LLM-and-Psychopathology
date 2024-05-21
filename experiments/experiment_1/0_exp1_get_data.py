import os
import sys
import pandas as pd
import numpy as np

# Current work
print(os.getcwd())
# Change directory 2 level up
os.chdir("..")
os.chdir("..")
print(os.getcwd())
# Look for the file in the directory
print(os.listdir())

sys.path.append(os.getcwd())

from include.pathology_prompting import Prompting
from include.pathology_scoring import PathologyScoring
from models import Dolphin, GptModel, Mistral, LlaMA, Gemma


def get_last_iteration(filename):
    try:
        df = pd.read_csv(filename)
        return df['Iteration'].max() + 1
    except FileNotFoundError:
        return 1
temperatures = [0.9]
models = ["gpt-3.5-turbo", "mistral", "dolphin", "llama", "gemma", "vicuna", "mixstral"]
tecniques = ["naive", "chain", "react"]

#0 gpt
#1 mistral
#2 dolphin
#3 llama
#4 alpaca
model= models[4]
prompt_technique = tecniques[1]

max_iteration = 101

pp = Prompting("include/tests")
if model == "gpt-3.5-turbo":
    llm = GptModel()
elif model == "dolphin":
    llm = Dolphin()
elif model == "mistral":
    llm = Mistral()
elif model == "gemma":
    llm = Gemma()
elif model == "llama":
    llm = LlaMA()

ps = PathologyScoring()

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

pathologies_t = [
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
for set_temperature in temperatures:
    csv_filename = f"experiments/experiment_1/results/{model}/scores_{prompt_technique}_{model}_{set_temperature}.csv"
    starting_iteration = get_last_iteration(csv_filename)
    print(f"Starting iteration: {starting_iteration}", "\n")

    for iteration in range(starting_iteration, max_iteration):
        scores = []

        for induced_pathology in pathologies_i:
            iter_scores = {}

            for tested_pathology in pathologies_t:
                print(
                    f"Testing '{tested_pathology}' using prompt from '{induced_pathology}'...",
                    "\n"
                )
                prompting_function = getattr(pp, f"{prompt_technique}_prompting")
                #print(f"Generating prompt for induced pathology: '{induced_pathology}'...", "\n")
                prompt = prompting_function(induced_pathology, tested_pathology, exp_1=True, filter=False)
                #print(f"Prompt generated: '{prompt}'", "\n")
                if model == "gpt-3.5-turbo":
                    response = llm.query(prompt, max_tokens=3000, temperature=set_temperature, debug=True)
                else:
                    response = llm.query(question=prompt, temperature=set_temperature)
            
                print(f"Response generated: '{response}'", "\n")

                print(f"Scoring response for '{tested_pathology}'...", "\n")
                scoring_function = getattr(
                    ps, tested_pathology.lower().replace(" ", "_") + "_scoring"
                )
                scoring_result = scoring_function(response)
                label = scoring_result[0]
                score = scoring_result[2]
                while not (0 <= score <= 1):
                        print(f"Wrong response generated: '{response}'", "\n")
                        if model == "gpt-3.5-turbo":
                            response = llm.query(question=prompt, max_tokens=3000, temperature=set_temperature, debug=True)                    
                        elif model == "mistral":
                            response = llm.query(question=prompt, temperature =set_temperature)
                        elif model == "dolphin":
                            response = llm.query(question=prompt, temperature=set_temperature)
                        elif model == "llama":
                            response = llm.query(question=prompt, temperature=set_temperature)
                        elif model == "gemma":
                            response = llm.query(question=prompt, temperature=set_temperature)
                        print(f"Scoring response for '{tested_pathology}'...", "\n")
                        scoring_function = getattr(
                            ps, tested_pathology.lower().replace(" ", "_") + "_scoring"
                        )
                        scoring_result = scoring_function(response)
                        label = scoring_result[0]
                        score = scoring_result[2]
                iter_scores[tested_pathology] = score
                print(f"Score for '{tested_pathology}': {score}, Label: '{label}'", "\n")

            iter_scores_row = iter_scores.copy()
            iter_scores_row["Induced Pathology"] = induced_pathology
            iter_scores_row["Iteration"] = iteration
            print(iter_scores_row, induced_pathology, iteration)
            scores.append(iter_scores_row)
            print(f"Test finished, for induced pathology {induced_pathology}", "\n")

        df_scores = pd.DataFrame(scores)
        df_scores.to_csv(csv_filename, mode='a', header=not os.path.exists(csv_filename), index=False)
        print(f"Iteration {iteration} finished, for induced pathology {induced_pathology}", "\n")
