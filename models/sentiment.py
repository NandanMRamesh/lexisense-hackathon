from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_sentiment():
    return pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")

def analyze_sentiment(text):
    sentiment_analyzer = load_sentiment()
    result = sentiment_analyzer(text)[0]
    label = result["label"].lower()
    score = result["score"]
    return {"Sentiment": label, "Confidence": round(score, 2)}
