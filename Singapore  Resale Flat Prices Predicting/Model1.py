import streamlit as st
import joblib
import numpy as np

# Load the model
dt_model = joblib.load('decision_tree_model.pkl')

# Function to make predictions
def predict_price(town, flat_type, storey_range, floor_area_sqm, flat_model, lease_commence_date, age):
    features = np.array([[town, flat_type, storey_range, floor_area_sqm, flat_model, lease_commence_date, age]])
    prediction = dt_model.predict(features)
    return prediction[0]

# Streamlit app
st.title("Singapore Resale Flat Prices Predicting")
st.markdown("<i>Predict the resale price of flats in Singapore</i>", unsafe_allow_html=True)

# Input fields
town = st.text_input("Town")
flat_type = st.text_input("Flat Type")
storey_range = st.text_input("Storey Range")
floor_area_sqm = st.number_input("Floor Area (sqm)")
flat_model = st.text_input("Flat Model")
lease_commence_date = st.number_input("Lease Commence Date")
age = st.number_input("Age")

if st.button("Predict"):
    price = predict_price(town, flat_type, storey_range, floor_area_sqm, flat_model, lease_commence_date, age)
    st.write(f"Predicted Resale Price: ${price:,.2f}")
