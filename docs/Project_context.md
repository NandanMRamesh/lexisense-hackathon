# 📘 Project Context — LexiSense Hackathon

This file documents the **tools, approach, and important decisions** for the LexiSense project.  
It is meant to serve as a reference for future developers (or an LLM) so the project context is always clear.

---

## 🔹 Project Overview
- **Problem Statement ID:** 25035  
- **Title:** Sentiment analysis of comments received through E-consultation module  
- **Organization:** Ministry of Corporate Affairs (MoCA)  
- **Goal:** Analyze stakeholder feedback on draft legislations to help policymakers understand public opinion faster.  

---

## 🔹 Approach
1. **Input**  
   - Stakeholders submit comments (text or CSV for demo).  

2. **Processing (via AI pipelines)**  
   - **Sentiment Analysis:** Classify comments as Positive / Negative / Neutral.  
   - **Summarization:** Generate short summaries of longer comments.  
   - **Word Cloud:** Visualize frequent keywords across all comments.  

3. **Output (via Streamlit dashboard)**  
   - Interactive interface with:  
     - Single comment analysis  
     - Bulk CSV upload + analysis  
     - Word cloud visualization  
     - Sentiment distribution charts  

---

## 🔹 Tools & Libraries
### 🧠 Machine Learning (Hugging Face Pipelines)
- **Transformers Library:** [https://huggingface.co/docs/transformers](https://huggingface.co/docs/transformers)  
- **Pipelines used:**
  - `sentiment-analysis` → Sentiment classification  
  - `summarization` → Comment summarization  

### 🎨 Visualization
- **Streamlit** (UI + dashboard) → [https://docs.streamlit.io](https://docs.streamlit.io)  
- **WordCloud** (keyword visualization) → [https://amueller.github.io/word_cloud/](https://amueller.github.io/word_cloud/)  
- **Matplotlib** (basic plots for sentiment distribution)  

### 📂 Data Handling
- **CSV files** with Pandas for reading/writing.  
- Example: `sample_comments.csv` → analyzed → `processed.csv`  

---

## 🔹 Architecture (Simplified)
User Comment(s)↓Streamlit Frontend (UI)↓Hugging Face Pipelines├── Sentiment Analysis├── Summarization└── Word Cloud↓Dashboard Output (tables, charts, images)


---

## 🔹 Decisions Taken
- ✅ Use **Streamlit** instead of React/FastAPI for simplicity and speed.  
- ✅ Use **Hugging Face pipelines** (pretrained models) → no training required.  
- ✅ Use **CSV files** for storage instead of a database.  
- ✅ Run models **locally** → free, offline after first download.  
- ❌ Dropped old laptop server idea (too complex networking).  
- ✅ Deployment option: **Streamlit Cloud (free)** for public demo URL.  

---

## 🔹 Future Improvements
- Use **FastAPI + database** (e.g., PostgreSQL) for production scale.  
- Add **aspect-based sentiment** (per clause/section of legislation).  
- Deploy on **cloud VM** for reliability (AWS/GCP).  
- Add **multi-language support** (comments in Hindi/regional languages).  
- Improve **summarization accuracy** with fine-tuned models.  

---

## 🔹 Team Distribution (6 Members)
- Person 1 → Team Lead / Integrator  
- Person 2 → Streamlit UI  
- Person 3 → Sentiment Analysis  
- Person 4 → Summarization  
- Person 5 → Word Cloud & Charts  
- Person 6 → Backend Testing & Optimizations  

---

## 🔹 Hackathon Timeline
- **Day 1:** Setup, test Hugging Face pipelines, prepare sample CSVs.  
- **Day 2:** Build Streamlit dashboard, integrate ML functions, add visualizations.  
- **Day 3:** Testing, UI polish, final demo prep.  

---

## 🔹 Key Takeaways
- Hugging Face pipelines are **ideal for hackathons** → plug-and-play AI.  
- Streamlit makes **professional dashboards fast**.  
- Focus on **polish + working demo** over complex backend.  
- Keep everything **offline-capable** to avoid internet issues in demo.  
