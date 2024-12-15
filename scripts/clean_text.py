import os
import json
import logging
from typing import List, Dict, Any

from .utils import (
    is_malayalam, 
    clean_text, 
    chunk_text, 
    remove_stopwords, 
    setup_logging
)

def process_json_file(
    file_path: str, 
    max_chunk_length: int = 512, 
    chunk_overlap: int = 50
) -> List[Dict[str, Any]]:
    """
    Process a single JSON file for Malayalam text.
    
    Args:
        file_path (str): Path to the JSON file
        max_chunk_length (int): Maximum words per chunk
        chunk_overlap (int): Words to overlap between chunks
    
    Returns:
        List[Dict[str, Any]]: Processed file contents
    """
    logger = logging.getLogger(__name__)
    processed_entries = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            data = json.load(f)
        
        # Handle different JSON structures
        contents = []
        if isinstance(data, dict):
            contents = [data.get("content", "")]
        elif isinstance(data, list):
            contents = [item.get("content", "") for item in data if isinstance(item, dict)]
        
        for content in contents:
            if not content:
                continue
            
            # Malayalam content processing
            if is_malayalam(content):
                cleaned_content = clean_text(content)
                cleaned_content = remove_stopwords(cleaned_content)
                
                # Chunk long texts
                if len(cleaned_content.split()) > max_chunk_length:
                    content_chunks = chunk_text(
                        cleaned_content, 
                        max_length=max_chunk_length, 
                        overlap=chunk_overlap
                    )
                    
                    for chunk in content_chunks:
                        if chunk.strip():
                            chunk_entry = data.copy() if isinstance(data, dict) else data[0].copy()
                            chunk_entry['content'] = chunk
                            processed_entries.append(chunk_entry)
                else:
                    # Short content processing
                    if cleaned_content:
                        processed_entry = data.copy() if isinstance(data, dict) else data[0].copy()
                        processed_entry['content'] = cleaned_content
                        processed_entries.append(processed_entry)
        
        logger.info(f"Processed file: {file_path}")
    
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
    
    return processed_entries

def process_directory(
    input_dir: str, 
    output_file: str, 
    max_chunk_length: int = 512, 
    chunk_overlap: int = 50
) -> None:
    """
    Process all JSON files in a directory.
    
    Args:
        input_dir (str): Input directory containing JSON files
        output_file (str): Output file path for processed data
        max_chunk_length (int): Maximum words per chunk
        chunk_overlap (int): Words to overlap between chunks
    """
    logger = setup_logging()
    processed_data = []
    total_files = 0
    
    # Validate input directory
    if not os.path.exists(input_dir):
        logger.error(f"Input directory not found: {input_dir}")
        return
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Process files
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                file_entries = process_json_file(
                    file_path, 
                    max_chunk_length, 
                    chunk_overlap
                )
                processed_data.extend(file_entries)
                total_files += 1
    
    # Remove duplicates
    processed_data = list({json.dumps(entry, sort_keys=True) for entry in processed_data})
    processed_data = [json.loads(entry) for entry in processed_data]
    
    # Save processed data
    try:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            json.dump(processed_data, out_f, ensure_ascii=False, indent=2)
        
        logger.info(f"Processing Complete:")
        logger.info(f"Total Files Processed: {total_files}")
        logger.info(f"Total Entries Processed: {len(processed_data)}")
        logger.info(f"Output File: {output_file}")
    
    except Exception as e:
        logger.error(f"Error saving processed data: {e}")