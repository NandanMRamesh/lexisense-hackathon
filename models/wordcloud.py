from wordcloud import WordCloud
import streamlit as st
import tempfile

def generate_wordcloud(comments, max_words=100):
    """
    Generate and display a word cloud from a list of comments.
    Uses tempfile + st.image to avoid Streamlit MediaFileStorage errors.
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

    # Save to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        wc.to_file(tmpfile.name)
        st.image(tmpfile.name, use_container_width=True)
