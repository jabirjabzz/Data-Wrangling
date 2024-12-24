# import json
# import re
# from transformers import MarianMTModel, MarianTokenizer
# import os

# # Define translation functions
# def load_model_and_tokenizer(model_path):
#     """Load the MarianMT model and tokenizer."""
#     try:
#         tokenizer = MarianTokenizer.from_pretrained(model_path)
#         model = MarianMTModel.from_pretrained(model_path)
#         return tokenizer, model
#     except Exception as e:
#         print(f"Error loading model/tokenizer from {model_path}: {e}")
#         return None, None

# def translate_text(text, tokenizer, model):
#     """Translate text."""
#     try:
#         inputs = tokenizer([text], return_tensors="pt", max_length=512, truncation=True)
#         translated_tokens = model.generate(**inputs)
#         return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
#     except Exception as e:
#         print(f"Translation error: {e}")
#         return None

# def back_translate(content, ml_en_path, en_ml_path):
#     """Perform back-translation."""
#     try:
#         ml_en_tokenizer, ml_en_model = load_model_and_tokenizer(ml_en_path)
#         en_ml_tokenizer, en_ml_model = load_model_and_tokenizer(en_ml_path)

#         if ml_en_tokenizer is None or ml_en_model is None or en_ml_tokenizer is None or en_ml_model is None:
#             return None

#         intermediate = translate_text(content, ml_en_tokenizer, ml_en_model)
#         if intermediate is None:
#             return None
#         print("Intermediate (English):", intermediate)

#         back_translated = translate_text(intermediate, en_ml_tokenizer, en_ml_model)
#         if back_translated is None:
#             return None
#         print("Back-translated content (Malayalam):", back_translated)

#         return back_translated
#     except Exception as e:
#         print("Back-translation error:", e)
#         return None

# # Preprocessing functions
# def preprocess_content(content):
#     """Preprocess content."""
#     if content is None:  # Handle None input
#         return ""
#     content = re.sub(r"[^a-zA-Z\u0D00-\u0D7F\s]", "", content)  # Malayalam range
#     content = re.sub(r"\s+", " ", content).strip()
#     return content

# # Augmentation pipeline
# def augment_text(content, ml_en_path, en_ml_path):
#     """Apply preprocessing and back-translation."""
#     preprocessed = preprocess_content(content)
#     if not preprocessed:
#         return ""  # Return empty string if preprocessed content is empty
#     return back_translate(preprocessed, ml_en_path, en_ml_path)

# # File paths (MAKE SURE THESE ARE CORRECT)
# input_file = r"C:\Users\Administrator\Documents\GitHub\Text_cleaning\data\output_data\root1\http___www.puzha.com_cartoon__cleaned.json"
# output_file = r"C:\Users\Administrator\Documents\GitHub\Text_cleaning\data\output_data\root2\augmented_malayalam_data.json"

# ml_en_path = r"C:\Users\Administrator\Documents\GitHub\ml-models\malayalam_back-translation\ml-en"
# en_ml_path = r"C:\Users\Administrator\Documents\GitHub\ml-models\malayalam_back-translation\en-ml"

# # Create output directory if it doesn't exist
# os.makedirs(os.path.dirname(output_file), exist_ok=True)

# try:
#     # Read input JSON file
#     with open(input_file, "r", encoding="utf-8") as infile:
#         data = json.load(infile)

#     # Perform augmentation (handling cases where data["content"] might be a list)
#     if isinstance(data["content"], list):
#         augmented_contents = []
#         for content_item in data["content"]:
#             preprocessed_item = preprocess_content(content_item)
#             if preprocessed_item:
#                 augmented_item = augment_text(preprocessed_item, ml_en_path, en_ml_path)
#                 augmented_contents.append(augmented_item if augmented_item else content_item) #if aug failed use original
#             else:
#                 augmented_contents.append(content_item)
#         data["augmented_content"] = augmented_contents
#     else:
#         original_content = data.get("content", "")  # Use .get to handle missing keys
#         data["content"] = preprocess_content(original_content)
#         if data["content"]:
#             data["augmented_content"] = augment_text(data["content"], ml_en_path, en_ml_path)
#             if data["augmented_content"] is None:
#                 data["augmented_content"] = original_content
#         else:
#             data["augmented_content"] = original_content

#     # Save augmented data to output JSON file
#     with open(output_file, "w", encoding="utf-8") as outfile:
#         json.dump(data, outfile, ensure_ascii=False, indent=4)

#     print("Data augmentation complete. Augmented file saved to:", output_file)

# except FileNotFoundError:
#     print(f"Error: Input file not found: {input_file}")
# except json.JSONDecodeError:
#     print(f"Error: Invalid JSON format in input file: {input_file}")
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")


from transformers import MarianMTModel, MarianTokenizer

ml_en_path = r"C:\Users\Administrator\Documents\GitHub\ml-models\malayalam_back-translation\ml-en"
en_ml_path = r"C:\Users\Administrator\Documents\GitHub\ml-models\malayalam_back-translation\en-ml"

try:
    tokenizer_ml_en = MarianTokenizer.from_pretrained(ml_en_path)
    model_ml_en = MarianMTModel.from_pretrained(ml_en_path)
    print("ml-en model loaded successfully!")

    tokenizer_en_ml = MarianTokenizer.from_pretrained(en_ml_path)
    model_en_ml = MarianMTModel.from_pretrained(en_ml_path)
    print("en-ml model loaded successfully!")

except Exception as e:
    print(f"Error loading model: {e}")