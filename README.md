 SmartCrop

AI-Based Crop Disease and Nutrient Deficiency Detection

Problem Statement

Agriculture plays a critical role in ensuring food security and supporting livelihoods, especially in developing regions. However, crop productivity is often reduced due to plant diseases and nutrient deficiencies that remain undetected until visible damage has already occurred. Early symptoms generally appear on leaves as color changes, spots, or texture variations, but accurate identification requires expert knowledge that is not easily accessible to most farmers.

Traditional disease detection methods rely on manual inspection by agricultural experts or laboratory testing. These approaches are time-consuming, costly, and impractical for farmers in remote or rural areas. As a result, farmers frequently depend on guesswork or informal advice, leading to incorrect treatment and excessive use of pesticides and fertilizers. This increases production costs and causes long-term environmental damage.

Proposed Solution

SmartCrop is an AI-based web application designed to assist farmers in identifying crop diseases and nutrient deficiencies at an early stage using leaf images captured through mobile devices. The system applies deep learning–based computer vision techniques to analyze images and provide fast, interpretable results along with confidence scores.

The solution is designed to be simple, efficient, and accessible, even in low-connectivity environments.

System Architecture

The system follows a modular architecture:

User Interface → Flask Backend → FastAPI ML Service → Prediction Output

The Flask backend manages routing, sessions, and image uploads.

The FastAPI service handles machine learning inference.

The frontend provides a clean and intuitive user experience.

Technology Stack
Frontend

HTML

CSS

JavaScript

Backend

Flask (Python)

Machine Learning

MobileNetV2 (Convolutional Neural Network)

FastAPI (Inference API)

Project Structure
SmartCrop/
├── frontend/
│   ├── app.py
│   ├── templates/
│   │   ├── login.html
│   │   ├── upload.html
│   │   ├── analysis.html
│   │   └── history.html
│   ├── static/
│   └── requirements.txt
│
├── ml/
│   ├── inference.py
│   ├── model/
│   └── requirements.txt
│
├── README.md
└── .gitignore

How to Run the Project
Step 1: Start the ML Inference Server
cd ml
pip install -r requirements.txt
uvicorn inference:app --reload

Step 2: Start the Flask Backend
cd frontend
pip install -r requirements.txt
python app.py


Access the application at:

http://127.0.0.1:5000

Authentication

For hackathon demonstration purposes, authentication is implemented using a simple session-based login system.

Demo Credentials:

Email: admin@smartcrop.com
Password: smartcrop


Guest access is also available.

Dataset Information

Datasets are not included in this repository due to size constraints.
The model was trained using publicly available datasets such as:

PlantVillage dataset

Open-source nutrient deficiency datasets

Key Features

AI-based early disease detection

Confidence-based prediction output

Modular and scalable architecture

User-friendly interface

Fast and lightweight inference using MobileNetV2

Hackathon Note

This project was developed as part of a hackathon submission. The focus was on rapid prototyping, modular design, and real-world applicability rather than production-scale deployment.

Contributors

SmartCrop was developed by a student team focused on applying artificial intelligence to solve real-world agricultural problems.
