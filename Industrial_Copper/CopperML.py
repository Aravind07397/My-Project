import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, PowerTransformer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report
import joblib

# Load dataset
file_path = "C:\\Users\\aravi\\OneDrive\\Desktop\\Python Scripts\\Industrial_Copper\\Copper_Set.xlsx"
df = pd.read_excel(file_path)

# Data Preprocessing
# Filter dataset for classification model
df_classification = df[df['status'].isin(['WON', 'LOST'])]

# Encode the Status column
df_classification['status'] = df_classification['status'].map({'WON': 1, 'LOST': 0})

# Separate features and target variables
X_regression = df.drop(columns=['selling_price', 'status'])
y_regression = df['selling_price']

X_classification = df_classification.drop(columns=['selling_price', 'status'])
y_classification = df_classification['status']

# Handle missing values (if any) by filling them with the mean of numeric columns
X_regression.fillna(X_regression.select_dtypes(include=np.number).mean(), inplace=True)
X_classification.fillna(X_classification.select_dtypes(include=np.number).mean(), inplace=True)

# Select only numeric columns for transformation
numeric_cols_regression = X_regression.select_dtypes(include=np.number).columns
numeric_cols_classification = X_classification.select_dtypes(include=np.number).columns

# Apply power transform to handle skewness
pt = PowerTransformer()
X_regression[numeric_cols_regression] = pt.fit_transform(X_regression[numeric_cols_regression])
X_classification[numeric_cols_classification] = pt.fit_transform(X_classification[numeric_cols_classification])

# Split the data into training and testing sets
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X_regression, y_regression, test_size=0.2, random_state=42)
X_train_cls, X_test_cls, y_train_cls, y_test_cls = train_test_split(X_classification, y_classification, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train_reg[numeric_cols_regression] = scaler.fit_transform(X_train_reg[numeric_cols_regression])
X_test_reg[numeric_cols_regression] = scaler.transform(X_test_reg[numeric_cols_regression])

X_train_cls[numeric_cols_classification] = scaler.fit_transform(X_train_cls[numeric_cols_classification])
X_test_cls[numeric_cols_classification] = scaler.transform(X_test_cls[numeric_cols_classification])

# Train the regression model
regressor = RandomForestRegressor(n_estimators=100, random_state=42)
regressor.fit(X_train_reg, y_train_reg)

# Train the classification model
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X_train_cls, y_train_cls)

# Save the models
joblib.dump(regressor, 'regressor_model.pkl')
joblib.dump(classifier, 'classifier_model.pkl')

# Load the models
regressor = joblib.load('regressor_model.pkl')
classifier = joblib.load('classifier_model.pkl')

# Define the Streamlit app
st.title("Copper Industry Sales and Leads Prediction")

# Predict Selling Price
st.header("Predict Selling Price")
with st.form("regression_form"):
    input_data_reg = {}
    for col in X_regression.columns:
        input_data_reg[col] = st.text_input(f"Enter value for {col}", value="0")
    
    submitted_reg = st.form_submit_button("Predict Selling Price")
    
    if submitted_reg:
        input_df_reg = pd.DataFrame([input_data_reg])
        # Convert input data to numeric
        input_df_reg[numeric_cols_regression] = input_df_reg[numeric_cols_regression].apply(pd.to_numeric)
        input_df_reg[numeric_cols_regression] = scaler.transform(pt.transform(input_df_reg[numeric_cols_regression]))
        selling_price_pred = regressor.predict(input_df_reg)
        st.write(f"Predicted Selling Price: {selling_price_pred[0]}")

# Predict Lead Status
st.header("Predict Lead Status")
with st.form("classification_form"):
    input_data_cls = {}
    for col in X_classification.columns:
        input_data_cls[col] = st.text_input(f"Enter value for {col}", value="0")
    
    submitted_cls = st.form_submit_button("Predict Status")
    
    if submitted_cls:
        input_df_cls = pd.DataFrame([input_data_cls])
        # Convert input data to numeric
        input_df_cls[numeric_cols_classification] = input_df_cls[numeric_cols_classification].apply(pd.to_numeric)
        input_df_cls[numeric_cols_classification] = scaler.transform(pt.transform(input_df_cls[numeric_cols_classification]))
        status_pred = classifier.predict(input_df_cls)
        status = 'WON' if status_pred[0] == 1 else 'LOST'
        st.write(f"Predicted Status: {status}")

# Evaluate the regression model
st.subheader("Regression Model Evaluation")
y_pred_reg = regressor.predict(X_test_reg)
mse = mean_squared_error(y_test_reg, y_pred_reg)
rmse = np.sqrt(mse)
st.write(f'RMSE: {rmse}')

# Evaluate the classification model
st.subheader("Classification Model Evaluation")
y_pred_cls = classifier.predict(X_test_cls)
accuracy = accuracy_score(y_test_cls, y_pred_cls)
st.write(f'Accuracy: {accuracy}')
st.write(classification_report(y_test_cls, y_pred_cls))

