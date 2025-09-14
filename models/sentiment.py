# sentiment_utils.py
from transformers import pipeline

# Load the model once (saves time)
sentiment_pipeline = pipeline("sentiment-analysis") #type: ignore

def analyze_sentiment(texts):
    """
    Run sentiment analysis on a single string or a list of strings.
    Returns a list of dicts with 'label' and 'score'.
    """
    if isinstance(texts, str):
        texts = [texts]

    return sentiment_pipeline(texts)
