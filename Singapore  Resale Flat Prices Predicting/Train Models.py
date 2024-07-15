import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import joblib

# Load the feature-engineered dataframe
df = pd.read_csv("C:\\Users\\aravi\\OneDrive\\Desktop\\Python Scripts\\Singapore  Resale Flat Prices Predicting\\feature_engineered_resale_flat_prices.csv")

# Define the target variable and features
X = df.drop(columns=['resale_price'])
y = df['resale_price']

# Impute missing values
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Function to evaluate model performance
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions, squared=False)
    r2 = r2_score(y_test, predictions)
    return mae, mse, rmse, r2

# Hyperparameter tuning for Linear Regression (note: Linear Regression has limited hyperparameters to tune)
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_mae, lr_mse, lr_rmse, lr_r2 = evaluate_model(lr_model, X_test, y_test)

print("Linear Regression Metrics:")
print(f"MAE: {lr_mae}")
print(f"MSE: {lr_mse}")
print(f"RMSE: {lr_rmse}")
print(f"R²: {lr_r2}")
print("\n")

# Save the Linear Regression model
joblib.dump(lr_model, 'linear_regression_model.pkl')

# Hyperparameter tuning for Decision Tree
dt_param_grid = {
    'max_depth': [None, 10, 20, 30, 40, 50],
    'min_samples_split': [2, 10, 20],
    'min_samples_leaf': [1, 10, 20]
}
dt_model = GridSearchCV(DecisionTreeRegressor(random_state=42), dt_param_grid, cv=5, scoring='neg_mean_squared_error')
dt_model.fit(X_train, y_train)
dt_best_model = dt_model.best_estimator_
dt_mae, dt_mse, dt_rmse, dt_r2 = evaluate_model(dt_best_model, X_test, y_test)

print("Decision Tree Best Parameters:", dt_model.best_params_)
print("Decision Tree Metrics:")
print(f"MAE: {dt_mae}")
print(f"MSE: {dt_mse}")
print(f"RMSE: {dt_rmse}")
print(f"R²: {dt_r2}")
print("\n")

# Save the Decision Tree model
joblib.dump(dt_best_model, 'decision_tree_model.pkl')

