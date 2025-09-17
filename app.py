import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from models.summarise import summarize_text
from models.sentiment import analyze_sentiment
from models.wordcloud import generate_wordcloud
from visuals.speedometer import show_speedometer

st.set_page_config(page_title="LexiSense Dashboard", layout="wide")

st.title("📊 LexiSense – E-Consultation Comments Dashboard")

# Initialize session state
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "results_df" not in st.session_state:
    st.session_state.results_df = None
if "overall_summary" not in st.session_state:
    st.session_state.overall_summary = None
if "comments" not in st.session_state:
    st.session_state.comments = []

# ------------------------
# BEFORE ANALYSIS → Show uploader
# ------------------------
if not st.session_state.analysis_done:
    st.write("Upload comments CSV to get **summaries, sentiment insights, and visualizations**.")
    uploaded_file = st.file_uploader("📂 Upload a CSV file with a 'Comment' column", type=["csv"])

    if st.button("🚀 Analyze Comments") and uploaded_file:
        df = pd.read_csv(uploaded_file)

        if "Comment" not in df.columns:
            st.error("CSV must have a 'Comment' column.")
        else:
            comments = df["Comment"].dropna().astype(str).tolist()

            if len(comments) == 0:
                st.error("No valid comments found in the CSV.")
            else:
                with st.spinner("Processing comments..."):
                    results = []
                    all_text = " ".join(comments)

                    overall_summary = summarize_text(all_text)

                    for comment in comments:
                        if len(comment.split()) > 15:
                            summary = summarize_text(comment, max_length=60, min_length=15)
                        else:
                            summary = comment
                        sentiment = analyze_sentiment(comment)
                        results.append({
                            "Comment": comment,
                            "Summary": summary,
                            **sentiment
                        })

                    results_df = pd.DataFrame(results)

                # Save results in session_state
                st.session_state.analysis_done = True
                st.session_state.results_df = results_df
                st.session_state.overall_summary = overall_summary
                st.session_state.comments = comments
                st.rerun()

# ------------------------
# AFTER ANALYSIS → Show dashboard
# ------------------------
else:
    results_df = st.session_state.results_df
    overall_summary = st.session_state.overall_summary
    comments = st.session_state.comments

    if results_df is None or results_df.empty:
        st.warning("⚠️ No analysis results available.")
    else:
        st.success("✅ Analysis Completed!")

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
            st.subheader("🚦 Average Sentiment Score")
            sentiment_map = {"positive": 100, "neutral": 50, "negative": 0}
            numeric_scores = results_df["Sentiment"].map(sentiment_map)
            numeric_scores = numeric_scores.dropna()
            if not numeric_scores.empty:
                 avg_sentiment_score = int(numeric_scores.mean())
                 show_speedometer(avg_sentiment_score)
            else: 
                 st.write("No sentiment scores available to display.")


             # Word Cloud
        st.subheader("☁️ Word Cloud of Comments")
        generate_wordcloud(comments)


        # Detailed Table (with color-coded sentiment)
        st.subheader("🔍 Detailed Comment Analysis")

        def highlight_sentiment(val):
            if isinstance(val, str):
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

    # Restart button
    if st.button("🔄 New Analysis"):
        st.session_state.analysis_done = False
        st.session_state.results_df = None
        st.session_state.overall_summary = None
        st.session_state.comments = []
        st.rerun()
