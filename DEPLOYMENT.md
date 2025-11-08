# Quick Deployment Guide

## Option 1: Deploy to Your Existing Heart-Disease-UCI Repository

1. **Navigate to the deployment folder:**
   ```bash
   cd "C:\Users\Lenovo\Downloads\Heart-Disease-Deployment"
   ```

2. **Initialize git (if not already):**
   ```bash
   git init
   ```

3. **Add all files:**
   ```bash
   git add .
   ```

4. **Commit:**
   ```bash
   git commit -m "Add Streamlit deployment app for heart disease prediction"
   ```

5. **Add your GitHub repository as remote:**
   ```bash
   git remote add origin https://github.com/KamelNegm77/Heart-Disease-UCI.git
   ```

6. **Push to GitHub:**
   ```bash
   git branch -M main
   git push -u origin main
   ```

## Option 2: Create New Repository

1. Create a new repository on GitHub (e.g., `Heart-Disease-Prediction-App`)
2. Follow steps 1-4 from Option 1
3. Use your new repository URL in step 5

## Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `KamelNegm77/Heart-Disease-UCI`
5. Set **Main file path**: `streamlit_app.py`
6. Click "Deploy"

The app will be live at: `https://your-app-name.streamlit.app`

## Files Included

✅ `streamlit_app.py` - Main application  
✅ `final_model_20250512_031519.joblib` - Trained model  
✅ `requirements.txt` - Dependencies  
✅ `README.md` - Documentation  
✅ `.gitignore` - Git ignore rules  

