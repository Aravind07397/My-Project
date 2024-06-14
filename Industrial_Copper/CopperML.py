import streamlit as st
import pandas as pd
import joblib

# Load your trained models and label encoders
reg_model = joblib.load('reg_model.pkl')
clf_model = joblib.load('clf_model.pkl')
label_encoders = joblib.load('label_encoders.pkl')

st.title("Selling Price and Status Prediction")

# Collect user inputs
quantity_tons = st.number_input("Quantity (tons)", min_value=0.0)
customer = st.number_input("Customer ID", min_value=0)
country = st.number_input("Country Code", min_value=0)
item_type = st.selectbox("Item Type", label_encoders['item type'].classes_)  
application = st.number_input("Application Code", min_value=0)
thickness = st.number_input("Thickness", min_value=0.0)
width = st.number_input("Width", min_value=0.0)
material_ref = st.selectbox("Material Reference", label_encoders['material_ref'].classes_)  
product_ref = st.number_input("Product Reference", min_value=0)
item_date = st.date_input("Item Date")
delivery_date = st.date_input("Delivery Date")

# Convert dates to numeric features
item_date_year = item_date.year
item_date_month = item_date.month
item_date_day = item_date.day
delivery_date_year = delivery_date.year
delivery_date_month = delivery_date.month
delivery_date_day = delivery_date.day

# Prepare the input data
input_data = pd.DataFrame({
    'quantity tons': [quantity_tons],
    'customer': [customer],
    'country': [country],
    'item type': [label_encoders['item type'].transform([item_type])[0]],
    'application': [application],
    'thickness': [thickness],
    'width': [width],
    'material_ref': [label_encoders['material_ref'].transform([material_ref])[0]],
    'product_ref': [product_ref],
    'item_date_year': [item_date_year],
    'item_date_month': [item_date_month],
    'item_date_day': [item_date_day],
    'delivery_date_year': [delivery_date_year],
    'delivery_date_month': [delivery_date_month],
    'delivery_date_day': [delivery_date_day]
})

# Predict Selling Price
predicted_price = reg_model.predict(input_data)
st.write(f"Predicted Selling Price: {predicted_price[0]}")

# Predict Status
predicted_status = clf_model.predict(input_data)
predicted_status_label = label_encoders['status'].inverse_transform(predicted_status)
st.write(f"Predicted Status: {predicted_status_label[0]}")
