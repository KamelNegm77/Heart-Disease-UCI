import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import os

# Heart Disease UCI Dataset Features (excluding target 'num' and metadata)
HEART_DISEASE_FEATURES = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
    'restecg', 'thalch', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
]

@st.cache_resource
def load_model_auto():
    """Load the heart disease model automatically"""
    # First check current directory (for Streamlit Cloud)
    model_paths = sorted(Path('.').glob('final_model_*.joblib'))
    
    if not model_paths:
        # Fallback: Search in Downloads directory (for local testing)
        downloads_path = Path.home() / 'Downloads'
        if downloads_path.exists():
            model_paths = sorted(downloads_path.glob('final_model_*.joblib'))
    
    if not model_paths:
        st.warning('⚠️ No model found. Please ensure final_model_*.joblib exists.')
        return None, None

    model_path = model_paths[-1]  # load latest
    try:
        model = joblib.load(model_path)
        return model, str(model_path)
    except Exception as e:
        st.error(f'Failed to load model: {e}')
        return None, None


def main():
    st.title('❤️ Heart Disease Prediction')
    st.write('Enter patient details to predict the likelihood of heart disease.')
    
    load_mode = st.sidebar.radio('Model source', ['Auto-detect latest', 'Upload .joblib'], index=0)
    
    model = None
    model_label = ''
    
    if load_mode == 'Auto-detect latest':
        model, model_path = load_model_auto()
        if model is not None:
            model_label = f'✅ Loaded model: {os.path.basename(model_path)}'
        else:
            model_label = '❌ No final_model_*.joblib found. Please upload a model on the left.'
    else:
        uploaded = st.sidebar.file_uploader('Upload Heart Disease model (.joblib)', type=['joblib'])
        if uploaded is not None:
            try:
                model = joblib.load(uploaded)
                model_label = '✅ Loaded uploaded model file'
            except Exception as e:
                st.sidebar.error(f'Failed to load model: {e}')
    
    st.caption(model_label)
    
    # Feature inputs with descriptions
    st.subheader('Patient Information')
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input('Age', min_value=1, max_value=120, value=50, step=1)
        sex = st.selectbox('Sex', ['Male', 'Female'], format_func=lambda x: x)
        cp = st.selectbox('Chest Pain Type (cp)', 
                         ['Typical Angina', 'Atypical Angina', 'Non-anginal Pain', 'Asymptomatic'],
                         help='0: Typical, 1: Atypical, 2: Non-anginal, 3: Asymptomatic')
        trestbps = st.number_input('Resting Blood Pressure (trestbps)', min_value=0, max_value=300, value=120, step=1)
        chol = st.number_input('Serum Cholesterol (chol)', min_value=0, max_value=600, value=200, step=1)
        fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dl (fbs)', [0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')
        restecg = st.selectbox('Resting ECG (restecg)', 
                              ['Normal', 'ST-T Wave Abnormality', 'Left Ventricular Hypertrophy'],
                              help='0: Normal, 1: ST-T Wave Abnormality, 2: Left Ventricular Hypertrophy')
    
    with col2:
        thalch = st.number_input('Maximum Heart Rate Achieved (thalch)', min_value=0, max_value=250, value=150, step=1)
        exang = st.selectbox('Exercise Induced Angina (exang)', [0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')
        oldpeak = st.number_input('ST Depression (oldpeak)', min_value=0.0, max_value=10.0, value=0.0, step=0.1, format='%.1f')
        slope = st.selectbox('Slope of Peak Exercise ST Segment (slope)', 
                            ['Upsloping', 'Flat', 'Downsloping'],
                            help='0: Upsloping, 1: Flat, 2: Downsloping')
        ca = st.number_input('Number of Major Vessels (ca)', min_value=0, max_value=4, value=0, step=1)
        thal = st.selectbox('Thalassemia (thal)', 
                           ['Normal', 'Fixed Defect', 'Reversible Defect'],
                           help='1: Normal, 2: Fixed Defect, 3: Reversible Defect')
    
    # Convert categorical inputs to numeric
    sex_numeric = 1 if sex == 'Male' else 0
    cp_numeric = ['Typical Angina', 'Atypical Angina', 'Non-anginal Pain', 'Asymptomatic'].index(cp)
    restecg_numeric = ['Normal', 'ST-T Wave Abnormality', 'Left Ventricular Hypertrophy'].index(restecg)
    slope_numeric = ['Upsloping', 'Flat', 'Downsloping'].index(slope)
    thal_numeric = ['Normal', 'Fixed Defect', 'Reversible Defect'].index(thal) + 1  # 1, 2, or 3
    
    # Prepare feature dictionary
    feature_dict = {
        'age': age,
        'sex': sex_numeric,
        'cp': cp_numeric,
        'trestbps': trestbps,
        'chol': chol,
        'fbs': fbs,
        'restecg': restecg_numeric,
        'thalch': thalch,
        'exang': exang,
        'oldpeak': oldpeak,
        'slope': slope_numeric,
        'ca': ca,
        'thal': thal_numeric
    }
    
    if st.button('🔍 Predict Heart Disease', type='primary'):
        if model is None:
            st.error('❌ No model loaded. Please use Auto-detect or upload a .joblib model.')
            return
        
        try:
            # Create DataFrame with features in the correct order
            df = pd.DataFrame([feature_dict])
            
            # Make prediction
            prediction = model.predict(df)[0]
            prediction_proba = model.predict_proba(df)[0]
            
            # Display results
            if prediction == 0:
                st.success('✅ **No Heart Disease Detected**')
                st.info(f'Probability: {prediction_proba[0]*100:.2f}%')
            else:
                st.error('⚠️ **Heart Disease Detected**')
                st.warning(f'Probability: {prediction_proba[1]*100:.2f}%')
            
            # Show probability breakdown
            with st.expander('📊 Detailed Probabilities'):
                st.write(f'**No Heart Disease**: {prediction_proba[0]*100:.2f}%')
                st.write(f'**Heart Disease Present**: {prediction_proba[1]*100:.2f}%')
                
        except Exception as e:
            st.error(f'Prediction failed: {e}')
            with st.expander('🛠 Debug info'):
                st.write('**Input features:**', feature_dict)
                st.write('**Error details:**', str(e))
                st.write('**Model type:**', type(model).__name__)
    
    with st.expander('ℹ️ Feature Information'):
        st.markdown("""
        - **age**: Age in years
        - **sex**: 1 = Male, 0 = Female
        - **cp**: Chest pain type (0-3)
        - **trestbps**: Resting blood pressure (mm Hg)
        - **chol**: Serum cholesterol (mg/dl)
        - **fbs**: Fasting blood sugar > 120 mg/dl (1 = yes, 0 = no)
        - **restecg**: Resting ECG results (0-2)
        - **thalch**: Maximum heart rate achieved
        - **exang**: Exercise induced angina (1 = yes, 0 = no)
        - **oldpeak**: ST depression induced by exercise
        - **slope**: Slope of peak exercise ST segment (0-2)
        - **ca**: Number of major vessels colored by fluoroscopy (0-4)
        - **thal**: Thalassemia (1-3)
        """)
    
    # Optional: Debug info
    with st.expander("🛠 Debug info"):
        st.write("📂 Current directory:", os.getcwd())
        if model is not None:
            st.write("📄 Model type:", type(model).__name__)
            if hasattr(model, 'feature_names_in_'):
                st.write("📋 Expected features:", list(model.feature_names_in_))


if __name__ == '__main__':
    main()

