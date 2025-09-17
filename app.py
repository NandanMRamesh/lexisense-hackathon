import streamlit as st
import pandas as pd
import nltk
from io import BytesIO
from models.summarise import summarize_text
from models.sentiment import analyze_sentiment
from models.wordcloud import generate_wordcloud
from visuals.speedometer import show_speedometer
from visuals.barchart import show_sentiment_bar_chart
from typing import Dict, Any, cast

st.set_page_config(page_title="LexiSense Dashboard", layout="wide")

st.title("📊 LexiSense – E-Consultation Comments Dashboard")

MAX_COMMENTS = 500  # Optional limit for very large CSVs

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

    # Persist uploaded file
    if uploaded_file is not None:
        st.session_state['uploaded_file_bytes'] = uploaded_file.read()

    analyze_disabled = uploaded_file is None
    if st.button("🚀 Analyze Comments", disabled=analyze_disabled):
        if 'uploaded_file_bytes' not in st.session_state:
            st.warning("Please upload a CSV file first!")
        else:
            uploaded_bytes_io = BytesIO(st.session_state['uploaded_file_bytes'])
            df = pd.read_csv(uploaded_bytes_io)

            if df.empty:
                st.error("CSV is empty. Please upload a valid CSV file.")
            elif "Comment" not in df.columns:
                st.error("CSV must have a 'Comment' column.")
            else:
                comments = df["Comment"].dropna().astype(str).tolist()
                # Clean empty/whitespace-only comments
                comments = [c.strip() for c in comments if c.strip()]
                if len(comments) == 0:
                    st.error("No valid comments found in the CSV.")
                else:
                    # Limit processed comments
                    comments = comments[:MAX_COMMENTS]

                    with st.spinner("Processing comments..."):
                        results = []
                        all_text = " ".join(comments)

                        # Overall summary
                        try:
                            overall_summary = summarize_text(all_text)
                        except Exception as e:
                            st.error(f"Error generating overall summary: {e}")
                            overall_summary = ""

                        for comment in comments:
                            try:
                                words = len(comment.split())
                                if words > 15:
                                    max_len = min(60, words)
                                    min_len = min(15, max_len)
                                    summary = summarize_text(comment, max_length=max_len, min_length=min_len)
                                else:
                                    summary = comment

                                sentiment = analyze_sentiment(comment)
                                sentiment = cast(Dict[str, Any], sentiment)
                                sentiment_label = sentiment.get("Sentiment", "neutral")
                                sentiment_score = sentiment.get("Score", 0.0)

                            except Exception as e:
                                st.error(f"Error processing comment: {e}")
                                summary = comment
                                sentiment_label = "neutral"
                                sentiment_score = 0.0

                            results.append({
                                "Comment": comment,
                                "Summary": summary,
                                "Sentiment": sentiment_label,
                                "Score": sentiment_score
                            })

                        results_df = pd.DataFrame(results)

                        # Debug preview
                        st.write("🔎 Debug Preview of results_df")
                        st.dataframe(results_df.head())

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
        st.info(overall_summary if overall_summary else "No summary available.")

        # Sentiment Distribution
        st.subheader("📈 Sentiment Distribution")

        col1, col2 = st.columns(2)

        with col1:
            try:
                if not results_df.empty:
                    show_sentiment_bar_chart(results_df)
                else:
                    st.write("No sentiment data to display.")
            except Exception as e:
                st.error(f"Error generating sentiment bar chart: {e}")

        with col2:
            st.subheader("Average Sentiment Score")
            try:
                sentiment_map = {"positive": 100, "neutral": 50, "negative": 0}
                numeric_scores = results_df["Sentiment"].str.lower().map(sentiment_map)
                numeric_scores = numeric_scores.dropna()
                if not numeric_scores.empty:
                    avg_sentiment_score = int(numeric_scores.mean())
                    show_speedometer(avg_sentiment_score)
                else:
                    st.write("No sentiment scores available to display.")
            except Exception as e:
                st.error(f"Error generating speedometer: {e}")

        # Word Cloud
        st.subheader("☁️ Word Cloud of Comments")
        try:
            if comments:
                generate_wordcloud(comments)
            else:
                st.write("No comments available for Word Cloud.")
        except Exception as e:
            st.error(f"Error generating Word Cloud: {e}")

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

        try:
            styled_df = results_df.style.apply(
                lambda col: col.map(highlight_sentiment) if col.name == "Sentiment" else [""] * len(col),
                axis=0
            )
            st.dataframe(styled_df, width="stretch")
        except Exception as e:
            st.error(f"Error displaying table: {e}")

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
        if 'uploaded_file_bytes' in st.session_state:
            del st.session_state['uploaded_file_bytes']
        st.rerun()
