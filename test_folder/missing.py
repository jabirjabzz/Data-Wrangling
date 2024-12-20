from transformers import pipeline
import pandas as pd
import re
from indicnlp.tokenize import indic_tokenize

# Initialize the fill-mask pipeline
try:
    fill_mask = pipeline("fill-mask", model="xlm-roberta-base")
except Exception as e:
    raise RuntimeError(f"Failed to initialize fill-mask pipeline: {e}")

def fill_missing_word(text):
    """Fills the missing word indicated by the <mask> token in the text."""
    if "<mask>" not in text:
        raise ValueError("The input text must contain the <mask> token for the model to fill in.")
    try:
        predictions = fill_mask(text)
        return predictions[0]["sequence"]  # Return the top prediction
    except Exception as e:
        raise RuntimeError(f"Error during mask filling: {e}")

def add_missing_full_stop(text):
    """Adds a full stop at the end if missing."""
    if not re.search(r'[.!?]$', text.strip()):
        return text.strip() + "."
    return text.strip()

def segment_words(text, language='ml'):
    """Segments words where spaces are missing."""
    try:
        tokens = indic_tokenize.trivial_tokenize(text, lang=language)
        return ' '.join(tokens)
    except Exception as e:
        raise RuntimeError(f"Error during word segmentation: {e}")

def clean_and_correct_text(text, language='ml'):
    """
    Combines all preprocessing steps: 
    1. Segmentation,
    2. Filling missing words using <mask>,
    3. Adding punctuation.
    """
    try:
        text = segment_words(text, language=language)
        if "<mask>" in text:  # Only apply fill_mask if <mask> exists
            text = fill_missing_word(text)
        text = add_missing_full_stop(text)
        return text
    except Exception as e:
        raise RuntimeError(f"Error in text cleaning and correction: {e}")

# Example usage
text = "കേരളംഒരു മനോഹരമായസ്ഥലമാ."
try:
    corrected_text = clean_and_correct_text(text, language='ml')
    print(f"Corrected Text: {corrected_text}")
    
    # Save to CSV
    pd.DataFrame({"Corrected Text": [corrected_text]}).to_csv('corrected_text.csv', index=False)
    print("Corrected text saved to corrected_text.csv.")
except Exception as e:
    print(f"An error occurred: {e}")
