from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_summarizer():
    return pipeline("summarization")

summarizer = load_summarizer()

def summarize_text(text, max_length=130, min_length=30):
    return summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
