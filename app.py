# app.py
import streamlit as st
from models.sentiment import analyze_sentiment

st.title("Sentiment Analysis Demo")

# Text input
user_text = st.text_area("Enter a comment:")

if st.button("Analyze"):
    if user_text.strip():
        result = analyze_sentiment(user_text)[0]
        st.write(f"**Sentiment:** {result['label']}")
        st.write(f"**Confidence:** {result['score']:.2f}")
    else:
        st.warning("Please enter some text.")
