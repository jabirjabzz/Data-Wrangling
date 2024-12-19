import json
import re
import os

def is_malayalam_word(word):
    """
    Check if a word contains Malayalam characters.
    """
    return bool(re.search(r'[\u0D00-\u0D7F]', word))

def malayalam_word_tokenizer(text):
    """
    Tokenize text preserving Malayalam and English words.
    """
    # Remove extra whitespaces and split
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Split on spaces, preserving both Malayalam and English words
    words = text.split()
    
    return words

def malayalam_chunk_text(
    text, 
    max_words=512, 
    overlap_words=50, 
    min_chunk_words=100
):
    """
    Chunk text with linguistically aware method.
    
    Args:
        text (str): Input text
        max_words (int): Maximum words per chunk
        overlap_words (int): Number of words to overlap
        min_chunk_words (int): Minimum words to form a chunk
    
    Returns:
        List[dict]: Chunks of text
    """
    words = malayalam_word_tokenizer(text)
    
    if len(words) <= max_words:
        return [{"text": text}]
    
    chunks = []
    start = 0
    
    while start < len(words):
        # Calculate end of current chunk
        end = min(start + max_words, len(words))
        
        # Extract chunk
        chunk_words = words[start:end]
        chunk_text = ' '.join(chunk_words)
        
        # Only add if chunk meets minimum word requirement
        if len(chunk_words) >= min_chunk_words:
            chunks.append({"text": chunk_text})
        
        # Move start point with overlap
        start += (max_words - overlap_words)
    
    return chunks

def process_json_files(input_directory, output_directory, max_words=512, overlap_words=50):
    """
    Process all JSON files in a directory with chunking.
    
    Args:
        input_directory (str): Path to input JSON files
        output_directory (str): Path to save chunked JSON files
        max_words (int): Maximum words per chunk
        overlap_words (int): Number of words to overlap
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    # Process each JSON file in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.json'):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, f'chunked_{filename}')
            
            # Read input JSON file
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract text
            text = data.get('text', '')
            
            # Chunk the text
            chunks = malayalam_chunk_text(
                text, 
                max_words=max_words, 
                overlap_words=overlap_words
            )
            
            # Write chunked data to output file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(chunks, f, ensure_ascii=False, indent=2)
            
            print(f"Processed {filename}: {len(chunks)} chunks")

# Example usage
if __name__ == "__main__":
    input_dir = "path/to/input/json/files"
    output_dir = "path/to/output/chunked/files"
    
    process_json_files(
        input_directory=input_dir, 
        output_directory=output_dir,
        max_words=512,  # Configurable chunk size
        overlap_words=50  # Configurable overlap
    )