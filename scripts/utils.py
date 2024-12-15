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

def chunk_text(text, max_length=512, overlap=50):
    """
    Split text into chunks of specified maximum length with overlap.
    
    Args:
        text (str): Input text to be chunked
        max_length (int): Maximum number of words per chunk
        overlap (int): Number of words to overlap between chunks
    
    Returns:
        list: List of text chunks
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + max_length, len(words))
        chunks.append(" ".join(words[start:end]))
        start += (max_length - overlap)
    return chunks

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