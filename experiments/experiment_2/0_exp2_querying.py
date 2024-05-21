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
import re

def text_to_dictionary(text, react=False):
    result_dictionary = {}
    lines = text.split('\n')

    if react:
        capture = False
        for line in lines:
            if re.match(r"Final Response[:\s]*", line) or capture:
                capture = True
                line_content = re.sub(r"^Final Response[:\s]*-?", "", line).strip()
                if line_content: 
                    key_value = re.split(r":\s*", line_content, 1)
                    if len(key_value) == 2:
                        key, value = key_value
                        key = key.lstrip('- ').strip()
                        result_dictionary[key] = [val.strip() for val in value.split(',')]
                elif line.strip() == "":  
                    if len(result_dictionary) == 10 and all(len(value) == 10 for value in result_dictionary.values()):
                        break  
                    capture = False 

def realizar_consulta_y_verificar(prompt_function, pathology, item, sublist, temperature, react=False, llm=None, filter=True):
    if react == False:
        while True:
            prompt = prompt_function(
                induced_pathology=pathology,
                tested_pathology=pathology,
                exp_2=True,
                word_list=sublist,
                filter=filter)
            print("------------\n", prompt)
            llm_response = llm.query(prompt, max_tokens=2500, temperature=temperature)
            print(llm_response)
            dict_results = text_to_dictionary(llm_response, react=react)
            print("-----------\n", dict_results)
            if all(len(v) == 10 for v in dict_results.values()) and len(dict_results) == 10:
                return dict_results
            else:
                print(f'The response for "{pathology}" and "{item}" does not meet the requirements. Repeating the query...')
    else:
        while True:
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
                attempt = 0
                success = False  
                while attempt < 100 and not success:
                    try:
                        print("------------\n", prompt)
                        response = llm.query(context=context_prompt, question=f"The surveyed word is: {word}", max_tokens=700, temperature=temperature)
                        print("-----------\n", response)
                        final_response_section = response.split("Final Response:")[-1].strip()
                        if ":" in final_response_section:  
                            key_word, words_str = final_response_section.split(":", 1)
                            words = [word.strip().rstrip(".") for word in words_str.split(",")] 
                            words = words[:10]
                            key_word = key_word.strip()
                            print(key_word, ":", words)
                            if len(words) == 10 and all(len(w) <= 20 and "\\n" not in w for w in words):
                                dict_results[word] = words
                                success = True  
                            else:
                                raise ValueError("Invalid word format: contains '\\n' or exceeds 20 characters.") 
                        else:
                            raise ValueError("No ':' found in response, causing unpacking to fail.")
                    except ValueError as e:
                        print(f"Error: {e}. Intentando de nuevo...")
                        attempt += 1  
                
                if not success:
                    print (f'Not all words have been successfully queried for "{pathology}" and "{item}". Repeating the query...')
                    
            if len(dict_results) == 10:
                return dict_results
            else:
                print(f'The response for "{pathology}" and "{item}" does not meet the requirements. Repeating the query...')


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
prompt_technique = "chain"
if prompt_technique == "react":
    react = True
else:
    react = False
temperature = 0.7
csv_filename = f"experiments/experiment_2/results/results_{prompt_technique}_{model}_{temperature}-3.csv"

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
                            pathology, f"{item}-{sublist_type}-{index}", words, temperature, react, llm, filter
                        )
                        for surveyed_word, related_words in dict_results.items():
                            writer.writerow([
                                pathology, f"{item}-{sublist_type}", surveyed_word, *related_words, iteration
                            ])


                        
