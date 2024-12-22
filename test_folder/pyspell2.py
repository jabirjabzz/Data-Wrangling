# from indicnlp.spellchecker import SpellChecker

# # Initialize the spell checker for Malayalam
# SPELL = SpellChecker(language='ml')

# def correct_spelling_ml(text):
#     corrected_words = []
#     for word in text.split():
#         corrected_word = SPELL.correct(word)
#         corrected_words.append(corrected_word)
#     return " ".join(corrected_words)

# # Example Usage
# text = "എന്റെ പേര് രാഹുല്‍ ആണ്." #Example text
# corrected_text = correct_spelling_ml(text)
# print(f"Original Text: {text}")
# print(f"Corrected Text: {corrected_text}")

# text_with_errors = "മലയാളം സ്പെല്ലിംഗ് ചെക്കർ പരീക്ഷണം ആണ്."
# corrected_text_with_errors = correct_spelling_ml(text_with_errors)
# print(f"Original Text with errors: {text_with_errors}")
# print(f"Corrected Text with errors: {corrected_text_with_errors}")





# from import spacy
# from spacy_hunspell import spaCyHunSpell

# # Load a blank spacy model
# nlp = spacy.blank("xx")

# # Add the Hunspell spell checker to the pipeline
# hunspell = spaCyHunSpell(nlp, "path/to/hunspell_dictionaries")
# nlp.add_pipe(hunspell)

# # Example usage
# text = "ഇത് ഒരു ഉദാഹരണ വാക്യം ആണ്"
# doc = nlp(text)

# for token in doc:
#     if not token._.hunspell_spell:
#         print(f"Misspelled word: {token.text}")
#         print(f"Suggestions: {token._.hunspell_suggest}") import sanscript
# from indic_transliteration.sanscript import transliterate

# # Example usage
# text = "ഇത് ഒരു ഉദാഹരണ വാക്യം ആണ്"
# transliterated_text = transliterate(text, sanscript.MALAYALAM, sanscript.ITRANS)
# print(transliterated_text)



from spellchecker import SpellChecker

# Initialize the spell checker for Malayalam
spell = SpellChecker(language=None, case_sensitive=True)
spell.word_frequency.load_text_file(r"C:\Users\Administrator\Documents\GitHub\Text_cleaning\test_folder\malayalaword.txt")

# Example usage
text = "ഇത് ഒരു ഉദാഹരണ വാക്യം ആണ്"
words = text.split()

for word in words:
    if word not in spell:
        print(f"Misspelled word: {word}")
        print(f"Suggestions: {spell.candidates(word)}")