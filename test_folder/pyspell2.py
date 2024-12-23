import re

def load_malayalam_words(filepath):
    words = set()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            words.add(word)
    return words

def correct_spelling_ml(text, word_list):
    words = re.findall(r"[\u0D00-\u0D7F]+", text) # Regex to extract Malayalam words
    corrected_words = []
    for word in words:
        if word in word_list:
            corrected_words.append(word)
        else:
            # Simple fallback: keep the original word
            corrected_words.append(word)
            print(f"Word '{word}' not found in dictionary.")
    return " ".join(corrected_words)

# Load the Malayalam wordlist
try:
    malayalam_words = load_malayalam_words(r"C:\Users\Administrator\Documents\GitHub\spell_checker_malayalam\spellchecker\libindic\spellchecker\data\ml_rootwords.txt") # Replace with your file path
except FileNotFoundError:
    print("Error: malayalam_wordlist.txt not found. Please provide a wordlist.")
    exit()

# Example usage:
text = "എന്റെ പേര് രാഹുല്‍ ആണ്."
corrected_text = correct_spelling_ml(text, malayalam_words)
print(f"Original: {text}")
print(f"Corrected: {corrected_text}")

text_with_errors = "മലയാളം സ്പെല്ലിംഗ ചെക്കർ പരീക്ഷണ ആണ്."
corrected_text_with_errors = correct_spelling_ml(text_with_errors, malayalam_words)
print(f"Original with errors: {text_with_errors}")
print(f"Corrected with errors: {corrected_text_with_errors}")

# (cenv) PS C:\Users\Administrator\Documents\GitHub\Text_cleaning> python test_folder/pyspell2.py
# Word 'എന്റെ' not found in dictionary.
# Word 'പേര്' not found in dictionary.
# Word 'രാഹുല്' not found in dictionary.
# Original: എന്റെ പേര് രാഹുല്‍ ആണ്.
# Corrected: എന്റെ പേര് രാഹുല് ആണ്
# Word 'സ്പെല്ലിംഗ്' not found in dictionary.
# Original with errors: മലയാളം സ്പെല്ലിംഗ് ചെക്കർ പരീക്ഷണം ആണ്.
# Corrected with errors: മലയാളം സ്പെല്ലിംഗ് ചെക്കർ പരീക്ഷണം ആണ്
# (cenv) PS C:\Users\Administrator\Documents\GitHub\Text_cleaning> 