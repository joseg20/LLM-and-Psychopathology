import os
import sys
import csv
import pandas as pd
import re
from tqdm import tqdm

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
from data.subjects import animals_count

pp = Prompting("include/tests")

ps = PathologyScoring()

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
    "Social Anxiety",
]

model = "dolphin"
prompt_technique = "react"
temperature = 0.9

if model == "gpt-3.5-turbo":
    llm = GptModel()
elif model == "mistral":
    llm = Mistral()
elif model == "dolphin":
    llm = Dolphin()
elif model == "llama":
    llm = LlaMA()
elif model == "gemma":
    llm = Gemma()

results = {}

for subject, n_exp3 in tqdm(animals_count['animals'].items(), desc="Procesando sujetos"):
    attempts = 0
    max_attempts = 99  

    if 100 < subject < 200:
        induced_pathology = pathologies_induced[6]
    elif subject >= 200:
        induced_pathology = pathologies_induced[0]

    while attempts < max_attempts:
        attempts += 1

        if prompt_technique == "react":
            
            prompt = pp.react_prompting(
                induced_pathology=induced_pathology,
                exp_3=True,
                n_exp3=n_exp3
            )
            
            response = llm.query(
                context="",
                question=prompt,
                max_tokens=1000,
                temperature=temperature
            )
            
            final_response_match = re.search(r'Final Response:(.*)', response, re.DOTALL)
            
            if final_response_match:
                words = [word.strip() for word in final_response_match.group(1).split(',')]
                
                if len(words) > n_exp3:
                    words = words[:n_exp3]
                
                if len(words) == n_exp3:
                    results[subject] = words
                    break  
                else:
                    print(f'Attempt {attempts}: Obtained {len(words)} words, expected {n_exp3}. Retrying...')
            else:
                words=[]
                print(f'Not found "Final Response" in attempt {attempts}. Retrying...')
        
            if subject not in results:
                results[subject] = words + [''] * (n_exp3 - len(words))
        
        elif prompt_technique == "chain":
            
            prompt = pp.chain_prompting(
                induced_pathology=induced_pathology,
                exp_3=True,
                n_exp3=n_exp3
            )
            
            response = llm.query(
                context="",
                question=prompt,
                max_tokens=1000,
                temperature=temperature
            )
            
            final_response_match = re.search(r'Generated words:(.*)', response, re.DOTALL)
            
            if final_response_match:
                words = [word.strip() for word in final_response_match.group(1).split(',')]
                
                if len(words) > n_exp3:
                    words = words[:n_exp3]
                
                if len(words) == n_exp3:
                    results[subject] = words
                    break  
                else:
                    print(f'Attempt {attempts}: Obtained {len(words)} words, expected {n_exp3}. Retrying...')
            else:
                words=[]
                print(f'Not found "Generated Words" in attempt {attempts}. Retrying...')
        
            if subject not in results:
                results[subject] = words + [''] * (n_exp3 - len(words))

        elif prompt_technique == "naive":
            
            prompt = pp.naive_prompting(
                induced_pathology=induced_pathology,
                exp_3=True,
                n_exp3=n_exp3
            )
            
            response = llm.query(
                context="",
                question=prompt,
                max_tokens=1000,
                temperature=temperature
            )

            final_response_match = re.search(r'Generated words:(.*)', response, re.DOTALL)
            
            if final_response_match:
                words = [word.strip() for word in final_response_match.group(1).split(',')]
                
                if len(words) > n_exp3:
                    words = words[:n_exp3]
                
                if len(words) == n_exp3:
                    results[subject] = words
                    break  
                else:
                    print(f'Attempt {attempts}: Obtained {len(words)} words, expected {n_exp3}. Retrying...')
            else:
                words=[]
                print(f'Not found "Generated Words" in attempt {attempts}. Retrying...')
        
            if subject not in results:
                results[subject] = words + [''] * (n_exp3 - len(words))

csv_filename = f"experiments/experiment_3/results/words/{model}/exp3_{prompt_technique}_{model}_{temperature}.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    writer.writerow(['Subject'] + list(results.keys()))
    
    max_words = max(len(words) for words in results.values())
    
    for i in range(max_words):
        row = ['Word'] 
        for words in results.values():

            row.append(words[i] if i < len(words) else '')
        writer.writerow(row)

print(f'Results saved in {csv_filename}')
