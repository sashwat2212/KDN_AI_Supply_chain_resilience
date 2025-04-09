from fastapi import FastAPI
from news_scraper import scrape_and_classify_news
from fastapi import FastAPI, HTTPException
from weather import get_weather
from ai_recommendation import get_ai_recommendation
import pickle
import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI
import numpy as np
import onnxruntime as ort
from pydantic import BaseModel





# Load the trained model
with open("/Users/kdn_aisashwat/Desktop/supply_chain_resillience/notebooks/random_forest_model.pkl", "rb") as f:
    model = pickle.load(f)




# Load ONNX model
onnx_model_path = "/Users/kdn_aisashwat/Desktop/supply_chain_resillience/notebooks/lstm_model.onnx"
session = ort.InferenceSession(onnx_model_path)

# Initialize FastAPI app
app = FastAPI()

# Define input schema
class InputData(BaseModel):
    data: list  # Expecting a list of numerical values



# Define input data model
class InputData(BaseModel):
    days_for_shipment_scheduled: float
    order_day_of_week: int
    shipping_day_of_week: int
    


# Define min-max values for denormalization
scaling_info = {
    "Temperature_C": {"min": -19.96, "max": 40},
    "Humidity_pct": {"min": 30, "max": 90},
    "Precipitation_mm": {"min": 8.9, "max": 15},
    "Wind_Speed_kmh": {"min": 0.0000506, "max": 30}
}

feature_order = ["Temperature_C", "Humidity_pct", "Precipitation_mm", "Wind_Speed_kmh"]

def denormalize(predictions, feature_names, scaling_info):
    """ Convert normalized LSTM output back to real-world values. """
    return {
        feature: predictions[i] * (scaling_info[feature]["max"] - scaling_info[feature]["min"]) + scaling_info[feature]["min"]
        for i, feature in enumerate(feature_names)
    }

@app.post("/predict")
async def predict(data: dict):
    try:
        # Extract input features and ensure correct shape
        input_data = np.array(data["features"]).reshape(1, 1, 4).astype(np.float32)
        
        # Run inference
        ort_inputs = {session.get_inputs()[0].name: input_data}
        ort_outs = session.run(None, ort_inputs)
        
        # Extract raw predictions and denormalize
        normalized_predictions = ort_outs[0].tolist()[0]  # Extract first element from batch
        denormalized_predictions = denormalize(normalized_predictions, feature_order, scaling_info)
        
        return {"forecast": denormalized_predictions}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.post("/predict1/")
def predict(data: InputData):
    # Convert input data to DataFrame
    df = pd.DataFrame([data.dict()])
    
    # Make prediction
    prediction = model.predict(df)[0]
    
    return {"prediction": int(prediction)}
    


@app.get("/classified-news")
async def get_classified_news():
    """Fetches and classifies news articles in real-time."""
    articles = scrape_and_classify_news()
    return {"news": articles}


@app.get("/weather/{city}")
async def fetch_weather(city: str):
    weather_data = get_weather(city)
    if weather_data:
        return {"weather": weather_data}
    raise HTTPException(status_code=404, detail="Weather data not found")

@app.get("/ai-recommendation/{city}")
async def fetch_ai_recommendation(city: str):
    weather_data = get_weather(city)
    if not weather_data:
        raise HTTPException(status_code=404, detail="Weather data not found")
    
    recommendation = get_ai_recommendation(weather_data)
    return {"recommendation": recommendation}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




