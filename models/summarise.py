from transformers import pipeline, AutoTokenizer
import streamlit as st

@st.cache_resource
def load_summarizer():
    return pipeline(
        "summarization", 
        model="sshleifer/distilbart-cnn-12-6", 
        revision="a4f8f3e"
    )

summarizer = load_summarizer()
tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")

def summarize_text(text, max_length=130, min_length=30):
    """
    Summarizes input text using the distilbart model.
    Truncates input if longer than model max length.
    Returns summary or an error message on failure.
    """
    max_input_len = tokenizer.model_max_length
    
    # Truncate text to max input length if necessary
    if len(text) > max_input_len:
        text = text[:max_input_len]

    try:
        summary = summarizer(
            text, 
            max_length=max_length, 
            min_length=min_length, 
            do_sample=False
        )[0]['summary_text']
        return summary
    except Exception as e:
        return f"[Summary Error] {str(e)}"
