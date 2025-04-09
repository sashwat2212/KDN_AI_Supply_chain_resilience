from fastapi import FastAPI
import numpy as np
import onnxruntime as ort
from pydantic import BaseModel

# Load ONNX model
onnx_model_path = "lstm_model.onnx"
session = ort.InferenceSession(onnx_model_path)

# Initialize FastAPI app
app = FastAPI()

# Define input schema
class InputData(BaseModel):
    data: list  # Expecting a list of numerical values

@app.post("/predict")
async def predict(input_data: InputData):
    try:
        # Convert input data to NumPy array
        input_array = np.array(input_data.data, dtype=np.float32).reshape(1, -1, 1)  # Adjust shape based on model's expectation
        
        # Run inference
        input_name = session.get_inputs()[0].name
        prediction = session.run(None, {input_name: input_array})[0]

        return {"prediction": prediction.tolist()}
    
    except Exception as e:
        return {"error": str(e)}

# Run the server with: uvicorn server:app --host 0.0.0.0 --port 8000 --reload
