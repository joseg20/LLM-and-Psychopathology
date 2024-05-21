import pandas as pd
import numpy as np
from gensim import downloader as api
import matplotlib.pyplot as plt
import os
import math
from tqdm import tqdm
from scipy.spatial.distance import cosine

# Current work
print(os.getcwd())
# Change directory 2 levels up
os.chdir("..")
os.chdir("..")
print(os.getcwd())
# Look for the file in the directory
print(os.listdir())

def loadFastTextModel():
    print("Loading FastText Model")
    model = api.load('fasttext-wiki-news-subwords-300')
    print("Done.", len(model.key_to_index), "words loaded!")
    return model

word_vectors = loadFastTextModel()

def pairwise_distance(word, related_words_list, word_vectors):
    distances = []
    if word not in word_vectors:
        word = related_words_list[0]
        if word not in word_vectors:
            return np.nan
    word_vector = word_vectors[word]
    for related_word in related_words_list:
        if related_word in word_vectors:
            related_vector = word_vectors[related_word]
            distance = cosine(word_vector, related_vector)
        else:
            distance = np.nan
        distances.append(distance)
    return np.nanmean(distances)

def remove_duplicates_preserve_order(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def trajectory_distance2(word_list, word_vectors):
    embeddings = {word: word_vectors[word] for word in word_list if word in word_vectors}
    if len(embeddings) < 2:
        return np.nan
    distances = []
    for i in range(len(word_list) - 1):
        word1 = word_list[i]
        word2 = word_list[i + 1]
        if word1 in embeddings and word2 in embeddings:
            distance = cosine(embeddings[word1], embeddings[word2])
            distances.append(distance)
        else:
            distances.append(np.nan)
    distances = [x for x in distances if not math.isnan(x)]
    return np.nanmean(distances)

model_name = "llama"
prompt_techniques = ["naive","chain","react"]
temperatures = [0.3,0.7,0.9]
for prompt_technique in prompt_techniques:
    for temperature in temperatures:
        print(f'experiments/experiment_3/results/words/{model_name}/exp3_{prompt_technique}_{model_name}_{temperature}.csv')
        data = pd.read_csv(f'experiments/experiment_3/results/words/{model_name}/exp3_{prompt_technique}_{model_name}_{temperature}.csv')
        # data = pd.read_csv('experiments/experiment_3/results/words/humandata.csv')
        
        results = []
        for subject in data.columns[1:]: 
            subject_data = data[subject].dropna() 
            subject_data = subject_data.apply(lambda x: str(x).lower())
            subject_data = subject_data.tolist()
            word_0 = subject_data[0]
            if subject == "111" and model_name == "gemma" and temperature == 0.7:
                print(word_0)
                print()
                print(subject_data)
            subject_data = remove_duplicates_preserve_order(subject_data)
            if word_0 in subject_data:
                subject_data.remove(word_0)
            category_word = "animal"
            avg_trajectory_distance2 = trajectory_distance2(subject_data, word_vectors)
            distancesword0 = pairwise_distance(word=word_0, related_words_list=subject_data, word_vectors=word_vectors)
            distancescategory = pairwise_distance(word=category_word, related_words_list=subject_data, word_vectors=word_vectors)
            label = "patient" if int(subject) < 200 else "control"
            results.append({
                'Subject': subject,
                'Label': label,
                'Average Sequential Distance': avg_trajectory_distance2,
                'Average Pairwise Distance Word 0': distancesword0,
                'Average Pairwise Distance Category': distancescategory
            })
        
        results_df = pd.DataFrame(results)
        results_df.to_csv(f'/experiments/experiment_3/results/distances_metrics/{model_name}/exp3_{prompt_technique}_{model_name}_{temperature}_distances.csv', index=False)
