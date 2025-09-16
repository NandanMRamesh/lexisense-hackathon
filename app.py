import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from models.summarise import summarize_text
from models.sentiment import analyze_sentiment
from models.wordcloud import generate_wordcloud

st.set_page_config(page_title="LexiSense Dashboard", layout="wide")

st.title("📊 LexiSense – E-Consultation Comments Dashboard")
st.write("Upload comments CSV to get **summaries, sentiment insights, and visualizations**.")

# Initialize df
df = None
comments = []

# File upload only
uploaded_file = st.file_uploader("📂 Upload a CSV file with a 'Comment' column", type=["csv"])

if uploaded_file:
    tmp_df = pd.read_csv(uploaded_file)
    if "Comment" not in tmp_df.columns:
        st.error("CSV must have a 'Comment' column.")
    else:
        df = tmp_df
        comments = df["Comment"].dropna().astype(str).tolist()

if st.button("🚀 Analyze Comments"):
    if not comments:
        st.warning("Please upload a valid CSV with comments.")
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

            results_df = pd.DataFrame(results)

        # ---- Dashboard Layout ----
        st.success("✅ Analysis Completed!")

        # Collapsible raw comments (only if df exists)
        if df is not None:
            with st.expander("📑 View Uploaded Comments"):
                st.dataframe(df, use_container_width=True)

        # Overall Summary
        st.subheader("📝 Overall Summary")
        st.info(overall_summary)

        # Sentiment Distribution
        st.subheader("📈 Sentiment Distribution")
        sentiment_counts = results_df["Sentiment"].value_counts()

        col1, col2 = st.columns(2)

        with col1:
            st.bar_chart(sentiment_counts)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(
                sentiment_counts.to_numpy(),
                labels=sentiment_counts.index.tolist(),
                autopct="%1.1f%%",
                startangle=90
            )
            ax.axis("equal")
            st.pyplot(fig)

        # Word Cloud
        st.subheader("☁️ Word Cloud of Comments")
        generate_wordcloud(comments)

        # Detailed Table (with color-coded sentiment)
        st.subheader("🔍 Detailed Comment Analysis")

        def highlight_sentiment(val):
            if val.lower() == "positive":
                return "color: green; font-weight: bold;"
            elif val.lower() == "negative":
                return "color: red; font-weight: bold;"
            elif val.lower() == "neutral":
                return "color: gray; font-weight: bold;"
            return ""

        styled_df = results_df.style.apply(
            lambda col: col.map(highlight_sentiment) if col.name == "Sentiment" else [""] * len(col),
            axis=0
        )
        st.dataframe(styled_df, use_container_width=True)

        # Download Option
        st.download_button(
            label="📥 Download Analyzed Results (CSV)",
            data=results_df.to_csv(index=False).encode("utf-8"),
            file_name="analyzed_comments.csv",
            mime="text/csv",
        )
