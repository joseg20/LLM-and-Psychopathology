import pandas as pd

# Cargar el archivo CSV
file_path = '/home/jose/Git/SE-AP/experiments/experiment_2/results/mistral/results_react_mistral_0.3.csv'
df = pd.read_csv(file_path)


def clean_multiline_strings(text):

    if isinstance(text, str):

        return text.replace("\n", " ").replace("\r", " ").strip()

    return text


cleaned_df = df.applymap(clean_multiline_strings)

# Guardar el DataFrame resultante en un nuevo archivo CSV
cleaned_file_path = '/home/jose/Git/SE-AP/experiments/experiment_2/results/mistral/results_react_mistral_0.3aa.csv'
df.to_csv(cleaned_file_path, index=False)

# Confirmar la ruta del archivo limpio
cleaned_file_path