import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from models.sentiment import analyze_sentiment   # your custom model
from nltk.sentiment import SentimentIntensityAnalyzer

st.title("Sentiment Analysis Demo")

# Text input + File upload
user_text = st.text_area("Enter a comment:")
uploaded_file = st.file_uploader("Upload CSV with a 'comment' column", type="csv")

if st.button("Analyze"):
    # --- Analyze user text ---
    if user_text.strip():
        result = analyze_sentiment(user_text)[0]   # your model output
        st.write(f"*Sentiment:* {result['label']}")
        st.write(f"*Confidence:* {result['score']:.2f}")

    # --- Analyze CSV and Generate WordCloud ---
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)

            if "comment" not in df.columns:
                st.error("CSV must contain a 'comment' column.")
            else:
                # Analyze all comments
                results = analyze_sentiment(df["comment"].tolist())
                df["Sentiment"] = [r["label"] for r in results]
                df["Confidence"] = [r["score"] for r in results]

                st.subheader("Uploaded Data with Sentiment")
                st.dataframe(df)

                # WordCloud only from CSV comments with chosen sentiment
           
            sia = SentimentIntensityAnalyzer()

            def classify_comment_vader(comment):
             score = sia.polarity_scores(comment)['compound']
             if score >= 0.05:
               return "Positive"
             elif score <= -0.05:
                 return "Negative"
             else:
                return None
            all_comments = df["comment"].tolist()
            filtered_comments = [c for c in all_comments if classify_comment_vader(c) ]
            if filtered_comments:
                    text = " ".join(filtered_comments)
                    wordcloud = WordCloud(
                        width=800,
                        height=400,
                        background_color="white",
                        stopwords=STOPWORDS
                    ).generate(text)

                    plt.figure(figsize=(10, 5))
                    plt.imshow(wordcloud, interpolation="bilinear")
                    plt.axis("off")
                    st.pyplot(plt)

        except Exception as e:
            st.error(f"Error reading file: {e}")

    # --- If neither ---
    if not user_text.strip() and not uploaded_file:
        st.warning("Please enter some text or upload a CSV file.")