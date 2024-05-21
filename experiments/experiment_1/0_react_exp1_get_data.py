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
import re

def get_last_iteration(filename):
    try:
        df = pd.read_csv(filename)
        return df['Iteration'].max() + 1
    except FileNotFoundError:
        return 1

temperatures = [0.3]
models = ["gpt-3.5-turbo", "mistral", "dolphin", "llama", "gemma"]
#0 gpt
#1 mistral
#2 dolphin
#3 llama
#4 gemma
model= models[-2]
prompt_technique = "react"

max_iteration = 56

pp = Prompting("include/tests")
if model == "gpt-3.5-turbo":
    llm = GptModel()
elif model == "dolphin":
    llm = Dolphin()
elif model == "mistral":
    llm = Mistral()
elif model == "llama":
    llm = LlaMA()
elif model == "gemma":
    llm = Gemma()

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
    csv_filename = f"experiments/experiment_1/results/{model}/ASDASD{prompt_technique}_{model}_{set_temperature} copy 2.csv"
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
                prompt = prompting_function(induced_pathology, tested_pathology, exp_1=True, filter=False)

                context_prompt = prompt[0]
                questions_dict = prompt[1]
                responses_dict={}
                for question_number, question_text in questions_dict.items():
                    attempt = 0
                    print(question_number,question_text,"\n")
                    while attempt < 500:
                        response = llm.query(context=context_prompt, question=question_text, max_tokens=1000, temperature=set_temperature)
                        print(response, "\n---------\n")
                        print(attempt,"\n------------\n")
                        print(responses_dict,"\n------------\n")
                        if tested_pathology == "Social Anxiety":
                            regex_patterns = [
                                r"Final Response: \(([A-D])\)\s*-?\s*\(([A-D])\)",
                                r"Final Response: \(([A-D])\)\s*\w*\s*-?\s*\(([A-D])\)\s*\w*",
                                r"Final Response: ([A-D])\s*-?\s*([A-D])",
                                r"Final Response: \(([A-D])\) - \(([A-D])\)",
                                r"Final Response: \(([A-D])\)-\(([A-D])\)"
                            ]

                            for regex in regex_patterns:
                                match = re.search(regex, response, flags=re.DOTALL)
                                print(match)
                                if match:
                                    label = match.group(1)
                                    label2 = match.group(2)
                                    responses_dict[question_number] = (label, label2)
                                    break
                            if match:
                                break
                        
                        else:
                            match = re.search(r"Final Response: \((.)\)", response)
                            if match:
                                responses_dict[question_number] = match.group(1)
                                break
                        attempt += 1

                for question_number in questions_dict:
                    if question_number not in responses_dict:
                        responses_dict[question_number] = "No Response"
                if tested_pathology == "Social Anxiety":
                    response_string = "\n".join([f"{key}. ({value[0]}) - ({value[1]})" for key, value in sorted(responses_dict.items(), key=lambda item: int(item[0]))])
                else:
                    response_string = "\n".join([f"{key}. ({value})" for key, value in sorted(responses_dict.items(), key=lambda item: int(item[0]))])
                print(f"Response generated: '{response_string}'", "\n")

                print(f"Scoring response for '{tested_pathology}'...", "\n")
                scoring_function = getattr(
                    ps, tested_pathology.lower().replace(" ", "_") + "_scoring"
                )
                scoring_result = scoring_function(response_string)
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
