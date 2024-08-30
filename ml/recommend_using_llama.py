import pickle
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama

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

# Define the LLM
llm = ChatOllama(
    model="llama3",
    temperature=0.2
)

# Define prompt templates for diabetic and non-diabetic advice
diabetic_prompt_template = """You are an AI specialising in medical domain.Give advice related to diet,exercies,routine etc. after analysing this characteristics

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
In the end , give some educational facts in a funny way related to health

Personalised Diabetes Management Advice:
"""

prevention_prompt_template = """You are an AI specialising in medical domain.Give advice related to diet,exercies,routine etc. after analysing this characteristics

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
In the end , give some educational facts in a funny way related to health

Personalised Diabetes Prevention Advice:
"""
# Select the appropriate prompt template based on the prediction
if prediction[0] == 1:
    selected_prompt_template = diabetic_prompt_template
else:
    selected_prompt_template = prevention_prompt_template

# Create the PromptTemplate with the selected template
DIABETES_ADVICE_PROMPT = PromptTemplate.from_template(selected_prompt_template)

# Get the last row's data as a dictionary for the prompt
row = data.iloc[-1]

# Format the prompt with patient-specific data
formatted_prompt = DIABETES_ADVICE_PROMPT.format(
    bmi=row["BMI"],
    age=row["Age"],
    preg=row["Pregnancies"],
    glu=row["Glucose"],
    bp=row["BloodPressure"],
    skin=row["SkinThickness"],
    insulin=row["Insulin"],
    func=row["DiabetesPedigreeFunction"],
)

# Get the LLM response by directly passing the formatted prompt
result = llm.invoke(formatted_prompt)

# Process the LLM response content
content = result.content

# Output the LLM advice
print(content)
