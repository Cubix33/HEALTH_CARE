import pickle
import pandas as pd
import google.generativeai as genai
from google.generativeai.types import SafetySettingDict

# Load the trained model from the pickle file
with open('diabetes_xgb.pkl', 'rb') as file:
    model = pickle.load(file)

# Load the data from the CSV file
data = pd.read_csv("patient_details.csv")
data.drop(columns=['Patient ID'], inplace=True)

# Select the last row of the DataFrame and reshape it for prediction
last_row = data.iloc[-1, :].values.reshape(1, -1)

# Make a prediction using the loaded model
prediction = model.predict(last_row)

# Configure Gemini Pro
genai.configure(api_key="AIzaSyCOll-1nURu72Fv-XMKNx0txTb7J77y5cE")

# Set up the model
model = genai.GenerativeModel('gemini-pro')

# Define safety settings
safety_settings = [
    SafetySettingDict(category="HARM_CATEGORY_DANGEROUS", threshold="BLOCK_NONE"),
    SafetySettingDict(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
    SafetySettingDict(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
    SafetySettingDict(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
    SafetySettingDict(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
]

# Define prompt templates for diabetic and non-diabetic advice
diabetic_prompt_template = """You are an AI expert in medical domain. Give advice related to diet (with examples), exercises (with examples), routine etc. after analysing these characteristics:

Patient Characteristics:
- BMI: {bmi}
- Age: {age}
- Pregnancies: {preg}
- Glucose: {glu}
- Blood Pressure: {bp}
- Skin Thickness: {skin}
- Insulin: {insulin}
- Diabetes Pedigree Function: {func}

Don't use word I, instead use we.
In the end, give some educational facts in a funny way related to health.

Personalised Diabetes Management Advice:
"""

prevention_prompt_template = """You are an AI expert in medical domain. Give advice related to diet (with examples), exercises (with examples), routine etc. after analysing these characteristics:

Patient Characteristics:
- BMI: {bmi}
- Age: {age}
- Pregnancies: {preg}
- Glucose: {glu}
- Blood Pressure: {bp}
- Skin Thickness: {skin}
- Insulin: {insulin}
- Diabetes Pedigree Function: {func}

Don't mention these factors' values.
Don't use word I, instead use we.
In the end, give some educational facts in a funny way related to health and diabetes.

Personalised Diabetes Prevention Advice:
"""

# Select the appropriate prompt template based on the prediction
selected_prompt_template = diabetic_prompt_template if prediction[0] == 1 else prevention_prompt_template

# Get the last row's data
row = data.iloc[-1]

# Format the prompt with patient-specific data
formatted_prompt = selected_prompt_template.format(
    bmi=row["BMI"],
    age=row["Age"],
    preg=row["Pregnancies"],
    glu=row["Glucose"],
    bp=row["BloodPressure"],
    skin=row["SkinThickness"],
    insulin=row["Insulin"],
    func=row["DiabetesPedigreeFunction"],
)

# Generate content using Gemini Pro
response = model.generate_content(
    formatted_prompt,
    safety_settings=safety_settings,
    generation_config=genai.types.GenerationConfig(
        temperature=0.2,
        top_p=1,
        top_k=1,
        max_output_tokens=2048,
    )
)

# Output the generated advice
print(response.text)