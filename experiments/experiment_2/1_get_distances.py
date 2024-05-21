import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import gensim.downloader as api
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from tqdm import tqdm
import math

# Current work
print(os.getcwd())

# Change directory 2 level up
os.chdir("..")
os.chdir("..")
print(os.getcwd())

# Look for the file in the directory
print(os.listdir())

def loadGloveModel(gloveFile):
    print("Loading Glove Model")
    f = open(gloveFile,'r', encoding='utf8')
    model = {}
    for line in tqdm(f, desc="Loading words"):
        splitLine = line.split(' ')
        word = splitLine[0]
        embedding = np.asarray(splitLine[1:], dtype='float32')
        model[word] = embedding
    print("Done.", len(model), "words loaded!")
    return model

model = "llama"
prompt_technique = "react"
temperature = 0.3
gloveFile = "/experiments/experiment_2/data/glove.840B.300d.txt"
word_vectors = loadGloveModel(gloveFile)

data = pd.read_csv(f'experiments/experiment_2/results/{model}/results_{prompt_technique}_{model}_{temperature}_cleaned.csv')
data[data['Iteration'] == 1]

from sklearn.metrics.pairwise import cosine_similarity

def sequential_distance(word, related_words_list, word_vectors):
    distances = []
    if word not in word_vectors:
        return [np.nan] * len(related_words_list)
    word_vector = word_vectors[word].reshape(1, -1)
    for related_word in related_words_list:
        if related_word in word_vectors:
            related_vector = word_vectors[related_word].reshape(1, -1)
            distance = cosine_similarity(word_vector, related_vector)[0][0]
        else:
            distance = np.nan
        distances.append(distance)
    return distances

sequential_distances = data.apply(lambda row: sequential_distance(row['Surveyed Word'], [row[f'Related {j}'] for j in range(1, 11)], word_vectors), axis=1)

for i in range(1, 11):
    data[f'Sequential Distance {i}'] = sequential_distances.apply(lambda distances: distances[i-1] if len(distances) >= i else np.nan)

data['Average Sequential Distance'] = data[[f'Sequential Distance {i}' for i in range(1, 11)]].apply(lambda row: row.mean(), axis=1)

data['STD Sequential Distance'] = data[[f'Sequential Distance {i}' for i in range(1, 11)]].apply(lambda row: row.std(), axis=1)

def calculate_simplex_volume(word_list, word_vectors):
    unique_words = list(dict.fromkeys(word_list))
    vectors = [word_vectors.get(word) for word in unique_words if word in word_vectors]
    vectors = np.array([v for v in vectors if v is not None])

    if len(vectors) <= 1:
        return np.nan 

    reference_vector = vectors[0]
    vectors = vectors - reference_vector

    vectors = vectors[1:]

    if vectors.size == 0:
        return 0.0

    gram_matrix = np.dot(vectors, vectors.T)

    rank = np.linalg.matrix_rank(gram_matrix)
    if rank < len(vectors):
        print("Dependencia lineal detectada.")
        return 0.0

    det_gram = np.linalg.det(gram_matrix)
    if det_gram <= 0:
        return 0.0

    volume = math.sqrt(det_gram) / math.factorial(len(vectors))

    return volume

data['Simplex Volume'] = data.apply(lambda row: calculate_simplex_volume([row['Surveyed Word']] + [row[f'Related {j}'] for j in range(1, 11)], word_vectors), axis=1)

data.to_csv(f'experiments/experiment_2/results_with_distances/{model}/results_with_distances_{prompt_technique}_{model}_{temperature}_distances.csv', index=False)