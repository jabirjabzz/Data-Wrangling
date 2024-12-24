import json
import re
from transformers import MarianMTModel, MarianTokenizer

# Define translation functions
def load_model_and_tokenizer(model_path):
    """
    Load the MarianMT model and tokenizer from a local directory.
    """
    tokenizer = MarianTokenizer.from_pretrained(model_path)
    model = MarianMTModel.from_pretrained(model_path)
    return tokenizer, model

def translate_text(text, tokenizer, model):
    """
    Translate text using the specified MarianMT model and tokenizer.
    """
    inputs = tokenizer([text], return_tensors="pt", max_length=512, truncation=True)
    translated_tokens = model.generate(**inputs)
    return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

def back_translate(content, ml_en_path, en_ml_path):
    """
    Perform back-translation for Malayalam content.
    """
    try:
        # Load models and tokenizers
        ml_en_tokenizer, ml_en_model = load_model_and_tokenizer(ml_en_path)
        en_ml_tokenizer, en_ml_model = load_model_and_tokenizer(en_ml_path)

        # Step 1: Translate Malayalam to English
        intermediate = translate_text(content, ml_en_tokenizer, ml_en_model)
        print("Intermediate (English):", intermediate)

        # Step 2: Translate English back to Malayalam
        back_translated = translate_text(intermediate, en_ml_tokenizer, en_ml_model)
        print("Back-translated content (Malayalam):", back_translated)

        return back_translated
    except Exception as e:
        print("Back-translation error:", e)
        return content  # Fallback to original content

# Preprocessing functions
def preprocess_content(content):
    """
    Preprocess content to clean and remove garbled or repetitive text.
    """
    # Remove non-alphabetic characters
    content = re.sub(r"[^a-zA-Z\u0D00-\u0D7F\s]", "", content)  # Malayalam range
    # Replace multiple spaces with a single space
    content = re.sub(r"\s+", " ", content)
    return content.strip()

# Augmentation pipeline
def augment_text(content, ml_en_path, en_ml_path):
    """
    Apply preprocessing and back-translation to augment the content.
    """
    preprocessed = preprocess_content(content)
    if not preprocessed:
        return content  # Skip if content is non-informative
    return back_translate(preprocessed, ml_en_path, en_ml_path)

# File paths
input_file = r"C:\Users\Administrator\Documents\GitHub\Text_cleaning\data\output_data\root1\http___www.puzha.com_cartoon__cleaned.json"
output_file = r"C:\Users\Administrator\Documents\GitHub\Text_cleaning\data\output_data\root2\augmented_malayalam_data.json"

# Local model paths (replace with actual paths)
ml_en_path = r"C:\Users\Administrator\Documents\GitHub\ml-models\malayalam_back-translation\ml-en"
en_ml_path = r"C:\Users\Administrator\Documents\GitHub\ml-models\malayalam_back-translation\en-ml"

# Read input JSON file
with open(input_file, "r", encoding="utf-8") as infile:
    data = json.load(infile)

# Perform augmentation
original_content = data["content"]
data["content"] = preprocess_content(original_content)  # Clean original content
if data["content"]:
    data["augmented_content"] = augment_text(data["content"], ml_en_path, en_ml_path)
else:
    data["augmented_content"] = original_content  # Fallback to original

# Save augmented data to output JSON file
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=4)

print("Data augmentation complete. Augmented file saved to:", output_file)
