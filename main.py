import os
import sys
from scripts.clean_text import process_directory

def main():
    """
    Main function to execute text processing.
    """
    # Specific input and output paths
    input_dir = r"C:\Users\Administrator\Documents\GitHub\Text cleaning\data\input_data"
    output_dir = r"C:\Users\Administrator\Documents\GitHub\Text cleaning\data\output_data\root1"
    
    # Create output filename based on the input filename
    output_file = os.path.join(output_dir, "cleaned_data.jsonl")
    
    # Process directory
    process_directory(
        input_dir=input_dir,
        output_file=output_file  # Using output_file instead of output_dir
    )
    
    print("Processing complete. Exiting...")
    sys.exit(0)

if __name__ == "__main__":
    main()