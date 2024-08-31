import pickle
import pandas as pd

# Load the trained model
with open('diabetes_xgb.pkl', 'rb') as file:
    model = pickle.load(file)

# Load the data
data = pd.read_csv("patient_details.csv")
data.drop(columns=['Patient ID'], inplace=True)

# Select the last row of the DataFrame for prediction
new_data = data.iloc[-1, :].values.reshape(1, -1)

# Make a prediction using the loaded model
predictions = model.predict(new_data)
probabilities = model.predict_proba(new_data)

# Anomaly detection based on probability percentage
proba_diabetic = probabilities[0][1]  # Probability of being diabetic

if 0.8 <= proba_diabetic < 0.9:
    anomaly_status = "ALERT!Extreme chances of being diabetic."
elif proba_diabetic >= 0.9:
    anomaly_status = "Very high chances of being diabetic."
else:
    anomaly_status = "Moderate or low chances of being diabetic."

# Print the result
print(f"Predicted probability of being diabetic: {proba_diabetic:.2f}")
print(f"Anomaly detection status: {anomaly_status}")
