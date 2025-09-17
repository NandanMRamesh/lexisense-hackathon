import plotly.graph_objects as go
import streamlit as st
import time

def show_speedometer(sentiment_score: int):
    placeholder = st.empty()

    for score in range(0, sentiment_score + 1, 2):  # Smooth animation
        fig = go.Figure(go.Indicator(
            mode="gauge+number",  # Removed delta
            value=score,
            number={
                'suffix': "%",
                'font': {'size': 48, 'color': '#1f77b4'}
            },
            domain={'x': [0, 1], 'y': [0, 1]},
            title={
                'text': "<b>Sentiment Score</b>",
                'font': {'size': 28, 'color': '#333333'}
            },
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "#333333"},
                'bar': {'color': '#1f77b4', 'thickness': 0.3},
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
