import re
import logging
import stopwordsiso
from typing import List, Optional

def setup_logging(log_file: str = 'text_processing.log') -> logging.Logger:
    """
    Configure and set up logging for the text processing module.
    
    Args:
        log_file (str): Path to the log file
    
    Returns:
        logging.Logger: Configured logger instance
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

def is_malayalam(text: str) -> bool:
    """
    Check if text contains Malayalam characters.
    
    Args:
        text (str): Input text to check
    
    Returns:
        bool: True if Malayalam characters are present, False otherwise
    """
    if not isinstance(text, str):
        logging.warning(f"Non-string input: {type(text)}")
        return False
    
    malayalam_match = re.search(r'[\u0D00-\u0D7F]', text)
    
    if not malayalam_match:
        logging.debug(f"No Malayalam characters found in text: {text[:100]}...")
    
    return bool(malayalam_match)

def clean_text(text: str) -> str:
    """
    Clean and normalize Malayalam text.
    
    Args:
        text (str): Input text to clean
    
    Returns:
        str: Cleaned text
    """
    if not isinstance(text, str):
        logging.warning(f"Non-string input in clean_text: {type(text)}")
        return ""
    
    # Normalize spaces and remove non-Malayalam characters
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\u0D00-\u0D7F\s.,!?]', '', text)
    return text.strip()

def chunk_text(text: str, max_length: int = 512, overlap: int = 50) -> List[str]:
    """
    Split text into chunks with specified maximum length and overlap.
    
    Args:
        text (str): Input text to chunk
        max_length (int): Maximum number of words per chunk
        overlap (int): Number of words to overlap between chunks
    
    Returns:
        List[str]: List of text chunks
    """
    words = text.split()
    chunks = []
    start = 0
    
    while start < len(words):
        end = min(start + max_length, len(words))
        chunks.append(" ".join(words[start:end]))
        start += (max_length - overlap)
    
    return chunks

def remove_stopwords(text: str, language: str = "ml") -> str:
    """
    Remove stopwords from the given text.
    
    Args:
        text (str): Input text
        language (str): Language code (default: "ml" for Malayalam)
    
    Returns:
        str: Text with stopwords removed
    """
    try:
        stop_words = set(stopwordsiso.stopwords(language))
        words = text.split()
        filtered_words = [word for word in words if word not in stop_words]
        return ' '.join(filtered_words)
    except Exception as e:
        logging.error(f"Stopword removal failed: {e}")
        return text