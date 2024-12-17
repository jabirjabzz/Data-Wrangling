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

        if file_path.lower().endswith('.jsonl'):  # Case-insensitive check
            parsed_objects = []
            for line in content.splitlines():
                line = line.strip()
                if line:  # Skip empty lines
                    try:
                        parsed_objects.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON in line: {line}. Error: {e}") #Print the error to debug
                        continue
            if not parsed_objects:
                raise ValueError(f"No valid JSON found in {file_path}")
            return parsed_objects

        elif file_path.lower().endswith('.json'): # Check for standard JSON
            try:
                return json.loads(content) # Directly parse the content
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON format in {file_path}")
        else:
            raise ValueError(f"File format not supported. Use .json or .jsonl")

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

def preprocess_text(text):
    """
    Preprocess text for repetition detection.
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove punctuation except Malayalam-specific punctuations
    text = re.sub(r'[^\u0D00-\u0D7F\s.,!?]', '', text)
    return text

def extract_sentences(text):
    """
    Extract sentences from Malayalam text.
    """
    # Split sentences preserving Malayalam-specific punctuations
    sentences = re.split(r'[.\n!?]+', text)
    # Clean and filter out empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def detect_near_duplicates(sentences, similarity_threshold=0.8):
    """
    Detect near-duplicate sentences using difflib.
    """
    unique_sentences = []
    for i, sentence in enumerate(sentences):
        is_duplicate = False
        for existing in unique_sentences:
            # Calculate similarity ratio
            similarity = difflib.SequenceMatcher(None, sentence, existing).ratio()
            if similarity >= similarity_threshold:
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique_sentences.append(sentence)
    
    return unique_sentences

def remove_repetitive_phrases(text, min_phrase_length=5, max_repetitions=3):
    """
    Remove repetitive phrases from text.
    """
    # Preprocess text
    preprocessed_text = preprocess_text(text)
    
    # Extract words
    words = preprocessed_text.split()
    
    # Find repetitive phrases
    phrases = []
    for i in range(len(words) - min_phrase_length + 1):
        for length in range(min_phrase_length, min(min_phrase_length + 5, len(words) - i + 1)):
            phrase = ' '.join(words[i:i+length])
            phrases.append(phrase)
    
    # Count phrase repetitions
    phrase_counts = Counter(phrases)
    
    # Remove overly repetitive phrases
    filtered_words = []
    i = 0
    while i < len(words):
        current_phrase = ' '.join(words[i:i+min_phrase_length])
        if phrase_counts[current_phrase] <= max_repetitions:
            filtered_words.append(words[i])
            i += 1
        else:
            # Skip repetitive phrase
            i += min_phrase_length
    
    return ' '.join(filtered_words)

def process_repetition_removal(input_path, output_path):
    """
    Process JSON file to remove repetitions.
    """
    try:
        logger.info(f"Starting to process {input_path}")
        
        # Safely load JSON data
        data = safe_json_load(input_path)
        
        # Extract text (handle different possible JSON structures)
        text = data.get('text', '') if isinstance(data, dict) else str(data)
        
        logger.info(f"Original text length: {len(text)}")
        
        # Remove repetitive content
        processed_text = remove_repetitive_phrases(text)
        
        # Extract unique sentences
        sentences = extract_sentences(processed_text)
        unique_sentences = detect_near_duplicates(sentences)
        
        # Reconstruct text
        final_text = ' '.join(unique_sentences)
        
        logger.info(f"Processed text length: {len(final_text)}")
        
        # Write processed text
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({"text": final_text}, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Successfully processed {input_path}")
        
    except Exception as e:
        logger.error(f"Error processing {input_path}: {e}")
        logger.error(traceback.format_exc())

def batch_process_repetition(input_directory, output_directory):
    """
    Batch process all JSON files in a directory.
    """
    # Create output directory if not exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Get list of JSON files
    json_files = [f for f in os.listdir(input_directory) if f.endswith('.json')]
    
    logger.info(f"Total JSON files found: {len(json_files)}")
    
    # Process each JSON file
    for filename in json_files:
        input_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, f'processed_{filename}')
        
        try:
            process_repetition_removal(input_path, output_path)
        except Exception as e:
            logger.error(f"Failed to process {filename}: {e}")
    
    logger.info("Batch processing complete")
# Example usage
if __name__ == "__main__":
    # Example for single file processing
    # process_repetition_removal(
    #     'input.json', 
    #     'output.json'
    # )
    input_dir= (r'C:\Users\Administrator\Documents\GitHub\Text cleaning\data\output_data\root1')
    output_dir= (r'C:\Users\Administrator\Documents\GitHub\Text cleaning\data\output_data\root2')
    batch_process_repetition(input_dir, output_dir) 
    # Example for batch processing
