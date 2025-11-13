from fastapi import FastAPI # for creating the API
from pydantic import BaseModel # for defining the request body
import joblib # for loading the model and scaler
import numpy as np # for making predictions
import uvicorn # for running the API
import sys
from pathlib import Path

# Add project root to Python path so imports work with reload
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Load the saved model and scaler

bundle = joblib.load('src/models/rf.pk1') # load the model and scaler from the saved file
model = bundle['model'] # get the model from the bundle
scaler = bundle['scaler'] # get the scaler from the bundle
feature_names = bundle['features'] # get the features from the bundle

# Define the data structure FASTAPI EXPECTS

class Flowdata(BaseModel): # class is a blueprint for creating objects
    features: dict # dictionary of feature names and values

# Create the API and intializes fastapi app
app = FastAPI(title="AI Cybersecurity Intrusion Detection System", description="Classify network flows into benign or malicious categories. ")

# Define the endpoint
@app.post("/predict")
def predict(flow_data: Flowdata): # function is a block of code that can be called to perform a task
    # Convert the input data to a numpy array
    X = np.array([[flow_data.features.get(f, 0.0) for f in feature_names]])
    x_scaled = scaler.transform(X)

    # Predict class
    y_pred = model.predict(x_scaled)[0] # predict the class of the input data
    proba = model.predict_proba(x_scaled).max() # max probability of the predicted class

    # Return the prediction and probability
    return {
        "prediction": y_pred,
        "confidence": round(float(proba), 4)
    }

# Run with uvicorn locally
if __name__ == "__main__":
    uvicorn.run("src.serve:app", host="0.0.0.0", port=8000, reload=True) # run the API on the specified host and port and reload the server when changes are made to the code