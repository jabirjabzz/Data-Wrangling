import re
import logging
import stopwordsiso
from collections import Counter
from typing import List

def setup_logging(log_file: str = 'text_processing.log') -> logging.Logger:
    """
    Configure and set up logging for the text processing module.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# def is_malayalam(text: str) -> bool:
#     """
#     Check if text contains Malayalam characters.
#     """
#     if not isinstance(text, str):
#         logging.warning(f"Non-string input: {type(text)}")
#         return False
#     return bool(re.search(r'[\u0D00-\u0D7F]', text))

def clean_text(text: str) -> str:
    """
    Clean and normalize Malayalam text.
    """
    if not isinstance(text, str):
        logging.warning(f"Non-string input in clean_text: {type(text)}")
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\u0D00-\u0D7F\s.,!?]', '', text)
    return text.strip()

def remove_repetitive_text(text: str, max_repeats: int = 3) -> str:
    """
    Remove sentences that are repeated more than `max_repeats` times.

    Args:
        text (str): Input Malayalam text
        max_repeats (int): Maximum allowed repetitions for a sentence

    Returns:
        str: Text with overly repetitive sentences removed
    """
    sentences = re.split(r'(\.|!|\?)', text)  # Split into sentences keeping delimiters
    if len(sentences) < 2:
        return text  # If no sentence boundaries, return original text

    # Reconstruct sentences properly
    sentences = ["".join(pair) for pair in zip(sentences[0::2], sentences[1::2])]

    # Count sentence occurrences
    sentence_counts = Counter(sentences)

    # Filter sentences exceeding the repetition threshold
    filtered_sentences = [s for s in sentences if sentence_counts[s] <= max_repeats]

    return " ".join(filtered_sentences)

# def chunk_text(text: str, max_length: int = 512, overlap: int = 50) -> List[str]:
#     """
#     Split text into chunks with overlapping sections.
#     Each chunk is represented as a JSON object.

#     Args:
#         text (str): Input text to chunk
#         max_length (int): Maximum number of words per chunk
#         overlap (int): Number of words to overlap between chunks

#     Returns:
#         List[str]: List of JSON strings, each containing a chunk of text
#     """
#     words = text.split()
#     chunks = []
#     start = 0

#     while start < len(words):
#         end = min(start + max_length, len(words))
#         chunk_text = " ".join(words[start:end])
#         chunks.append({"text": chunk_text})
#         start += (max_length - overlap)

#     return chunks

def remove_stopwords(text: str, language: str = "ml") -> str:
    """
    Remove stopwords from the given text.
    """
    try:
        stop_words = set(stopwordsiso.stopwords(language))
        words = text.split()
        filtered_words = [word for word in words if word not in stop_words]
        return ' '.join(filtered_words)
    except Exception as e:
        logging.error(f"Stopword removal failed: {e}")
        return text