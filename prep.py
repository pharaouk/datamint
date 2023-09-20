import pandas as pd

def convert_csv_to_jsonl(csv_file_path, jsonl_file_path):
    # Read the CSV data
    data = pd.read_csv(csv_file_path)

    # Convert and save DataFrame to JSONL
    data.to_json(jsonl_file_path, orient='records', lines=True)

# Usage
convert_csv_to_jsonl('dfsample2.csv', 'dfsample2.jsonl')