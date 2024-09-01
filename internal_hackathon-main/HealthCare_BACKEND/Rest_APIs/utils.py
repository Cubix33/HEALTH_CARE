import pickle
import pandas as pd
import cv2
import numpy as np
import pytesseract
import re
import xgboost
from Data_user.models import DiabetesData
from rest_framework import serializers
from PIL import Image
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


# This is risky! 
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"  # Adjust the path accordingly


# def extract_patient_details_from_image(image):
#     def preprocess_image(image_path):
#         # Load the image using OpenCV
#         img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
#         # Resize the image to make the text more prominent
#         img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
#         # Apply Gaussian Blur to reduce noise
#         img = cv2.GaussianBlur(img, (5, 5), 0)
        
#         # Apply thresholding to binarize the image
#         _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
#         return img

#     def extract_patient_details(preprocessed_img):
#         # Set Tesseract configuration options
#         custom_config = r'--oem 3 --psm 6'
        
#         # Use Tesseract to extract text
#         text = pytesseract.image_to_string(preprocessed_img, config=custom_config)
        
#         # Print the extracted text for inspection
#         print("Extracted Text:", text)
        
#         # Define a regex pattern to extract required fields
#         patterns = {
#             'Patient_ID': r'Patient ID:\s*([A-Z0-9]+)',
#             'Pregnancies': r'Pregnancies:\s*([\d.]+)',
#             'Glucose': r'Glucose:\s*([\d.]+)',
#             'BloodPressure': r'BloodPressure:\s*([\d.]+)',
#             'SkinThickness': r'SkinThickness:\s*([\d.]+)',
#             'Insulin': r'Insulin:\s*([\d.]+)',
#             'BMI': r'BMI:\s*([\d.]+)',
#             'DiabetesPedigreeFunction': r'DiabetesPedigreeFunction:\s*([\d.]+)',
#             'Age': r'Age:\s*([\d.]+)',
#             #'Outcome': r'Outcome:\s*([\d.]+)'
#         }
        
#         # Extract the values based on regex patterns
#         extracted_data = {}
#         for field, pattern in patterns.items():
#             match = re.search(pattern, text)
#             extracted_data[field] = match.group(1) if match else None
        
#         return extracted_data
    

def extract_patient_details_from_image(image):
    def preprocess_image(image):
        # Convert the image file to an OpenCV image
        img = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
        
        # Resize, blur, and threshold as needed
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return img

    preprocessed_img = preprocess_image(image)
    
    # Tesseract configuration
    custom_config = r'--oem 3 --psm 6'
    
    # Extract text using Tesseract
    text = pytesseract.image_to_string(preprocessed_img, config=custom_config)
    
    # Debugging: Print the extracted text to inspect it
    print("Extracted Text:\n", text)
    
    # Define regex patterns to extract required fields
    patterns = {
        'patient_id': r'(?:Patient ID|PatientID|Patient Id|ID):?\s*([A-Za-z0-9]+)',  # More flexible matching
        'pregnancies': r'Pregnancies:\s*([\d.]+)',
        'glucose': r'Glucose:\s*([\d.]+)',
        'blood_pressure': r'(?:Blood Pressure|BloodPressure):\s*([\d.]+)',  # Flexible for Blood Pressure
        'skin_thickness': r'SkinThickness:\s*([\d.]+)',
        'insulin': r'Insulin:\s*([\d.]+)',
        'bmi': r'BMI:\s*([\d.]+)',
        'diabetes_pedigree_function': r'DiabetesPedigreeFunction:\s*([\d.]+)',
        'age': r'Age:\s*([\d.]+)',
    }
    
    # Extract the values based on regex patterns
    extracted_data = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)  # Case insensitive search
        if match:
            value = match.group(1)
            # Logging the match
            print(f"Matched {field}: {value}")
            if field in ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'age']:
                extracted_data[field] = float(value)
            elif field in ['bmi', 'diabetes_pedigree_function']:
                extracted_data[field] = float(value)
            else:
                extracted_data[field] = value
        else:
            print(f"No match for {field}")
            extracted_data[field] = None  # Set to None if no match is found
    
    # Ensure that patient_id is properly handled
    if not extracted_data.get('patient_id'):
        print("Error: Could not extract patient ID from the image.")
        raise serializers.ValidationError({"patient_id": "Could not extract patient ID from the image."})
    
    return extracted_data