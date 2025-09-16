from transformers import pipeline
import streamlit as st

# Label mapping for Cardiff NLP RoBERTa
label_map = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive",
    "negative": "negative",
    "neutral": "neutral",
    "positive": "positive"
}

@st.cache_resource
def load_sentiment():
    return pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        device=-1  # CPU only
    )

sentiment_analyzer = load_sentiment()

def analyze_sentiment(text):
    """
    Analyzes sentiment for a single string or list of strings.
    Returns dict(s) with keys: Sentiment, Score.
    """
    try:
        if isinstance(text, list):
            if not text:
                return []
            results = sentiment_analyzer(text)
            output = []
            for res in results:
                label = res.get("label")
                if not isinstance(label, str):
                    label = "neutral"
                sentiment_label = label_map.get(label, "neutral").lower()
                score = round(res.get("score", 0.0), 2)
                output.append({"Sentiment": sentiment_label, "Score": score})
            return output
        else:
            result = sentiment_analyzer(text)[0]
            label = result.get("label")
            if not isinstance(label, str):
                label = "neutral"
            sentiment_label = label_map.get(label, "neutral").lower()
            score = round(result.get("score", 0.0), 2)
            return {"Sentiment": sentiment_label, "Score": score}
    except Exception as e:
        # Always return consistent keys
        return {"Sentiment": "neutral", "Score": 0.0}
