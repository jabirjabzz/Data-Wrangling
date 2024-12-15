import os
from scripts.clean_text import clean_text_file

def main():
    input_dir = r"C:\Users\Administrator\Documents\GitHub\Malayalam-Language-Scraping\output_Json"
    output_file = os.path.join("C:\\Users\\Administrator\\Documents\\GitHub\\Text cleaning\\data\\output", "cleaned_data.jsonl")
    
    print("Starting Malayalam text cleaning...")
    clean_text_file(input_dir, output_file)
    print(f"Text cleaning completed. Cleaned text saved to {output_file}")

if __name__ == "__main__":
    main()