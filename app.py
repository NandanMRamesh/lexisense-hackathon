import streamlit as st
import pandas as pd
from models.summarise import summarize_text
from models.sentiment import analyze_sentiment

st.title("📝 E-Consultation Comments Dashboard")
st.write("Paste comments or upload a CSV file to get summaries and sentiment analysis:")

# Option 1: Text input
user_input = st.text_area("Paste comments here (one per line)", height=200)
st.write("Large comments might be chunked for processing.")
# Option 2: CSV file upload
uploaded_file = st.file_uploader("Upload a CSV file with a 'Comment' column", type=["csv"])

comments = []

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if "Comment" not in df.columns:
        st.error("CSV must have a 'Comment' column.")
    else:
        comments = df["Comment"].dropna().astype(str).tolist()
elif user_input.strip():
    comments = [user_input.strip()]

if st.button("Analyze & Summarize"):
    if not comments:
        st.warning("Please enter or upload some comments to analyze.")
    else:
        with st.spinner("Processing comments..."):
            results = []
            all_text = " ".join(comments)

            # Summarize all comments together
            overall_summary = summarize_text(all_text)

            for comment in comments:
                if len(comment.split()) > 15:
                    summary = summarize_text(comment, max_length=60, min_length=15)
                else:
                    summary = comment  # Too short to summarize

                sentiment = analyze_sentiment(comment)
                results.append({
                    "Comment": comment,
                    "Summary": summary,
                    **sentiment
                })

            st.subheader("Overall Summary of All Comments:")
            st.info(overall_summary)

            st.subheader("Detailed Comment Analysis:")
            st.dataframe(results)
