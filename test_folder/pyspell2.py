import json
import random
import re
from transformers import MarianMTModel, MarianTokenizer, pipeline
import nltk
from nltk.corpus import wordnet

# Download WordNet for synonym replacement
nltk.download("wordnet")

# Define translation functions
def translate_text(text, model_name):
    """
    Translate text using the specified MarianMT model.
    """
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    # Tokenize input text
    inputs = tokenizer([text], return_tensors="pt", max_length=512, truncation=True)
    # Generate translation
    translated_tokens = model.generate(**inputs)
    # Decode translation
    return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

def back_translate(content):
    """
    Perform back-translation for Malayalam content.
    """
    try:
        # Step 1: Translate Malayalam to English
        intermediate = translate_text(content, "Helsinki-NLP/opus-mt-ml-en")
        print("Intermediate (English):", intermediate)

        # Step 2: Translate English back to Malayalam
        back_translated = translate_text(intermediate, "Helsinki-NLP/opus-mt-en-ml")
        print("Back-translated content (Malayalam):", back_translated)
        
        return back_translated
    except Exception as e:
        print("Back-translation error:", e)
        return content  # Fallback to original content


# Preprocessing functions
def preprocess_content(content):
    """
    Preprocess content to clean and remove duplicates.
    """
    # Remove non-informative text (punctuation-only or whitespace)
    if not re.search(r'\w', content):
        print("Content is non-informative. Skipping.")
        return None

    # Split into words, remove duplicates, and rejoin
    words = content.split()
    unique_words = list(dict.fromkeys(words))
    return " ".join(unique_words)

def expand_keywords(content):
    """
    Expand keywords into sentences using templates or a language model.
    """
    # Use a pre-trained paraphrasing model or language model
    generator = pipeline("text2text-generation", model="t5-base", tokenizer="t5-base")
    phrases = content.split()[:20]  # Process the first 20 keywords (adjust as needed)
    expanded = []
    for phrase in phrases:
        try:
            result = generator(f"Explain: {phrase}", max_length=50, num_return_sequences=1)
            expanded.append(result[0]["generated_text"])
        except Exception as e:
            print(f"Error expanding keyword '{phrase}':", e)
            expanded.append(phrase)  # Fallback to original keyword
    return " ".join(expanded)

def synonym_replacement(content, n=3):
    """
    Replace random words in the content with their synonyms.
    """
    words = content.split()
    new_words = words.copy()
    random_indices = random.sample(range(len(words)), min(n, len(words)))
    for i in random_indices:
        synonyms = wordnet.synsets(words[i])
        if synonyms:
            synonym = synonyms[0].lemmas()[0].name()
            new_words[i] = synonym if synonym != words[i] else words[i]
    return " ".join(new_words)

# Augmentation pipeline
def augment_text(content):
    """
    Apply preprocessing and augmentation techniques to the content.
    """
    preprocessed = preprocess_content(content)
    if not preprocessed:
        return content  # Return original if preprocessing failed

    # Combine augmentation techniques
    augmentations = []
    augmentations.append(back_translate(preprocessed))
    augmentations.append(expand_keywords(preprocessed))
    augmentations.append(synonym_replacement(preprocessed))

    # Join all augmented content into a single output
    return " ".join(augmentations)

# File paths
input_file = r"C:\Users\Administrator\Documents\GitHub\Text_cleaning\data\input_data\https___archives.mathrubhumi.com_nri_pravasi-bharatham_chennai_chennai-news_19feb2022-1.6459726.json"
output_file = r"C:\Users\Administrator\Documents\GitHub\Text_cleaning\data\output_data\root2\augmented_malayalam_data2.json"

# Read input JSON file
with open(input_file, "r", encoding="utf-8") as infile:
    data = json.load(infile)

# Perform augmentation
original_content = data["content"]
data["content"] = preprocess_content(original_content)  # Clean original content
if data["content"]:
    data["augmented_content"] = augment_text(original_content)
else:
    data["augmented_content"] = original_content  # Fallback to original

# Save augmented data to output JSON file
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=4)

print("Data augmentation complete. Augmented file saved to:", output_file)
