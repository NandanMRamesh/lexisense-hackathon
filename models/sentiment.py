from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import streamlit as st

@st.cache_resource
def load_sentiment():
    return pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")

sentiment_analyzer = load_sentiment()

def analyze_sentiment(text):
    result = sentiment_analyzer(text)[0]
    return {
        "Sentiment": result['label'],
        "Score": round(result['score'], 2)
    }
