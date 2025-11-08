# Heart Disease Prediction App

A Streamlit web application for predicting heart disease using machine learning.

## Model Information

- **Model**: Gradient Boosting Classifier
- **Model File**: `final_model_20250512_031519.joblib`
- **Accuracy**: 93.53%
- **Precision**: 93.65%
- **Recall**: 92.19%
- **F1-Score**: 92.91%
- **ROC-AUC**: 98.79%

## Features

The model uses 13 features from the UCI Heart Disease dataset:

1. **age** - Age in years
2. **sex** - 1 = Male, 0 = Female
3. **cp** - Chest pain type (0-3)
4. **trestbps** - Resting blood pressure (mm Hg)
5. **chol** - Serum cholesterol (mg/dl)
6. **fbs** - Fasting blood sugar > 120 mg/dl (1 = yes, 0 = no)
7. **restecg** - Resting ECG results (0-2)
8. **thalch** - Maximum heart rate achieved
9. **exang** - Exercise induced angina (1 = yes, 0 = no)
10. **oldpeak** - ST depression induced by exercise
11. **slope** - Slope of peak exercise ST segment (0-2)
12. **ca** - Number of major vessels colored by fluoroscopy (0-4)
13. **thal** - Thalassemia (1-3)

## Local Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run streamlit_app.py
```

## Deployment to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository
6. Set the main file path to: `streamlit_app.py`
7. Click "Deploy"

The app will automatically detect the model file (`final_model_20250512_031519.joblib`) in the repository.

## Usage

1. Enter patient information in the form
2. Click "Predict Heart Disease"
3. View the prediction result and probability scores

## Files

- `streamlit_app.py` - Main Streamlit application
- `final_model_20250512_031519.joblib` - Trained model file
- `requirements.txt` - Python dependencies
- `README.md` - This file

