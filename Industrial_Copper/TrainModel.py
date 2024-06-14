import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report
import joblib

# Load the Excel file
file_path = 'C:\\Users\\aravi\\OneDrive\\Desktop\\Python Scripts\\Industrial_Copper\\Copperdata.xlsx'  
df1 = pd.read_excel(file_path)

# Encoding categorical columns: 'status', 'item type', 'material_ref'
label_encoders = {}
for column in ['status', 'item type', 'material_ref']:
    le = LabelEncoder()
    df1[column] = le.fit_transform(df1[column])
    label_encoders[column] = le

# Splitting the data into features and target variables
X = df1.drop(columns=['selling_price', 'status'])
y_regression = df1['selling_price']  # Target for regression
y_classification = df1['status']     # Target for classification

# Splitting the data into training and testing sets
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X, y_regression, test_size=0.2, random_state=42)
X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(X, y_classification, test_size=0.2, random_state=42)

# Extracting year, month, and day from 'item_date' and 'delivery date'
for date_col in ['item_date', 'delivery date']:
    X_train_reg[date_col + '_year'] = X_train_reg[date_col].dt.year
    X_train_reg[date_col + '_month'] = X_train_reg[date_col].dt.month
    X_train_reg[date_col + '_day'] = X_train_reg[date_col].dt.day
    X_test_reg[date_col + '_year'] = X_test_reg[date_col].dt.year
    X_test_reg[date_col + '_month'] = X_test_reg[date_col].dt.month
    X_test_reg[date_col + '_day'] = X_test_reg[date_col].dt.day

    X_train_clf[date_col + '_year'] = X_train_clf[date_col].dt.year
    X_train_clf[date_col + '_month'] = X_train_clf[date_col].dt.month
    X_train_clf[date_col + '_day'] = X_train_clf[date_col].dt.day
    X_test_clf[date_col + '_year'] = X_test_clf[date_col].dt.year
    X_test_clf[date_col + '_month'] = X_test_clf[date_col].dt.month
    X_test_clf[date_col + '_day'] = X_test_clf[date_col].dt.day

# Dropping the original datetime columns
X_train_reg.drop(columns=['item_date', 'delivery date'], inplace=True)
X_test_reg.drop(columns=['item_date', 'delivery date'], inplace=True)
X_train_clf.drop(columns=['item_date', 'delivery date'], inplace=True)
X_test_clf.drop(columns=['item_date', 'delivery date'], inplace=True)

# Train the Linear Regression model
reg_model = LinearRegression()
reg_model.fit(X_train_reg, y_train_reg)

# Train the Logistic Regression model
clf_model = LogisticRegression(max_iter=1000)
clf_model.fit(X_train_clf, y_train_clf)

# Save the models and label encoders
joblib.dump(reg_model, 'reg_model.pkl')
joblib.dump(clf_model, 'clf_model.pkl')
joblib.dump(label_encoders, 'label_encoders.pkl')

print("Models and label encoders have been saved.")
