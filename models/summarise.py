from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_summarizer():
    # You can swap this with another summarization model if needed
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

# ---- Helper: break text into chunks ----
def chunk_text(text, max_words=800):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i + max_words])

# ---- Safe summarizer function ----
def summarize_text(text, max_length=130, min_length=30):
    # If the text is too long, split into chunks and summarize each
    words = text.split()
    if len(words) > 900:  # ~safe cutoff to avoid model's 1024 token limit
        summaries = []
        for chunk in chunk_text(text):
            summary = summarizer(
                chunk,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )[0]["summary_text"]
            summaries.append(summary)
        # Join the partial summaries and summarize again for a clean final summary
        combined_summary = " ".join(summaries)
        final_summary = summarizer(
            combined_summary,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )[0]["summary_text"]
        return final_summary
    else:
        return summarizer(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )[0]["summary_text"]
