from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# LOAD MODEL ON STARTUP
# -----------------------
MODEL_PATH = "tomato_leaf_baseline.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# -----------------------
# IMAGE PREPROCESSING
# -----------------------
def preprocess(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))
    arr = np.array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr

# -----------------------
# DECISION LOGIC
# -----------------------
def interpret(score):
    if score < 0.3:
        return "Diseased", round((1 - score) * 100, 2)
    elif score > 0.7:
        return "Healthy", round(score * 100, 2)
    else:
        confidence = 100 - abs(score - 0.5) * 200
        return "Uncertain", round(confidence, 2)

# -----------------------
# API ENDPOINT
# -----------------------
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    img = preprocess(image_bytes)

    score = float(model.predict(img)[0][0])
    status, confidence = interpret(score)

    return {
        "status": status,
        "confidence": confidence
    }
