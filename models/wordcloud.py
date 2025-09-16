from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st

def generate_wordcloud(comments, max_words=100):
    """
    Generate and display a word cloud from a list of comments.
    """
    if isinstance(comments, str):
        text = comments
    else:
        text = " ".join(comments)

    # Create word cloud
    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        max_words=max_words,
        collocations=False  # prevents joining of common word pairs
    ).generate(text)

    # Plot with matplotlib
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
