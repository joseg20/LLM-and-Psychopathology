import os
import sys
import csv

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
from data.words import *

def realizar_consulta_y_verificar(prompt_function, pathology, item, sublist, temperature, llm=None, filter=True):
    dict_results = {}
    prompt = prompt_function(
        induced_pathology=pathology,
        tested_pathology=pathology,
        exp_2=True,
        word_list=sublist,
        filter=filter)
    context_prompt = prompt[0]
    words = prompt[1]
    
    for word in words:
        while True:
            response = llm.query(context=context_prompt, question=f"The surveyed word is: {word}", max_tokens=700, temperature=temperature)
            print(response)
            
            final_response_start = response.find("Final Response:")
            if final_response_start != -1:
                final_response_text = response[final_response_start + len("Final Response:"):].strip()
                final_response_words = [w.strip() for w in final_response_text.split(',')]
                
                if any(len(w) > 20 or '\n' in w for w in final_response_words):
                    print(f"Revisiting the word {word} due to length or newline.")
                    continue
                
                if len(final_response_words) > 10:
                    final_response_words = final_response_words[:10]
                elif len(final_response_words) < 10:
                    final_response_words.extend([''] * (10 - len(final_response_words)))
                print(word, final_response_words)
                dict_results[word] = final_response_words
                break 

    return dict_results



pp = Prompting("include/tests")

ps = PathologyScoring()

results_dict = {}

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

model = "llama"
prompt_technique = "react"
if prompt_technique == "react":
    react = True
else:
    react = False
temperature = 0.7
csv_filename = f"experiments/experiment_2/results/results_{prompt_technique}_{model}_{temperature}bbaauujjht.csv"

if model == "gpt-3.5-turbo":
    llm = GptModel()
    filter = True
elif model == "mistral":
    llm = Mistral()
    filter = False
elif model == "dolphin":
    llm = Dolphin()
    filter = False
elif model == "llama":
    llm = LlaMA()
    filter = True
elif model == "gemma":
    llm = Gemma()
    filter=False

def get_last_iteration(csv_file):
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            last_line = list(csv.reader(f))[-1]
            last_iteration = int(last_line[-1]) 
            print(f"Última iteración encontrada: {last_iteration}")
        return last_iteration
    except FileNotFoundError:
        return 0  
    except IndexError:
        return 0 
start_iteration = get_last_iteration(csv_filename) + 1

# MATERIAL_WELL_BEING
concrete_items_MWB = MATERIAL_WELL_BEING["Concrete"]
concrete_sublists_MWB = [concrete_items_MWB[i:i+10] for i in range(0, len(concrete_items_MWB), 10)]
abstract_items_MWB = MATERIAL_WELL_BEING["Abstract"]
abstract_sublists_MWB = [abstract_items_MWB[i:i+10] for i in range(0, len(abstract_items_MWB), 10)]

#HEALTH
concrete_items_H = HEALTH["Concrete"]
concrete_sublists_H = [concrete_items_H[i:i+10] for i in range(0, len(concrete_items_H), 10)]
abstract_items_H = HEALTH["Abstract"]
abstract_sublists_H = [abstract_items_H[i:i+10] for i in range(0, len(abstract_items_H), 10)]

#PRODUCTIVITY
concrete_items_P = PRODUCTIVITY["Concrete"]
concrete_sublists_P = [concrete_items_P[i:i+10] for i in range(0, len(concrete_items_P), 10)]
abstract_items_P = PRODUCTIVITY["Abstract"]
abstract_sublists_P = [abstract_items_P[i:i+10] for i in range(0, len(abstract_items_P), 10)]

#INTIMACY
concrete_items_I = INTIMACY["Concrete"]
concrete_sublists_I = [concrete_items_I[i:i+10] for i in range(0, len(concrete_items_I), 10)]
abstract_items_I = INTIMACY["Abstract"]
abstract_sublists_I = [abstract_items_I[i:i+10] for i in range(0, len(abstract_items_I), 10)]

items = ['MWB', 'H', 'P', 'I']

iterations = 100

results_dict = {}

with open(csv_filename, mode='a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    if start_iteration == 1:
        writer.writerow(['Induced Pathology', 'Category', 'Surveyed Word', 'Related 1', 'Related 2', 'Related 3', 'Related 4', 'Related 5', 'Related 6', 'Related 7', 'Related 8', 'Related 9', 'Related 10', 'Iteration'])

    for iteration in range(start_iteration, 101):
        print(f"Iteración {iteration} de 100")
        for pathology in pathologies_induced:
            for item in ['MWB', 'H', 'P', 'I']:
                concrete_sublist = locals()[f'concrete_sublists_{item}']
                abstract_sublist = locals()[f'abstract_sublists_{item}']

                for sublist_type, sublist in [('C', concrete_sublist), ('A', abstract_sublist)]:
                    for index, words in enumerate(sublist, start=1):
                        dict_results = realizar_consulta_y_verificar(
                            getattr(pp, f"{prompt_technique}_prompting"),
                            pathology, f"{item}-{sublist_type}-{index}", words, temperature, llm, filter
                        )
                        for surveyed_word, related_words in dict_results.items():
                            writer.writerow([
                                pathology, f"{item}-{sublist_type}", surveyed_word, *related_words, iteration
                            ])

