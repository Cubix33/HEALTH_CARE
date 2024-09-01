# utils2.py
import pickle
import google.generativeai as genai
from google.generativeai.types import SafetySettingDict

# Load the machine learning model (can be done once when the module is loaded)
import os
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, '..', 'Rest_APIs', 'diabetes_xgb.pkl')
with open(file_path, 'rb') as file:
    model = pickle.load(file)

# Configure Google Generative AI
genai.configure(api_key="AIzaSyCOll-1nURu72Fv-XMKNx0txTb7J77y5cE")

# Set safety settings for the AI model
safety_settings = [
    SafetySettingDict(category="HARM_CATEGORY_DANGEROUS", threshold="BLOCK_NONE"),
    SafetySettingDict(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
    SafetySettingDict(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
    SafetySettingDict(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
    SafetySettingDict(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
]

def generate_recommendation(validated_data):
    """
    Generate a personalized recommendation based on patient data and calculate the probability of being diabetic.
    """
    # Prepare the input for the model
    input_data = [
        validated_data['pregnancies'],
        validated_data['glucose'],
        validated_data['blood_pressure'],
        validated_data['skin_thickness'],
        validated_data['insulin'],
        validated_data['bmi'],
        validated_data['diabetes_pedigree_function'],
        validated_data['age']
    ]

    # Reshape the input data for prediction
    input_data_reshaped = [input_data]

    # Predict the outcome and probabilities
    outcome_prediction = model.predict(input_data_reshaped)
    probabilities = model.predict_proba(input_data_reshaped)
    proba_diabetic = probabilities[0][1]

    # Determine anomaly status based on probability
    if 0.8 <= proba_diabetic < 0.9:
        anomaly_status = "ALERT! Extreme chances of being diabetic."
    elif proba_diabetic >= 0.9:
        anomaly_status = "Very high chances of being diabetic."
    else:
        anomaly_status = "Moderate or low chances of being diabetic."

    # Choose the appropriate prompt template
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
    
    selected_prompt_template = diabetic_prompt_template if outcome_prediction[0] == 1 else prevention_prompt_template

    # Format the prompt with the patient's data
    formatted_prompt = selected_prompt_template.format(
        bmi=validated_data['bmi'],
        age=validated_data['age'],
        preg=validated_data['pregnancies'],
        glu=validated_data['glucose'],
        bp=validated_data['blood_pressure'],
        skin=validated_data['skin_thickness'],
        insulin=validated_data['insulin'],
        func=validated_data['diabetes_pedigree_function'],
    )

    # Generate the recommendation
    response = genai.GenerativeModel('gemini-pro').generate_content(
        formatted_prompt,
        safety_settings=safety_settings,
        generation_config=genai.types.GenerationConfig(
            temperature=0.2,
            top_p=1,
            top_k=1,
            max_output_tokens=2048,
        )
    )
    
    text=beautify_response_text(response.text)
    # Return the recommendation text, outcome, and anomaly status
    return text, outcome_prediction[0], anomaly_status, proba_diabetic

def beautify_response_text(text):
    # Fix any misformatted bold markers
    text = text.replace("*  -", ":\n  -")  # Fix misformatted bullets with bold
    text = text.replace("*", "")           # Remove leftover asterisks

    # Add additional spacing for better readability
    text = text.replace(":\n", ":\n\n")
    text = text.replace("\n\n\n", "\n\n")  # Remove excessive line breaks

    # Add line breaks after section titles and lists
    text = text.replace("Diet:", "\nDiet:\n" + "-"*50)
    text = text.replace("Exercises:", "\nExercises:\n" + "-"*50)
    text = text.replace("Routine:", "\nRoutine:\n" + "-"*50)
    text = text.replace("Educational Facts in a Funny Way:", "\nEducational Facts in a Funny Way:\n" + "-"*50)
    
    return text.strip()  # Remove any leading or trailing whitespace

# Example usage with the provided response text
response_text = """
\n\nDiet:\n\n--------------------------------------------------\n\n\n\n  - **Focus on whole, unprocessed foods:*  - Fruits, vegetables, lean protein, and whole grains.\n\n  - **Limit processed foods, sugary drinks, and unhealthy fats:*  - These contribute to weight gain and inflammation.\n\n  - **Choose lean protein sources:*  - Chicken, fish, beans, and tofu.\n\n  - **Incorporate fiber-rich foods:*  - Oatmeal, brown rice, and leafy greens help regulate blood sugar levels.\n\n  - **Example meal plan:**\n\n      - Breakfast: Oatmeal with berries and nuts\n\n      - Lunch: Grilled chicken salad with mixed greens and vegetables\n\n      - Dinner: Salmon with roasted vegetables and brown rice\n\n\n\n\n\nExercises:\n\n--------------------------------------------------\n\n\n\n  - **Aim for at least 150 minutes of moderate-intensity exercise per week:*  - Brisk walking, cycling, or swimming.\n\n  - **Incorporate resistance training:*  - Weightlifting or bodyweight exercises to build muscle mass.\n\n  - **Choose activities you enjoy:*  - This will make it more likely that you'll stick to your routine.\n\n  - **Example exercises:**\n\n      - Walking for 30 minutes, 5 days a week\n\n      - Resistance training with dumbbells or resistance bands, 2-3 days a week\n\n\n\n\n\nRoutine:\n\n--------------------------------------------------\n\n\n\n  - **Establish a regular sleep schedule:*  - Aim for 7-9 hours of quality sleep each night.\n\n  - **Manage stress:*  - Engage in stress-reducing activities like yoga, meditation, or spending time in nature.\n\n  - **Monitor blood sugar levels regularly:*  - This will help you track your progress and make adjustments as needed.\n\n  - **Consider consulting with a registered dietitian or certified diabetes care and education specialist:*  - They can provide personalized guidance and support.\n\n\n\n**Educational Facts in a Funny Way:**\n\n\n\n  - **Why do we get goosebumps when we're cold?*  - It's our body's way of trying to warm us up by making our hair stand on end, trapping a layer of air next to our skin.\n\n  - **Why do we yawn?*  - It's not just because we're tired. Yawning helps regulate our body temperature and oxygen levels.\n\n  - **Why do our eyes change color?*  - The color of our eyes is determined by the amount of melanin in the iris. Melanin is a pigment that also gives our skin its color.
"""

# Clean and beautify the text
formatted_text = beautify_response_text(response_text)

# Display the result
print(formatted_text)