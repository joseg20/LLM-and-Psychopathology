import pandas as pd
import re

def extract_word_general_adjusted(text):
    """Esta función elimina los patrones 'wordx:', deja solo la palabra después de ': ' o ' - ', elimina las palabras repetidas seguidas de ':', deja solo la última palabra si hay un salto de línea, y deja solo la palabra después de ';'."""
    if isinstance(text, str):
        # Eliminar 'wordx:'
        text = re.sub(r"word\d+:\s*", "", text)
        # Dejar solo la palabra después de ': '
        text = re.sub(r"^[^:]+:\s*", "", text)
        # Dejar solo la palabra después de ' - '
        text = re.sub(r"^[^-]+\s-\s*", "", text)
        # Eliminar palabras repetidas seguidas de ':'
        text = re.sub(r"^(\w+)\s*\1\s*:\s*", r"\1", text)
        # Dejar solo la última palabra si hay un salto de línea
        text = re.sub(r".*\n", "", text).strip()
        # Dejar solo la palabra después de ';'
        text = re.sub(r"^[^;]+;\s*", "", text)
        return text
    return text

def main():
    # Asumiendo que el nombre del archivo es 'results_react_dolphin_0.9.csv'
    file_path = '/home/jose/Git/SE-AP/experiments/experiment_2/results/dolphin/results_react_dolphin_0.3.csv'
    output_file_path = '/home/jose/Git/SE-AP/experiments/experiment_2/results/dolphin/results_react_dolphin_0.3a.csv'

    # Cargar el dataset
    data = pd.read_csv(file_path)

    # Aplicar la función para corregir la columna 'Related 1' y otras columnas 'Related'
    related_columns = ['Related 1', 'Related 2', 'Related 3', 'Related 4', 'Related 5',
                       'Related 6', 'Related 7', 'Related 8', 'Related 9', 'Related 10']
    for col in related_columns:
        data[col] = data[col].apply(extract_word_general_adjusted)
        data[col] = data[col].str.lower()  # Convertir a minúsculas solo las columnas 'Related'

    # Guardar los datos corregidos
    data.to_csv(output_file_path, index=False)

    print(f"Archivo guardado como {output_file_path}")

if __name__ == "__main__":
    main()