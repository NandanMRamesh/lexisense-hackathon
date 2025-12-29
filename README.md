# LexiSense – AI-powered Consultation Analysis System

LexiSense is an AI-powered system that analyzes large volumes of stakeholder feedback submitted during public consultations.  
It helps policymakers quickly understand **public sentiment, recurring concerns, and key themes** in draft legislations.

Built as part of **Smart India Hackathon 2025** (Problem Statement ID: 25035).

---

## Problem Context

During public consultations on draft legislations, thousands of comments may be received through the e-Consultation module.  
Manual analysis is time-consuming and risks overlooking critical feedback.

**LexiSense automates this process using NLP**, ensuring every comment is systematically analyzed and summarized.

---

## What LexiSense Does

- **Sentiment Analysis**  
  Classifies each comment as *Positive, Neutral, or Negative* using pretrained NLP models.

- **Automatic Summarization**  
  Converts long stakeholder comments into concise, meaningful summaries.

- **Word Cloud Visualization**  
  Highlights frequently used terms to surface dominant themes and concerns.

- **Interactive Dashboard**  
  Enables analysts to explore insights visually through charts and summaries.

---

## System Architecture (High-level)

Input Comments (Text / CSV)  
→ NLP Pipelines (Sentiment + Summarization)  
→ Visualization & Insights  
→ Streamlit Dashboard / API Output  

The system is designed to be **modular, offline-capable, and scalable**.

---

## Tech Stack

- **Language:** Python  
- **Machine Learning:** Hugging Face Transformers  
- **Frontend / Dashboard:** Streamlit  
- **Backend (future-ready):** FastAPI  
- **Visualization:** Matplotlib, WordCloud  
- **Data Handling:** Pandas  
- **Deployment:** Docker (containerized)

---

## Current Features

- Single & bulk comment analysis  
- Sentiment distribution charts  
- Automatic summaries of feedback  
- Word cloud generation  
- Prototype dashboard for demo & analysis  

---

## Planned Enhancements

- PostgreSQL integration for large-scale data storage  
- Aspect-based sentiment analysis (per clause / provision)  
- Multilingual support (Hindi & regional languages)  
- Conversational chatbot using RAG (Retrieval-Augmented Generation)  
- Cloud deployment (AWS / GCP / On-prem)

---

## Getting Started
Clone this repository:

```bash
git clone <your-repo-url>
cd LexiSense
```
---

## Set up a virtual environment:
```bash
python -m venv .venv
venv\Scripts\activate
```

## Install requirments.txt
```bash
pip install -r requirements.txt
```

## Run the Dashboard
```bash
streamlit run app.py
```

# Team
Team Radianites — Smart India Hackathon 2025
