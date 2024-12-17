import json
import re
from collections import Counter
import difflib
import os

def safe_json_load(file_path):
    """
    Safely load JSON file, handling different formats.
    
    Args:
        file_path (str): Path to the JSON file
    
    Returns:
        dict: Parsed JSON data
    """
    try:
        # Try standard JSON loading
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If standard loading fails, try reading lines
        with open(file_path, 'r', encoding='utf-8') as f:
            # Read all lines and try parsing each
            lines = f.readlines()
            for line in lines:
                try:
                    return json.loads(line.strip())
                except json.JSONDecodeError:
                    continue
        
        # If no valid JSON found
        raise ValueError(f"No valid JSON found in {file_path}")

def preprocess_text(text):
    """
    Preprocess text for repetition detection.
    
    Args:
        text (str): Input text
    
    Returns:
        str: Preprocessed text
    """
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove punctuation except Malayalam-specific punctuations
    text = re.sub(r'[^\u0D00-\u0D7F\s.,!?]', '', text)
    return text

def extract_sentences(text):
    """
    Extract sentences from Malayalam text.
    
    Args:
        text (str): Input text
    
    Returns:
        List[str]: List of sentences
    """
    # Split sentences preserving Malayalam-specific punctuations
    sentences = re.split(r'[.\n!?]+', text)
    # Clean and filter out empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def detect_near_duplicates(sentences, similarity_threshold=0.8):
    """
    Detect near-duplicate sentences using difflib.
    
    Args:
        sentences (List[str]): List of sentences
        similarity_threshold (float): Similarity threshold for duplicates
    
    Returns:
        List[str]: Unique sentences
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
    
    Args:
        text (str): Input text
        min_phrase_length (int): Minimum words in a phrase to consider
        max_repetitions (int): Maximum allowed repetitions
    
    Returns:
        str: Text with repetitive phrases removed
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
    
    Args:
        input_path (str): Path to input JSON file
        output_path (str): Path to output JSON file
    """
    try:
        # Safely load JSON data
        data = safe_json_load(input_path)
        
        # Extract text (handle different possible JSON structures)
        text = data.get('text', '') if isinstance(data, dict) else str(data)
        
        # Remove repetitive content
        processed_text = remove_repetitive_phrases(text)
        
        # Extract unique sentences
        sentences = extract_sentences(processed_text)
        unique_sentences = detect_near_duplicates(sentences)
        
        # Reconstruct text
        final_text = ' '.join(unique_sentences)
        
        # Write processed text
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({"text": final_text}, f, ensure_ascii=False, indent=2)
        
        print(f"Processed {input_path}")
        print(f"Original text length: {len(text.split())}")
        print(f"Processed text length: {len(final_text.split())}")
    
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def batch_process_repetition(input_directory, output_directory):
    """
    Batch process all JSON files in a directory.
    
    Args:
        input_directory (str): Path to input JSON files
        output_directory (str): Path to output processed files
    """
    # Create output directory if not exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Process each JSON file
    for filename in os.listdir(input_directory):
        if filename.endswith('.json'):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, f'processed_{filename}')
            
            process_repetition_removal(input_path, output_path)

# Example usage
if __name__ == "__main__":
    # Example for single file processing
    # process_repetition_removal(
    #     'input.json', 
    #     'output.json'
    # )
    
    # Example for batch processing
    batch_process_repetition(
        input_directory= r'C:\Users\Administrator\Documents\GitHub\Text cleaning\data\output_data\root1',
        output_directory= r'C:\Users\Administrator\Documents\GitHub\Text cleaning\data\output_data\root2'
    )