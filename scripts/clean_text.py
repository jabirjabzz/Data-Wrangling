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

def process_json_file(file_path: str) -> List[dict]:
    """
    Process a single JSON file for Malayalam text.
    """
    logger = logging.getLogger(__name__)
    processed_entries = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        contents = []
        if isinstance(data, dict):
            contents = [data.get("content", "")]
        elif isinstance(data, list):
            contents = [item.get("content", "") for item in data if isinstance(item, dict)]

        for content in contents:
            # if not content or not is_malayalam(content):
            #     logger.info(f"Skipped non-Malayalam content: {content[:30]}...")
            #     continue

            cleaned_content = clean_text(content)
            logger.info(f"Cleaned content: {cleaned_content[:30]}...")
            cleaned_content = remove_stopwords(cleaned_content)
            cleaned_content = remove_repetitive_text(cleaned_content)
            processed_entries.append({"text": cleaned_content})

        logger.info(f"Processed file: {file_path}")

    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")

    return processed_entries


def process_directory(input_dir: str, output_file: str) -> None:
    """
    Process all JSON files in a directory.
    """
    logger = setup_logging()
    processed_data = []
    total_files = 0

    if not os.path.exists(input_dir):
        logger.error(f"Input directory not found: {input_dir}")
        return

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                processed_data.extend(process_json_file(file_path))
                total_files += 1

    try:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            for entry in processed_data:
                out_f.write(json.dumps(entry, ensure_ascii=False) + '\n')

        logger.info(f"Total Files Processed: {total_files}")
        logger.info(f"Output File: {output_file}")

    except Exception as e:
        logger.error(f"Error saving processed data: {e}")
