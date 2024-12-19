import os
import json
import logging
from typing import List

from .utils import (
    # is_malayalam, 
    clean_text, 
    remove_stopwords, 
    setup_logging,
    remove_repetitive_text
)

def process_json_file(file_path: str, output_dir: str) -> None:
    """
    Process a single JSON file and save it with '_cleaned' suffix,
    maintaining exact input structure.
    """
    logger = logging.getLogger(__name__)

    try:
        # Read the input file exactly as it is
        with open(file_path, 'r', encoding='utf-8') as f:
            original_data = json.load(f)

        # Process based on original structure
        if isinstance(original_data, dict):
            # For single JSON object
            content = original_data.get("content", "")
            cleaned_content = clean_text(content)
            cleaned_content = remove_stopwords(cleaned_content)
            cleaned_content = remove_repetitive_text(cleaned_content)
            original_data["content"] = cleaned_content
            processed_data = original_data
            
        elif isinstance(original_data, list):
            # For list of JSON objects
            processed_data = []
            for item in original_data:
                if isinstance(item, dict):
                    content = item.get("content", "")
                    cleaned_content = clean_text(content)
                    cleaned_content = remove_stopwords(cleaned_content)
                    cleaned_content = remove_repetitive_text(cleaned_content)
                    item_copy = item.copy()
                    item_copy["content"] = cleaned_content
                    processed_data.append(item_copy)
                else:
                    processed_data.append(item)  # Maintain non-dict items as is

        # Create output filename with '_cleaned' suffix
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        output_filename = f"{name}_cleaned{ext}"
        output_path = os.path.join(output_dir, output_filename)

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Write processed data in exact same structure as input
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, ensure_ascii=False, indent=2)

        logger.info(f"Processed and saved: {output_path}")

    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")

def process_directory(input_dir: str, output_dir: str) -> None:
    """
    Process all JSON files in directory, maintaining individual files.
    """
    logger = setup_logging()
    total_files = 0

    if not os.path.exists(input_dir):
        logger.error(f"Input directory not found: {input_dir}")
        return

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".json"):
                # Create corresponding output directory structure
                rel_path = os.path.relpath(root, input_dir)
                output_subdir = os.path.join(output_dir, rel_path)
                
                file_path = os.path.join(root, file)
                process_json_file(file_path, output_subdir)
                total_files += 1

    logger.info(f"Total Files Processed: {total_files}")