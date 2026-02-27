import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

INPUT_FILE = "/Users/hardikbhagtani/corporate-risk-radar/financial_data_m1/Labeled_Data.csv"
MODEL_FOLDER = 'models'
MODEL_FILE = os.path.join(MODEL_FOLDER, "risk_model.pkl")

if not os.path.exists(MODEL_FOLDER):
    os.makedirs(MODEL_FOLDER)

print("Starting Model Training...")

try:
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} companies")
except FileNotFoundError:
    print(f"Error: Required file not found")
    exit()

features = ['Debt_to_Equity', 'Interest_Coverage', 'Current_Ratio', 'Net_Profit_Margin']
X = df[features]
y = df['Target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training on {len(X_train)} companies...")
print(f"Testing on {len(X_test)} companies...")

model = xgb.XGBClassifier(
    n_estimators = 100,
    learning_rate = 0.1,
    max_depth = 3,
    scale_pos_weight = 10,
    random_state = 42
)

model.fit(X_train,y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print()
print("Model Training Completed")
print(f"Accuracy : {accuracy *100:.2f}%")
print("\n Detailed Report:")
print(classification_report(y_test, y_pred, target_names=['Safe', 'Risky']))

joblib.dump(model, MODEL_FILE)
print("Model Saved")