import json
import re
from collections import Counter
import difflib
import os
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('json_processing.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def safe_json_load(file_path):
    """Safely load JSON or JSONL file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if file_path.lower().endswith('.jsonl'):  # For JSONL (one object per line)
            parsed_objects = []
            for line in content.splitlines():
                line = line.strip()
                if line:  # Skip empty lines
                    try:
                        parsed_objects.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        logger.error(f"Error decoding JSON in line: {line}. Error: {e}")
            if not parsed_objects:
                raise ValueError(f"No valid JSON found in {file_path}")
            return parsed_objects

        elif file_path.lower().endswith('.json'):  # For standard JSON
            return json.loads(content)
        else:
            raise ValueError(f"File format not supported. Use .json or .jsonl")

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

def preprocess_text(text):
    """Preprocess text for repetition detection."""
    if not isinstance(text, str):
        text = str(text)
    
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove unwanted characters except Malayalam-specific punctuations
    text = re.sub(r'[^\u0D00-\u0D7F\s.,!?]', '', text)
    return text

def extract_sentences(text):
    """Extract sentences from Malayalam text."""
    sentences = re.split(r'[.\n!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def detect_near_duplicates(sentences, similarity_threshold=0.8):
    """Detect near-duplicate sentences using difflib."""
    unique_sentences = []
    for i, sentence in enumerate(sentences):
        is_duplicate = False
        for existing in unique_sentences:
            similarity = difflib.SequenceMatcher(None, sentence, existing).ratio()
            if similarity >= similarity_threshold:
                is_duplicate = True
                break
        if not is_duplicate:
            unique_sentences.append(sentence)
    return unique_sentences

def remove_repetitive_phrases(text, min_phrase_length=5, max_repetitions=3):
    """Remove repetitive phrases from text."""
    preprocessed_text = preprocess_text(text)
    words = preprocessed_text.split()
    phrases = []
    for i in range(len(words) - min_phrase_length + 1):
        for length in range(min_phrase_length, min(min_phrase_length + 5, len(words) - i + 1)):
            phrase = ' '.join(words[i:i+length])
            phrases.append(phrase)
    phrase_counts = Counter(phrases)
    filtered_words = []
    i = 0
    while i < len(words):
        current_phrase = ' '.join(words[i:i+min_phrase_length])
        if phrase_counts[current_phrase] <= max_repetitions:
            filtered_words.append(words[i])
            i += 1
        else:
            i += min_phrase_length
    return ' '.join(filtered_words)

def process_single_jsonl_file(input_path, output_path):
    """Process a single JSONL file for repetition removal."""
    try:
        logger.info(f"Processing file: {input_path}")
        
        # Load JSONL file
        data = safe_json_load(input_path)
        
        # Process each JSON object
        processed_data = []
        for idx, entry in enumerate(data):
            text = entry.get('text', '')
            if not text:
                logger.warning(f"No 'text' key found in entry {idx}")
                continue
            
            logger.info(f"Original text length (entry {idx}): {len(text)}")
            
            # Remove repetitive content and near-duplicates
            processed_text = remove_repetitive_phrases(text)
            sentences = extract_sentences(processed_text)
            unique_sentences = detect_near_duplicates(sentences)
            final_text = ' '.join(unique_sentences)
            
            # Store processed entry
            processed_data.append({"text": final_text})
        
        # Save processed data to a new file
        with open(output_path, 'w', encoding='utf-8') as f:
            for entry in processed_data:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        logger.info(f"File successfully processed and saved to {output_path}")
    
    except Exception as e:
        logger.error(f"Failed to process {input_path}: {e}")
        logger.error(traceback.format_exc())

# Example for processing a single file
if __name__ == "__main__":
    input_file = r'C:\Users\Administrator\Documents\GitHub\Text cleaning\data\output_data\root1\cleaned_data.jsonl'
    output_file = r'C:\Users\Administrator\Documents\GitHub\Text cleaning\data\output_data\root2\processed_output.jsonl'
    
    process_single_jsonl_file(input_file, output_file)
