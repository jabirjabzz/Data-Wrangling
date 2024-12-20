from transformers import pipeline
import pandas as pd
import re
from indicnlp.tokenize import indic_tokenize
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        logging.error(f"Error during mask filling: {e}")
        raise RuntimeError("Error during mask filling.") from e

def add_missing_full_stop(text):
    """Adds a full stop at the end if missing."""
    if not re.search(r'[.!?]$', text.strip()):
        return text.strip() + "."
    return text.strip()

def segment_words(text, language='ml'):
    """Segments words where spaces are missing."""
    try:
        # Use Indic NLP tokenizer for Malayalam
        tokens = indic_tokenize.trivial_tokenize(text, lang=language)
        return ' '.join(tokens)
    except Exception as e:
        logging.error(f"Error during word segmentation: {e}")
        raise RuntimeError("Error during word segmentation.") from e

def insert_mask(text):
    """Insert <mask> intelligently into the text."""
    words = text.split()
    if len(words) > 1:
        longest_word_index = max(range(len(words)), key=lambda i: len(words[i]))
        words.insert(longest_word_index + 1, "<mask>")
        return ' '.join(words)
    else:
        return f"<mask> {text}"

def clean_and_correct_text(text, language='ml'):
    """
    Combines all preprocessing steps: 
    1. Segmentation,
    2. Inserting <mask>,
    3. Filling missing words,
    4. Adding punctuation.
    """
    try:
        logging.info(f"Original Text: {text}")
        
        # Step 1: Segment words
        text = segment_words(text, language=language)
        logging.info(f"After Segmentation: {text}")
        
        # Step 2: Insert <mask> (if missing)
        if "<mask>" not in text:
            text = insert_mask(text)
            logging.info(f"After Inserting Mask: {text}")
        
        # Step 3: Fill missing words
        text = fill_missing_word(text)
        logging.info(f"After Filling Missing Words: {text}")
        
        # Step 4: Add missing punctuation
        text = add_missing_full_stop(text)
        logging.info(f"After Adding Missing Punctuation: {text}")
        
        return text
    except Exception as e:
        logging.error(f"Error in text cleaning and correction: {e}")
        raise

def save_to_csv(text, filename='corrected_text.csv'):
    """Save the corrected text to a CSV file."""
    try:
        df = pd.DataFrame({"Corrected Text": [text]})
        df.to_csv(filename, index=False)
        logging.info(f"Corrected text saved to {filename}.")
    except Exception as e:
        logging.error(f"Error writing to CSV: {e}")
        raise

# Example usage
text = "കേരളംഒരു മനോഹരമായസ്ഥലമാ."
try:
    corrected_text = clean_and_correct_text(text, language='ml')
    logging.info(f"Corrected Text: {corrected_text}")
    
    # Save to CSV
    save_to_csv(corrected_text)
except Exception as e:
    logging.error(f"An error occurred: {e}")
