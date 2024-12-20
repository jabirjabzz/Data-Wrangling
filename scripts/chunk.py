import json
import re
import os
from typing import List, Dict, Any

def is_malayalam_word(word: str) -> bool:
    """
    Check if a word contains Malayalam characters.
    """
    return bool(re.search(r'[\u0D00-\u0D7F]', word))

def malayalam_word_tokenizer(text: str) -> List[str]:
    """
    Tokenize text preserving Malayalam and English words.
    """
    text = re.sub(r'\s+', ' ', text).strip()
    return text.split()

def malayalam_chunk_text(
    text: str,
    url: str,
    timestamp: str,
    max_words: int = 512,
    overlap_words: int = 50,
    min_chunk_words: int = 100
) -> List[Dict[str, Any]]:
    """
    Chunk text with linguistically aware method while preserving metadata.
    
    Args:
        text (str): Input text
        url (str): Source URL
        timestamp (str): Document timestamp
        max_words (int): Maximum words per chunk
        overlap_words (int): Number of words to overlap
        min_chunk_words (int): Minimum words to form a chunk
    
    Returns:
        List[Dict]: Chunks of text with metadata
    """
    words = malayalam_word_tokenizer(text)
    
    if len(words) <= max_words:
        return [{
            "text": text,
            "metadata": {
                "url": url,
                "timestamp": timestamp,
                "chunk_index": 0,
                "total_chunks": 1
            }
        }]
    
    chunks = []
    start = 0
    chunk_index = 0
    
    while start < len(words):
        end = min(start + max_words, len(words))
        chunk_words = words[start:end]
        chunk_text = ' '.join(chunk_words)
        
        if len(chunk_words) >= min_chunk_words:
            chunks.append({
                "text": chunk_text,
                "metadata": {
                    "url": url,
                    "timestamp": timestamp,
                    "chunk_index": chunk_index,
                    "start_idx": start,
                    "end_idx": end
                }
            })
            chunk_index += 1
        
        start += (max_words - overlap_words)
    
    # Add total_chunks to metadata
    for chunk in chunks:
        chunk["metadata"]["total_chunks"] = len(chunks)
    
    return chunks

def process_json_files(input_directory: str, output_directory: str, max_words: int = 512, overlap_words: int = 50) -> None:
    """
    Process all JSON files in a directory with chunking.
    
    Args:
        input_directory (str): Path to input JSON files
        output_directory (str): Path to save chunked JSON files
        max_words (int): Maximum words per chunk
        overlap_words (int): Number of words to overlap
    """
    os.makedirs(output_directory, exist_ok=True)
    
    for filename in os.listdir(input_directory):
        if filename.endswith('.json'):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, f'chunked_{filename}')
            
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract all required fields
            content = data.get('content', '')
            url = data.get('url', '')
            timestamp = data.get('timestamp', '')
            
            # Chunk the text with metadata
            chunks = malayalam_chunk_text(
                text=content,
                url=url,
                timestamp=timestamp,
                max_words=max_words,
                overlap_words=overlap_words
            )
            
            # Create output structure
            output_data = {
                "original_url": url,
                "original_timestamp": timestamp,
                "chunks": chunks
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            print(f"Processed {filename}: {len(chunks)} chunks")

if __name__ == "__main__":
    input_dir = r"C:\Users\Administrator\Documents\GitHub\Text cleaning\data\output_data\root1"
    output_dir = r"C:\Users\Administrator\Documents\GitHub\Text cleaning\data\chunked sample"
    
    process_json_files(
        input_directory=input_dir,
        output_directory=output_dir,
        max_words=512,
        overlap_words=50
    )