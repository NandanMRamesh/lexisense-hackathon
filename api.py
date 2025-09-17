from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd
from models.sentiment import analyze_sentiment

app = FastAPI(title="Sentiment Analysis API")

# Request model for single text
class TextRequest(BaseModel):
    text: str
@app.post("/analyze-text")
def analyze_text(req: TextRequest):
    result = analyze_sentiment(req.text)
    return {
        "sentiment": result["Sentiment"],
        "confidence": result["Score"]
    }

@app.post("/analyze-csv")
async def analyze_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    if "comment" not in df.columns:
        return {"error": "CSV must have a 'comment' column"}

    sentiments = analyze_sentiment(df["comment"].tolist())
    df["Sentiment"] = [s["Sentiment"] for s in sentiments]
    df["Confidence"] = [s["Score"] for s in sentiments]

    return {
        "preview": df.head(10).to_dict(orient="records"),
        "distribution": df["Sentiment"].value_counts().to_dict()
    }

