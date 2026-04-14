from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: float

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/predict")
def predict(data: InputData):
    # Dummy model: sum of inputs
    prediction = data.feature1 + data.feature2 + data.feature3 + data.feature4
    return {"prediction": prediction}