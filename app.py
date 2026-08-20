# Build the Streamlit App
import streamlit as st
import pandas as pd
import joblib

# LOAD THE CORRECT FILE WE SAVED FROM THE TEMP FOLDER
model = joblib.load('flood_risk_model.joblib')

st.title("🌊 Flood Risk Detector")
st.markdown("**Capstone Project by Adedapo Ibrahim Bayo**")
st.write("Enter the environmental parameters below to classify the community's flood vulnerability.")

with st.form("prediction_form"):
    st.header("Environmental Inputs")
    col1, col2 = st.columns(2)
    
    with col1:
        state = st.selectbox("Target State", ['Kogi', 'Bayelsa', 'Jigawa', 'Lagos', 'Anambra', 'Niger', 'Benue', 'Rivers', 'Kwara', 'Delta'])
        avg_rainfall_mm = st.number_input("Average Monthly Rainfall (mm)", min_value=0.0, value=150.0)
        elevation_m = st.number_input("Elevation above sea level (m)", min_value=0.0, value=45.0)
        drainage_quality = st.selectbox("Drainage Infrastructure", ['Poor', 'Fair', 'Good'])
        
    with col2:
        river_level_m = st.number_input("River Water Level (m)", min_value=0.0, value=5.5)
        distance_to_river_km = st.number_input("Distance to Nearest River (km)", min_value=0.0, value=2.0)
        soil_type = st.selectbox("Predominant Soil Type", ['Clay', 'Sandy', 'Loamy'])
        past_flood_events = st.number_input("Flood Events in Last 5 Years", min_value=0, max_value=10, value=0)
        
    submitted = st.form_submit_button("Classify Risk")

if submitted:
    input_data = pd.DataFrame({
        'state': [state],
        'avg_rainfall_mm': [avg_rainfall_mm],
        'river_level_m': [river_level_m],
        'elevation_m': [elevation_m],
        'distance_to_river_km': [distance_to_river_km],
        'drainage_quality': [drainage_quality],
        'soil_type': [soil_type],
        'past_flood_events': [past_flood_events]
    })
    
    # Calculate engineered feature
    # Calculate the mathematical logic once
    calculated_vuln = ((input_data['avg_rainfall_mm'] * (1 / (input_data['distance_to_river_km'] + 0.1))) / (input_data['elevation_m'] + 1.0))
    
    # Assign it to BOTH column names so the model is guaranteed to find what it needs
    input_data['hydro_topographic_vuln'] = calculated_vuln
    input_data['risk_proximity_index'] = calculated_vuln
    # Run prediction
    prediction = model.predict(input_data)[0]
    
    st.markdown("---")
    st.subheader("Classification Result:")
    
    if prediction == 'High':
        st.error(f"🚨 **HIGH RISK**: Severe flood vulnerability detected for this profile in {state} State.")
    elif prediction == 'Medium':
        st.warning(f"⚠️ **MEDIUM RISK**: Moderate flood vulnerability detected for this profile in {state} State.")
    else:
        st.success(f"✅ **LOW RISK**: Minimal flood vulnerability detected for this profile in {state} State.")