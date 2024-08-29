import cv2
import numpy as np
import pytesseract
from PIL import Image
import pandas as pd
import re
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Change this to your tesseract installation path

def preprocess_image(image_path):
    # Load the image using OpenCV
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Resize the image to make the text more prominent
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # Apply Gaussian Blur to reduce noise
    img = cv2.GaussianBlur(img, (5, 5), 0)
    
    # Apply thresholding to binarize the image
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return img

def extract_patient_details(image_path):
    # Preprocess the image (as shown earlier)
    preprocessed_img = preprocess_image(image_path)
    
    # Set Tesseract configuration options
    custom_config = r'--oem 3 --psm 6'
    
    # Use Tesseract to extract text
    text = pytesseract.image_to_string(preprocessed_img, config=custom_config)
    
    # Print the extracted text for inspection
    print("Extracted Text:\n", text)
    
    # Define a regex pattern to extract required fields
    patterns = {
        'Patient ID': r'Patient ID:\s*([A-Z0-9]+)',
        'Pregnancies': r'Pregnancies:\s*([\d.]+)',
        'Glucose': r'Glucose:\s*([\d.]+)',
        'BloodPressure': r'BloodPressure:\s*([\d.]+)',
        'SkinThickness': r'SkinThickness:\s*([\d.]+)',
        'Insulin': r'Insulin:\s*([\d.]+)',
        'BMI': r'BMI:\s*([\d.]+)',
        'DiabetesPedigreeFunction': r'DiabetesPedigreeFunction:\s*([\d.]+)',
        'Age': r'Age:\s*([\d.]+)',
        #'Outcome': r'Outcome:\s*([\d.]+)'
    }
    
    # Extract the values based on regex patterns
    extracted_data = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, text)
        extracted_data[field] = match.group(1) if match else None
    
    return extracted_data


# Path to your image file
image_path = "H:\projects\internal hack\images\Outcome_1\patient_details_row_24.png"


# Extract details from the image
patient_details = extract_patient_details(image_path)

# Convert extracted data to a DataFrame
df = pd.DataFrame([patient_details])

# Save the DataFrame to a CSV file
csv_file_path = 'patient_details.csv'
df.to_csv(csv_file_path, index=False)

print(f"Patient details extracted and saved to {csv_file_path}")
