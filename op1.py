import pandas as pd
import joblib

def predict_mood_with_explanation(input_scores):
    # Define column names
    stress_cols = [f"Q3_{i}_S{i}" for i in range(1, 8)]
    anx_cols    = [f"Q3_{i}_A{i-7}" for i in range(8, 15)]
    depr_cols   = [f"Q3_{i}_D{i-14}" for i in range(15, 22)]
    all_cols = stress_cols + anx_cols + depr_cols

    # Create a DataFrame for the input
    df_input = pd.DataFrame([input_scores], columns=all_cols)

    # Load model and scaler
    model = joblib.load("dass21_model.pkl")
    scaler = joblib.load("scaler.pkl")

    # Scale the input
    input_scaled = scaler.transform(df_input)

    # Predict mood
    predicted_mood = model.predict(input_scaled)[0]

    # Calculate total scores
    stress_score = df_input[stress_cols].sum(axis=1).iloc[0] * 2
    anxiety_score = df_input[anx_cols].sum(axis=1).iloc[0] * 2
    depression_score = df_input[depr_cols].sum(axis=1).iloc[0] * 2

    # Severity helper
    def get_severity(score, category):
        thresholds = {
            "Stress": [14, 18, 25, 33],
            "Anxiety": [7, 10, 15, 20],
            "Depression": [9, 13, 20, 28]
        }
        labels = ["Normal", "Mild", "Moderate", "Severe", "Extremely Severe"]
        t = thresholds[category]
        if score <= t[0]: return labels[0]
        elif score <= t[1]: return labels[1]
        elif score <= t[2]: return labels[2]
        elif score <= t[3]: return labels[3]
        else: return labels[4]

    explanation = f"""
Predicted Mood: {predicted_mood}

Here's why:
- Stress Score: {stress_score} → {get_severity(stress_score, "Stress")}
- Anxiety Score: {anxiety_score} → {get_severity(anxiety_score, "Anxiety")}
- Depression Score: {depression_score} → {get_severity(depression_score, "Depression")}

The model detected **{predicted_mood}** as the most significant concern based on severity scores.
    """

    return predicted_mood, explanation.strip()


if __name__ == "__main__":
    # Simulated frontend scores: [0-3] range * 21 items
    input_scores = [3, 2, 2, 3, 1, 2, 2,   # Stress (Q1–Q7)
                    2, 2, 1, 2, 2, 1, 1,   # Anxiety (Q8–Q14)
                    1, 2, 2, 2, 1, 1, 1]   # Depression (Q15–Q21)

    mood, explanation = predict_mood_with_explanation(input_scores)
    print(explanation)
