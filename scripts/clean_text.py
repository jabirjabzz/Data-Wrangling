from scripts.utils import (
    is_malayalam,
    clean_text,
    remove_stopwords,
    chunk_text,
)
import json
import os

def clean_text_file(input_dir, output_file, max_chunk_length=512, chunk_overlap=50):
    """
    Process and clean Malayalam text data from JSON files while preserving original structure.
    
    Args:
        input_dir (str): Directory containing input JSON files
        output_file (str): Path to save processed JSON file
        max_chunk_length (int): Maximum number of words per chunk
        chunk_overlap (int): Number of words to overlap between chunks
    """
    processed_data = []
    processed_files = 0
    skipped_files = 0
    
    # Walk through input directory
    print(f"Scanning directory: {input_dir}")
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                try:
                    # Read JSON file
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        # Handle different possible JSON structures
                        content = ""
                        if isinstance(data, dict):
                            content = data.get("content", "")
                        elif isinstance(data, list):
                            # If it's a list, try to get content from the first item
                            if data and isinstance(data[0], dict):
                                content = data[0].get("content", "")
                        
                        # Debug print
                        print(f"Processing file: {file}")
                        print(f"Content type: {type(content)}")
                        print(f"Content sample: {str(content)[:100]}...")
                        
                        # Check if content is in Malayalam
                        if is_malayalam(content):
                            # Clean text
                            cleaned_content = clean_text(content)
                            
                            # Remove stopwords
                            cleaned_content = remove_stopwords(cleaned_content)
                            
                            # Chunk the text if it's too long
                            if len(cleaned_content.split()) > max_chunk_length:
                                content_chunks = chunk_text(
                                    cleaned_content, 
                                    max_length=max_chunk_length, 
                                    overlap=chunk_overlap
                                )
                                
                                # Create multiple entries for each chunk
                                for chunk in content_chunks:
                                    if chunk.strip():
                                        # Create a new dictionary with cleaned chunk
                                        chunk_data = data.copy() if isinstance(data, dict) else data[0].copy()
                                        chunk_data['content'] = chunk
                                        processed_data.append(chunk_data)
                            else:
                                # If text is short, process as before
                                if cleaned_content:
                                    # Create a new dictionary with cleaned content
                                    cleaned_data = data.copy() if isinstance(data, dict) else data[0].copy()
                                    cleaned_data['content'] = cleaned_content
                                    processed_data.append(cleaned_data)
                            
                            processed_files += 1
                        else:
                            skipped_files += 1
                
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    print(f"Error processing {file}: {e}")
                    skipped_files += 1
    
    # Remove duplicates based on the entire dictionary
    processed_data = list({json.dumps(d, sort_keys=True) for d in processed_data})
    processed_data = [json.loads(d) for d in processed_data]
    
    # Save processed data to JSON file
    with open(output_file, 'w', encoding='utf-8') as out_f:
        json.dump(processed_data, out_f, ensure_ascii=False, indent=2)
    
    print(f"Processed files: {processed_files}")
    print(f"Skipped files: {skipped_files}")
    print(f"Total processed text chunks: {len(processed_data)}")