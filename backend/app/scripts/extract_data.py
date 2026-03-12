import pandas as pd
import json
import os

def export_to_json():
    input_filename = 'CLASE_A_CATEGORÍA_I - NUEVO.xlsx'
    output_path = '/home/hersimmar/Documents/theoric-examen-app/backend/app/seed/data_sc.json'
    
    # Load the data
    df = pd.read_excel(input_filename)
    df.columns = df.columns.str.strip()
    
    formatted_data = []
    
    for _, row in df.iterrows():
        entry = {
            "id": int(row['ID']),
            "tipo_materia": row['TIPO DE MATERIA'],
            "clase_categoria": row['CLASE / CATEGORIA'],
            "tema": row['TEMA'],
            "pregunta": row['DESCRIPCIÓN DE LA PREGUNTA'],
            "alternativas": {
                "a": row['ALTERNATIVA 1'],
                "b": row['ALTERNATIVA 2'],
                "c": row['ALTERNATIVA 3'],
                "d": row['ALTERNATIVA 4']
            },
            "respuesta": row['RESPUESTA']
        }
        formatted_data.append(entry)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(formatted_data, f, indent=2, ensure_ascii=False)
    
    print(f"File saved successfully at: {output_path}")

if __name__ == "__main__":
    export_to_json()