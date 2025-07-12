import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

# Load your DASS-21 dataset
df = pd.read_csv("D:\Projects\Mental Health AI\DASS.csv")

# Stress (Q1 to Q7)
stress_cols = [f"Q3_{i}_S{i}" for i in range(1, 8)]

# Anxiety (Q8 to Q14)
anx_cols = [f"Q3_{i}_A{i-7}" for i in range(8, 15)]  # A1 to A7

# Depression (Q15 to Q21)
depr_cols = [f"Q3_{i}_D{i-14}" for i in range(15, 22)]  # D1 to D7

all_cols = stress_cols + anx_cols + depr_cols

# Drop rows with missing values
df = df.dropna(subset=all_cols)

# Calculate total scores (each score out of 21, scaled to 42 like DASS-42)
df["Stress"]     = df[stress_cols].sum(axis=1) * 2
df["Anxiety"]    = df[anx_cols].sum(axis=1) * 2
df["Depression"] = df[depr_cols].sum(axis=1) * 2

# Define severity thresholds for each category (from official DASS guidelines)
def severity(score, scale):
    thresholds = {
        "Stress":     [14, 18, 25, 33],   # mild, mod, severe, ext severe
        "Anxiety":    [7,  10, 15, 20],
        "Depression": [9,  13, 20, 28]
    }
    t = thresholds[scale]
    if score <= t[0]: return "Normal"
    elif score <= t[1]: return "Mild"
    elif score <= t[2]: return "Moderate"
    elif score <= t[3]: return "Severe"
    else: return "Extremely Severe"

# Assign highest severity dimension as "Mood"
def get_mood(row):
    severities = {
        "Stress": severity(row["Stress"], "Stress"),
        "Anxiety": severity(row["Anxiety"], "Anxiety"),
        "Depression": severity(row["Depression"], "Depression")
    }
    # Choose the one with the highest severity
    order = ["Normal", "Mild", "Moderate", "Severe", "Extremely Severe"]
    return max(severities.items(), key=lambda x: order.index(x[1]))[0]

df["Mood"] = df.apply(get_mood, axis=1)

# Prepare data for model
X = df[all_cols]
y = df["Mood"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train a classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Predict & evaluate
y_pred = model.predict(X_test_scaled)
print(classification_report(y_test, y_pred))

import joblib

joblib.dump(model, "dass21_model.pkl")
joblib.dump(scaler, "scaler.pkl")
