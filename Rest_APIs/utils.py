import pickle
import pandas as pd
import xgboost
from Data_user.models import DiabetesData
import os
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, '..', 'Rest_APIs', 'diabetes_xgb.pkl')
with open(file_path, 'rb') as file:
    model = pickle.load(file)

def ml_generate_outcome(diabetes_data):
    # Convert `diabetes_data` to a dictionary to create a DataFrame
    data_dict = {
        'Pregnancies': [diabetes_data.pregnancies],
        'Glucose': [diabetes_data.glucose],
        'BloodPressure': [diabetes_data.blood_pressure],
        'SkinThickness': [diabetes_data.skin_thickness],
        'Insulin': [diabetes_data.insulin],
        'BMI': [diabetes_data.bmi],
        'DiabetesPedigreeFunction': [diabetes_data.diabetes_pedigree_function],
        'Age': [diabetes_data.age]
    }

    # Create a DataFrame from the patient's data
    df = pd.DataFrame(data_dict)

    # Convert columns to appropriate numeric types (int or float)
    df['Pregnancies'] = pd.to_numeric(df['Pregnancies'], errors='coerce', downcast='integer')
    df['Glucose'] = pd.to_numeric(df['Glucose'], errors='coerce', downcast='integer')
    df['BloodPressure'] = pd.to_numeric(df['BloodPressure'], errors='coerce')
    df['SkinThickness'] = pd.to_numeric(df['SkinThickness'], errors='coerce', downcast='integer')
    df['Insulin'] = pd.to_numeric(df['Insulin'], errors='coerce')
    df['BMI'] = pd.to_numeric(df['BMI'], errors='coerce')
    df['DiabetesPedigreeFunction'] = pd.to_numeric(df['DiabetesPedigreeFunction'], errors='coerce')
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce', downcast='integer')

    # Fill NaN values with appropriate default values
    df.fillna(0, inplace=True)

    # Ensure the DataFrame is passed in the correct format to the model
    prediction = model.predict(df)

    # Return the prediction (1 for diabetic, 0 for non-diabetic)
    return prediction[0]
