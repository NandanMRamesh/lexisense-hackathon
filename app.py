import streamlit as st
import pandas as pd
from models.sentiment import analyze_sentiment

st.title("Sentiment Analysis Demo")

# Text input
user_text = st.text_area("Enter a comment:")
uploaded_file = st.file_uploader("Upload CSV with a 'comment' column", type="csv")


if st.button("Analyze"):
    if user_text.strip():
        result = analyze_sentiment(user_text)[0]
        st.write(f"**Sentiment:** {result['label']}")
        st.write(f"**Confidence:** {result['score']:.2f}")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df["Sentiment"] = analyze_sentiment(df["comment"].tolist())
        st.dataframe(df)

    else:
        st.warning("Please enter some text.")


    
