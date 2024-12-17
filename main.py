import os
import sys
from scripts.clean_text import process_directory

def main():
    """
    Main function to execute text processing.
    """
    # Specific input and output paths
    input_dir = r"C:\Users\Administrator\Documents\GitHub\Text cleaning\data\input_data"
    output_file = os.path.join(r"C:\Users\Administrator\Documents\GitHub\Text cleaning\data\output_data\root1", "cleaned_data.jsonl")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Process directory
    process_directory(
        input_dir=input_dir,
        output_file=output_file
    )
    print("Processing complete. Exiting...")
    sys.exit(0)

if __name__ == "__main__":
    main()
