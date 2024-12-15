import re
import stopwordsiso

def is_malayalam(text):
    """Check if text contains Malayalam characters."""
    return bool(re.search(r'[\u0D00-\u0D7F]', text))

def clean_text(text):
    """Clean and normalize Malayalam text."""
    # Remove unwanted characters
    text = re.sub(r'\s+', ' ', text)  # Normalize spaces
    text = re.sub(r'[^\u0D00-\u0D7F\s.,!?]', '', text)  # Keep only Malayalam characters and punctuation
    return text.strip()

def filter_stopwords(text, language="ml"):
    """
    Filters stop words from a given text using the stopwordsiso package.

    Args:
        text (str): The input text.
        language (str): The ISO 639-1 language code (e.g., "ml" for Malayalam).

    Returns:
        list or None: A list of words with stop words removed, or None if the language is not supported.
    """
    try:
        stop_words = set(stopwordsiso.stopwords(language))
    except KeyError:
        print(f"Language '{language}' is not supported by stopwordsiso.")
        return None
    except Exception as e:  # Catch any other exceptions
        print(f"An unexpected error occurred: {e}")
        return None

    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    return filtered_words

def remove_stopwords(text):
    """Remove Malayalam stopwords."""
    # Filter stopwords
    filtered_words = filter_stopwords(text, language="ml")
    
    # If filtering failed, return original text
    if filtered_words is None:
        return text
    
    return ' '.join(filtered_words)