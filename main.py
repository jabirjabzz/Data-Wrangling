import os
from scripts.clean_text import clean_text_file

def main():
    input_dir = r"C:\Users\Administrator\Documents\GitHub\Malayalam-Language-Scraping\output_Json"
    output_file = os.path.join("C:\\Users\\Administrator\\Documents\\GitHub\\Text cleaning\\data\\output", "cleaned_data.jsonl")
    
    print("Starting Malayalam text cleaning and chunking...")
    clean_text_file(
        input_dir, 
        output_file, 
        max_chunk_length=512,  # Adjust as needed
        chunk_overlap=50       # Adjust as needed
    )
    print(f"Text cleaning and chunking completed. Cleaned text saved to {output_file}")

if __name__ == "__main__":
    main()