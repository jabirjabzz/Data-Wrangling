import json
import re
import os
from transformers import MarianMTModel, MarianTokenizer
from tqdm import tqdm

# Define translation functions
def load_model_and_tokenizer(model_path):
    try:
        tokenizer = MarianTokenizer.from_pretrained(model_path)
        model = MarianMTModel.from_pretrained(model_path)
        return tokenizer, model
    except Exception as e:
        print(f"Error loading model/tokenizer from {model_path}: {e}")
        return None, None

def translate_text(text, tokenizer, model):
    try:
        inputs = tokenizer([text], return_tensors="pt", max_length=512, truncation=True)
        translated_tokens = model.generate(**inputs)
        return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    except Exception as e:
        print(f"Translation error: {e}")
        return None

def back_translate(content, ml_en_path, en_ml_path):
    try:
        ml_en_tokenizer, ml_en_model = load_model_and_tokenizer(ml_en_path)
        en_ml_tokenizer, en_ml_model = load_model_and_tokenizer(en_ml_path)

        if ml_en_tokenizer is None or ml_en_model is None or en_ml_tokenizer is None or en_ml_model is None:
            return None

        intermediate = translate_text(content, ml_en_tokenizer, ml_en_model)
        if intermediate is None:
            return None
        print("Intermediate (English):", intermediate)

        back_translated = translate_text(intermediate, en_ml_tokenizer, en_ml_model)
        if back_translated is None:
            return None
        print("Back-translated content (Malayalam):", back_translated)

        return back_translated
    except Exception as e:
        print("Back-translation error:", e)
        return None

# Preprocessing functions
def preprocess_content(content):
    if content is None:
        return ""
    content = re.sub(r"[^a-zA-Z\u0D00-\u0D7F\s]", "", content)  # Malayalam range
    content = re.sub(r"\s+", " ", content).strip()
    return content

# Augmentation pipeline
def augment_text(content, ml_en_path, en_ml_path):
    preprocessed = preprocess_content(content)
    if not preprocessed:
        return ""
    return back_translate(preprocessed, ml_en_path, en_ml_path)

# File paths
input_file = r"C:\Users\Administrator\Documents\GitHub\Text_cleaning\data\output_data\root2\processed_output.jsonl"
output_file = r"C:\Users\Administrator\Documents\GitHub\Text_cleaning\data\output_data\root2\augmented_malayalam_data.json"  
ml_en_path = r"C:\Users\Administrator\Documents\GitHub\ml-models\malayalam_back-translation\ml-en"
en_ml_path = r"C:\Users\Administrator\Documents\GitHub\ml-models\malayalam_back-translation\en-ml"

# Create output directory
os.makedirs(os.path.dirname(output_file), exist_ok=True)

augmented_data = []  # List to store augmented data

try:
    with open(input_file, "r", encoding="utf-8") as infile:
        for line in tqdm(infile, desc="Processing lines"):  # Iterate through lines
            try:
                item = json.loads(line)  # Load each line as JSON
                if "text" in item:
                    original_text = item["text"]
                    preprocessed_text = preprocess_content(original_text)
                    if preprocessed_text:
                        augmented_text = augment_text(preprocessed_text, ml_en_path, en_ml_path)
                        augmented_data.append({"original": original_text, "augmented": augmented_text if augmented_text else original_text})
                    else:
                        augmented_data.append({"original": original_text, "augmented": original_text})
                else:
                    print("Warning: 'text' key not found in a line. Skipping.")
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError in line: {line.strip()}: {e}") #print the problematic line
                continue  # Skip to the next line if there's a JSON error

    if augmented_data:
        with open(output_file, "w", encoding="utf-8") as outfile:
            json.dump(augmented_data, outfile, ensure_ascii=False, indent=4)
        print("Data augmentation complete. Augmented file saved to:", output_file)
    else:
        print("No data was augmented. Check your input data.")

except FileNotFoundError:
    print(f"Error: Input file not found: {input_file}")
except PermissionError:
    print(f"Error: Permission denied to write to output file: {output_file}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
