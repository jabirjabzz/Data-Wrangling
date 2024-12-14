from scripts.utils import (
    remove_html_tags,
    remove_special_characters,
    normalize_text,
    remove_duplicates,
    remove_stopwords,
)

def clean_text(raw_text):
    """Pipeline for cleaning text."""
    # Step 1: Remove HTML tags
    text = remove_html_tags(raw_text)
    
    # Step 2: Remove special characters and numbers
    text = remove_special_characters(text)
    
    # Step 3: Normalize text (lowercase, strip)
    text = normalize_text(text)
    
    # Step 4: Remove stopwords
    text = remove_stopwords(text)
    
    return text

def clean_text_file(input_path, output_path):
    """Clean a file and save the output."""
    with open(input_path, "r", encoding="utf-8") as infile:
        lines = infile.readlines()
    
    # Remove duplicates
    lines = remove_duplicates(lines)
    
    # Clean each line
    cleaned_lines = [clean_text(line) for line in lines]
    
    # Save cleaned text
    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(cleaned_lines))
