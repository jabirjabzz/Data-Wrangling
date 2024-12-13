from scripts.clean_text import clean_text_file

def main():
    input_file = "data/raw_text.txt"
    output_file = "data/cleaned_text.txt"
    
    print("Starting text cleaning...")
    clean_text_file(input_file, output_file)
    print(f"Text cleaning completed. Cleaned text saved to {output_file}")

if __name__ == "__main__":
    main()
