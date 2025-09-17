import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def show_sentiment_bar_chart(results_df: pd.DataFrame):
    """
    Display a sentiment bar chart with counts, percentages, and avg scores.
    
    Args:
        results_df (pd.DataFrame): DataFrame with 'Sentiment' and 'Score' columns
    """
    if "Sentiment" not in results_df.columns or results_df.empty:
        st.warning("No sentiment data available to display bar chart.")
        return

    # Count per sentiment
    sentiment_counts = results_df["Sentiment"].value_counts()
    total = sentiment_counts.sum()
    percentages = (sentiment_counts / total * 100).round(1)

    # Average score per sentiment
    avg_scores = results_df.groupby("Sentiment")["Score"].mean().round(2)

    # Custom colors
    colors = {
        "positive": "#00cc96",
        "neutral": "#ffcc00",
        "negative": "#ff4c4c"
    }

    fig = go.Figure()

    for sentiment in sentiment_counts.index:
        fig.add_trace(go.Bar(
            x=[sentiment],
            y=[sentiment_counts[sentiment]],
            text=f"{sentiment_counts[sentiment]} ({percentages[sentiment]}%)",
            textposition="auto",
            marker_color=colors.get(sentiment, "#636EFA")
        ))

    fig.update_layout(
        title="Sentiment Counts",
        yaxis_title="Number of Comments",
        xaxis_title="Sentiment",
        template="simple_white",
        height=450,
        margin=dict(l=40, r=40, t=50, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)
