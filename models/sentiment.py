from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import streamlit as st
from typing import Union, List, Dict

# Cache model + tokenizer so they're loaded only once
@st.cache_resource
def load_sentiment():
    model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_sentiment()

# Label mapping for Cardiff NLP Roberta
id2label = {0: "negative", 1: "neutral", 2: "positive"}


def analyze_sentiment(text: Union[str, List[str]]) -> Union[Dict[str, Union[str, float]], List[Dict[str, Union[str, float]]]]:
    """
    Analyze sentiment for a single string or a list of strings.
    Returns dict(s) with keys: Sentiment, Score.
    Score = softmax probability of the predicted class.
    """

    try:
        if isinstance(text, list):
            if not text:
                return []

            # Tokenize batch
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            with torch.no_grad():
                outputs = model(**inputs)
                probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

            results = []
            for i, row in enumerate(probs):
                label_id = torch.argmax(row).item()
                label = id2label[label_id]
                score = round(row[label_id].item(), 2)
                results.append({"Sentiment": label, "Score": score})

            return results

        else:  # Single string
            inputs = tokenizer(text, return_tensors="pt", truncation=True)
            with torch.no_grad():
                outputs = model(**inputs)
                probs = torch.nn.functional.softmax(outputs.logits, dim=-1)[0]

            label_id = torch.argmax(probs).item()
            label = id2label[label_id]
            score = round(probs[label_id].item(), 2)

            return {"Sentiment": label, "Score": score}

    except Exception as e:
        # Always return consistent keys
        return {"Sentiment": "neutral", "Score": 0.0}
