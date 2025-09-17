# Required Libraries
from transformers import pipeline
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Initialize Hugging Face Pipelines
sentiment = pipeline("sentiment-analysis")
# Initialize summarization pipeline with specific model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Placeholder: Load your comments data here
# Replace this with actual data loading code later
# Example dummy data for development:
comments_data = [
    "I support the proposed amendment as it brings clarity.",
    "The new draft is confusing and needs improvement.",
    "The timeline for implementation is reasonable.",
    "I have no strong opinion on this draft."
]

# Create DataFrame
df_comments = pd.DataFrame(comments_data, columns=['comment_text'])

# Sentiment Analysis Function
def analyze_sentiment(comment):
    result = sentiment(comment)[0]
    label = result['label']
    score = result['score']
    
    # Optional: Mark low confidence as NEUTRAL
    if score < 0.6:
        label = "NEUTRAL"
    
    return label, score

# Summarization Function
def summarize_comment(comment):
    try:
        # Generate summary for individual comment or text
        summary_result = summarizer(comment, max_length=50, min_length=5, do_sample=False)
        summary_text = summary_result[0]['summary_text']
    except Exception:
        summary_text = comment  # fallback if summarization fails
    return summary_text

# Apply Sentiment Analysis
df_comments['Sentiment'], df_comments['Sentiment_Score'] = zip(*df_comments['comment_text'].map(analyze_sentiment))

# Apply Summarization
df_comments['Summary'] = df_comments['comment_text'].map(summarize_comment)

# Display analyzed DataFrame
print(df_comments)

# Generate Word Cloud from all comments
all_text = " ".join(df_comments['comment_text'].tolist())

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)

# Plot the word cloud
plt.figure(figsize=(15, 7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Word Cloud of Comments")
plt.show()

# Optional: Save results for frontend or further processing
df_comments.to_csv("comments_analyzed.csv", index=False)
