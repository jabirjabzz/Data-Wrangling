import os
import sys
from scripts.clean_text import process_directory

def main():
    """
    Main function to execute text processing.
    Each input JSON file will have its own cleaned output file.
    """
    input_dir = r"C:\Users\Administrator\Documents\GitHub\Text cleaning\data\sample input"
    output_dir = r"C:\Users\Administrator\Documents\GitHub\Text cleaning\data\output_data\root1"
    
    # Process directory
    process_directory(
        input_dir=input_dir,
        output_dir=output_dir
    )
    
    print("Processing complete. Each file has been processed and saved with '_cleaned' suffix.")
    sys.exit(0)

if __name__ == "__main__":
    main()