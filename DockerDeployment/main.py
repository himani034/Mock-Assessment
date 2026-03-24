# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/predict")
def predict_score(hours: float):
    """Predict final score based on hours studied (dummy formula)"""
    return {"predicted_score": hours * 10}