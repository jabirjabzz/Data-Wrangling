import re
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")

def remove_html_tags(text):
    """Remove HTML tags using BeautifulSoup."""
    return BeautifulSoup(text, "html.parser").get_text()

def remove_special_characters(text):
    """Remove special characters and numbers."""
    return re.sub(r"[^a-zA-Z\s]", "", text)

def remove_duplicates(lines):
    """Remove duplicate lines."""
    return list(set(lines))

def normalize_text(text):
    """Lowercase and strip extra whitespace."""
    return text.strip().lower()

def remove_stopwords(text):
    """Remove stopwords."""
    stop_words = set(stopwords.words("english"))
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    return " ".join(filtered_words)