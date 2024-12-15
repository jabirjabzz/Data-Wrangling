import json
import os
import re

def is_malayalam(text):
    return bool(re.search(r'[\u0D00-\u0D7F]', text))

def clean_text(text):
    # Remove unwanted characters
    text = re.sub(r'\s+', ' ', text)  # Normalize spaces
    text = re.sub(r'[^\u0D00-\u0D7F\s.,!?]', '', text)  # Keep only Malayalam characters and punctuation
    return text.strip()

def process_data(input_dir, output_file):
    processed_data = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".json"):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    content = data.get("content", "")
                    if is_malayalam(content):
                        cleaned_content = clean_text(content)
                        if cleaned_content:
                            processed_data.append(cleaned_content)

    # Remove duplicates
    processed_data = list(set(processed_data))
        # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Save processed data to a JSONL file
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for entry in processed_data:
            out_f.write(json.dumps({"text": entry}, ensure_ascii=False) + '\n')

# Define paths
input_dir = r"C:\Users\Administrator\Documents\GitHub\Text cleaning\data\input_data"
# output_file = r"C:\Users\Administrator\Documents\GitHub\Text cleaning\data\output_data"
output_file = os.path.join("C:\\Users\\Administrator\\Documents\\GitHub\\Text cleaning\\output", "cleaned_data.jsonl")

# Process the data
process_data(input_dir, output_file)
