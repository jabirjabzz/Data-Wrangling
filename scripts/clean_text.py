from scripts.utils import (
    is_malayalam,
    clean_text,
    remove_stopwords,
)
import json
import os

def clean_text_file(input_dir, output_file):
    """
    Process and clean Malayalam text data from JSON files.
    
    Args:
        input_dir (str): Directory containing input JSON files
        output_file (str): Path to save processed JSONL file
    """
    processed_data = []
    
    # Walk through input directory
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".json"):
                try:
                    # Read JSON file
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        content = data.get("content", "")
                        
                        # Check if content is in Malayalam
                        if is_malayalam(content):
                            # Clean text
                            cleaned_content = clean_text(content)
                            
                            # Remove stopwords
                            cleaned_content = remove_stopwords(cleaned_content)
                            
                            # Add non-empty cleaned content
                            if cleaned_content:
                                processed_data.append(cleaned_content)
                
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    print(f"Error processing {file}: {e}")
    
    # Remove duplicates
    processed_data = list(set(processed_data))
    
    # Save processed data to JSONL file
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for entry in processed_data:
            out_f.write(json.dumps({"text": entry}, ensure_ascii=False) + '\n')
    
    print(f"Processed {len(processed_data)} Malayalam texts")