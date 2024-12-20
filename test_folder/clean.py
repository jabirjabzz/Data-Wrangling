import json
import re
import pandas as pd
import os
import glob
from pathlib import Path

def clean_data(input_pattern, output_dir):
    """Cleans Malayalam text data from JSON files and saves to CSV."""
    try:
        print(f"Input pattern: {input_pattern}")  # Debug: Print the input pattern
        json_files = glob.glob(input_pattern)
        print(f"Found files: {json_files}")  # Debug: Print the found files
        if not json_files:
            raise FileNotFoundError(f"No JSON files found matching pattern: {input_pattern}")

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        for input_file in json_files:
            print(f"Processing file: {input_file}")
            try:
                with open(input_file, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        if not isinstance(data, list):  # Check if data is a list 
                            data = [data]  # Wrap single object in a list
                        print(f"Data loaded: {data}")
                    except json.JSONDecodeError as e:
                        print(f"Warning: JSONDecodeError in {input_file}: {e}")
                        continue

                if not data:
                    print(f"Warning: No data in {input_file}")
                    continue

                df = pd.DataFrame(data)
                if df.empty:
                    print(f"Warning: Empty DataFrame after creation from {input_file}")
                    continue

                print(f"DataFrame columns: {df.columns}")
                if "content" not in df.columns:
                    print(f"Warning: 'content' column missing in {input_file}")
                    continue

                df.dropna(subset=["content"], inplace=True)
                print(f"DataFrame length after dropna: {len(df)}")

                def clean_text(text):
                    if not isinstance(text, str):
                        return ""
                    text = re.sub(r"<.*?>", "", text)
                    text = re.sub(r"[^\u0D00-\u0D7F\s]", "", text)
                    text = re.sub(r"\s+", " ", text).strip()
                    return text

                df["content"] = df["content"].apply(clean_text)
                df.drop_duplicates(subset=["content"], inplace=True)
                print(f"DataFrame length after drop_duplicates: {len(df)}")

                if len(df) == 0:
                    print(f"Warning: Empty DataFrame after cleaning in {input_file}")
                    continue

                base_name = Path(input_file).stem
                output_file = Path(output_dir) / f"{base_name}_cleaned.csv"
                df.to_csv(output_file, index=False, encoding="utf-8")
                print(f"Data from {input_file} saved to: {output_file}")

            except Exception as e:
                print(f"Error processing {input_file}: {e}")

    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
    except Exception as e:
        print(f"Overall Error: {e}")

# Example Usage (Relative Paths - Recommended):
input_pattern = "C:\\Users\\Administrator\\Documents\\GitHub\\Text cleaning\\data\\sample input\\*.json"  # Matches all .json files in the 'data' directory
output_directory = "C:\\Users\Administrator\\Documents\GitHub\\Text cleaning\\test_folder\\test_output"
clean_data(input_pattern, output_directory)


