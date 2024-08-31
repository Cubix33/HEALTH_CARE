import pickle
import pandas as pd
import shap

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

# Initialize SHAP explainer
explainer = shap.TreeExplainer(model)

# Calculate SHAP values for the new data
shap_values = explainer.shap_values(new_data)

# Generate SHAP explanation for the new data
shap_explanation = shap_values[0]

# Create a textual explanation
explanation_text = []

# Iterate over each feature and its SHAP value
for feature, shap_value in zip(data.columns, shap_explanation):
    if shap_value > 0:
        explanation_text.append(f"The patient's {feature} increased the likelihood of being diabetic.")
    elif shap_value < 0:
        explanation_text.append(f"The patient's {feature} decreased the likelihood of being diabetic.")
    else:
        explanation_text.append(f"The patient's {feature} had no effect on the likelihood of being diabetic.")

# Final decision explanation
if predictions[0] == 1:
    explanation_text.append("Overall, the model predicts that the patient is diabetic.")
else:
    explanation_text.append("Overall, the model predicts that the patient is healthy.")

# Print the explanation
for line in explanation_text:
    print(line)
