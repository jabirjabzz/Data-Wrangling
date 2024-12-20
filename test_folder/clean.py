import json
import re
import pandas as pd
import os

def clean_data(input_path, output_path):
    """
    Cleans Malayalam text data from a JSON file, saves it to a CSV.

    Args:
        input_path: Path to the input JSON file.
        output_path: Path to save the cleaned CSV file.
    """

    try:
        # Check if the input file exists *before* attempting to open it.
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        with open(input_path, "r", encoding="utf-8") as f:
            try:  # Nested try for JSON decoding specifically.
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(f"Error decoding JSON in {input_path}: {e}") from e #Improved error message

        if not data: #Check if the loaded data is empty.
            raise ValueError(f"No data found in JSON file: {input_path}")

        df = pd.DataFrame(data)

        if df.empty: #Check if the DataFrame is empty after creation
            raise pd.errors.EmptyDataError(f"DataFrame is empty after processing JSON data from {input_path}.")


        df.dropna(subset=["content"], inplace=True)

        def clean_text(text):
            if not isinstance(text, str): #Check if text is string before cleaning it
                return "" #Or handle the non-string value as needed.
            text = re.sub(r"<.*?>", "", text)
            text = re.sub(r"[^\u0D00-\u0D7F\s]", "", text)
            text = re.sub(r"\s+", " ", text).strip()
            return text

        df["content"] = df["content"].apply(clean_text)
        df.drop_duplicates(subset=["content"], inplace=True)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False, encoding="utf-8")
        print(f"Data cleaning completed and saved to: {output_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error: {e}")
    except pd.errors.EmptyDataError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage (unchanged):
input_file = "malayalam_data.json"
output_file = "cleaned_data/cleaned_malayalam_data.csv"

clean_data(input_file, output_file)

# Example with a non-existent file:
# clean_data("non_existent_file.json", "output.csv")
