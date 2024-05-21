import pandas as pd

dataname = "experiments/experiment_2/results/dolphin/results_react_dolphin_0.9.csv"

data = pd.read_csv(dataname)


def check_exact_pattern_and_print(df):
    # This function will check for the exact pattern and print the surveyed word and row index
    pattern_rows = []
    for index, row in df.iterrows():
        surveyed_word = row['Surveyed Word']
        # Check each related column for the exact pattern, ensuring strict format match
        pattern_found = all(str(row[f'Related {i}']) == f"{surveyed_word}{i}" for i in range(1, 11))
        if pattern_found:
            pattern_rows.append((surveyed_word, index))
    return pattern_rows

# Apply the function to the dataframe again to find exact matches
exact_pattern_rows = check_exact_pattern_and_print(data)
print(len(exact_pattern_rows))