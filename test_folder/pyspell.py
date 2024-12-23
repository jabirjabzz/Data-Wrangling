import json
from spellchecker import SpellChecker
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from googletrans import Translator

# spell_ml = SpellChecker(language='ml')  # Initialize spell checker for Malayalam
translator = Translator()

# def correct_spelling_ml(text):
#     words = text.split()
#     corrected_words = []
#     for word in words:
#         corrected_word = spell_ml.correction(word)
#         if corrected_word is not None:
#           corrected_words.append(corrected_word)
#         else:
#           corrected_words.append(word)
#     return " ".join(corrected_words)

def back_translate_ml(text, pivot_language='en'):  # Default pivot is English
    try:
        translated_to_pivot = translator.translate(text, dest=pivot_language).text
        back_translated = translator.translate(translated_to_pivot, dest='ml').text
        return back_translated
    except Exception as e: #Catching exceptions is important as network errors can occur
        print(f"Translation error: {e}")
        return None

def augment_malayalam_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    augmented_data = []

    for item in data:
        original_content = item['content']

        # 2. Sentence Splitting (if needed)
        sentences = sent_tokenize(original_content)

        for sentence in sentences:
            # 3. Back Translation
            back_translated_sentence = back_translate_ml(sentence)
            if back_translated_sentence:
                augmented_item = {
                    "url": item.get('url', ""),  # Keep other fields
                    "original_content": sentence,
                    "back_translation": back_translated_sentence,
                    "timestamp": item.get('timestamp', "")
                }
                augmented_data.append(augmented_item)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(augmented_data, outfile, ensure_ascii=False, indent=4)  # ensure_ascii=False is very important for non-ascii characters

# Example usage:
input_file = r"C:\Users\Administrator\Documents\GitHub\Text_cleaning\data\output_data\root1\http___campuslib.keralauniversity.ac.in_cgi-bin_koha_opac-shelves.pl_op_view_shelfnumber_126_sortfield_itemcallnumber_cleaned.json"  # your input json file
output_file = r"C:\Users\Administrator\Documents\GitHub\Text_cleaning\data\output_data\root2\augmented_malayalam_data.json"  # output json file
augment_malayalam_data(input_file, output_file)

# Example input file (malayalam_data.json)
# [
#     {"url":"test.com","content":"ഇതൊരു പരീക്ഷണം ആണ്.","timestamp":"12:00"},
#     {"url":"test2.com","content":"വേഗത കുറഞ്ഞ ഇന്റർനെറ്റ് കണക്ഷൻ കാരണം വെബ്സൈറ്റ് ലോഡ് ചെയ്യാൻ സമയമെടുത്തു.","timestamp":"13:00"}
# ]