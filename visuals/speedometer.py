# speedometer.py
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import time


def compute_overall_sentiment(results_df: pd.DataFrame) -> int:
    """
    Compute overall sentiment score (0–100) from a results dataframe.
    Maps sentiments into numeric values:
        negative = 0, neutral = 50, positive = 100
    """
    if results_df.empty or "Sentiment" not in results_df.columns:
        return 50  # Neutral fallback

    mapping = {"negative": 0, "neutral": 50, "positive": 100}
    scores = results_df["Sentiment"].map(mapping).dropna()

    if scores.empty:
        return 50  # Neutral fallback

    return int(scores.mean().round())


def show_speedometer(sentiment_score: int):
    """
    Display a smooth animated gauge showing overall sentiment score.
    Needle color changes based on sentiment zone.
    Also shows a textual label: Mostly Negative, Neutral, Mostly Positive.
    """
    placeholder = st.empty()

    # Determine needle color and label
    if sentiment_score <= 33:
        needle_color = "#ff4c4c"  # Red
        sentiment_label = "Mostly Negative"
    elif sentiment_score <= 66:
        needle_color = "#ffcc00"  # Yellow
        sentiment_label = "Neutral"
    else:
        needle_color = "#00cc96"  # Green
        sentiment_label = "Mostly Positive"

    # Show textual label above gauge
    st.markdown(f"### Overall Sentiment: **{sentiment_label}**")

    for score in range(0, sentiment_score + 1, 2):  # Smooth animation
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            number={
                'suffix': "%",
                'font': {'size': 48, 'color': needle_color}
            },
            domain={'x': [0, 1], 'y': [0, 1]},
            title={
                'text': "<b>Sentiment Score</b>",
                'font': {'size': 28, 'color': '#333333'}
            },
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "#333333"},
                'bar': {'color': "#1f77b4", 'thickness': 0.3},
                'bgcolor': "#f5f5f5",
                'borderwidth': 2,
                'bordercolor': "#dddddd",
                'steps': [
                    {'range': [0, 33], 'color': '#ff4c4c'},      # Red (negative)
                    {'range': [33, 66], 'color': '#ffcc00'},    # Yellow (neutral)
                    {'range': [66, 100], 'color': '#00cc96'}    # Green (positive)
                ],
                'threshold': {
                    'line': {'color': "#000000", 'width': 4},
                    'thickness': 0.75,
                    'value': score
                }
            }
        ))

        fig.update_layout(
            paper_bgcolor="white",
            font={'color': "#333333", 'family': "Arial"},
            margin=dict(l=40, r=40, t=50, b=40),
            height=400
        )

        placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.02)  # Smooth animation
