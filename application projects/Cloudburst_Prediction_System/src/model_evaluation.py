#src/model_evaluation.py
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "processed" / "ml_ready_weather_data.csv"
MODEL_FILE = BASE_DIR / "models" / "cloudburst_model.pkl"
df = pd.read_csv(DATA_FILE)
drop_cols = ["cloudburst_label"]
if "city" in df.columns:
    drop_cols.append("city")
X = df.drop(columns=drop_cols)
y = df["cloudburst_label"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
model = joblib.load(MODEL_FILE)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)
cm = confusion_matrix(y_test, y_pred)
print("Model Evaluation Results")
print("------------------------")
print(f"Accuracy : {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall   : {recall:.2f}")
print(f"F1-score : {f1:.2f}")
print("\nConfusion Matrix:")
print(cm)