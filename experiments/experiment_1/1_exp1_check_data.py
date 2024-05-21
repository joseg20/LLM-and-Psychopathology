import os
import pandas as pd

# Current work
print(os.getcwd())
# Change directory 2 levels up
os.chdir("..")
os.chdir("..")
print(os.getcwd())
# Look for the file in the directory
print(os.listdir())

models = ["gpt-3.5-turbo", "mistral", "dolphin", "llama", "gemma"]
tecniques = ["naive", "chain", "react"]

#0 gpt
#1 mistral
#2 dolphin
#3 llama
#4 alpaca

model= models[0]
temperatures= [0.3,0.7,0.9]
for tecnique in tecniques:
    for set_temperature in temperatures:
        csv_file = f'experiments/experiment_1/results/{model}/scores_{tecnique}_{model}_{set_temperature}.csv'

        df = pd.read_csv(csv_file)

        numeric_columns = df.columns[:-2]

        print(f"Checking {csv_file}")

        for column in numeric_columns:
            df[column] = pd.to_numeric(df[column], errors='coerce')

        for index, row in df.iterrows():
            for column in numeric_columns:
                value = row[column]
                if value < 0 or value > 1:
                    print(f"Out of range value found: {value} in row {index + 1}, column '{column}'")

        print("All values are within the expected range")

        iteration_counts = df['Iteration'].value_counts().sort_index()

        iterations_more_than_10 = iteration_counts[iteration_counts > 10]
        print(iterations_more_than_10)
