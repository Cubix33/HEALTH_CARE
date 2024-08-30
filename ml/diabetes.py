import os
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import random
import string

# Define the path to the CSV file
csv_file = "diabetes.csv"

# Load the CSV data
df = pd.read_csv(csv_file)

# Define the output directory for images
output_dir = "images"
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Define class names based on Outcome values
class_dirs = {
    0: "Outcome_0",
    1: "Outcome_1"
}

# Create directories for each class
for class_name in class_dirs.values():
    os.makedirs(os.path.join(output_dir, class_name), exist_ok=True)

# Define a function to generate a random alphanumeric Patient ID
def generate_patient_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Define a function to create an image for each row in the dataframe
def create_image_for_row(row_data, row_index):
    # Create a blank white image
    img = Image.new('RGB', (800, 400), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    # Define the font and font size
    try:
        font = ImageFont.truetype("arial.ttf", 20)
        font_bold = ImageFont.truetype("arialbd.ttf", 24)
    except IOError:
        font = ImageFont.load_default()
        font_bold = font
    
    # Generate a random Patient ID
    patient_id = generate_patient_id()
    
    # Prepare the text to be drawn, excluding the 'Outcome' column
    text = f"Patient Details - Row {row_index + 1}\n"
    text += f"Patient ID: {patient_id}\n\n"
    text += "\n".join([f"{col}: {row_data[col]}" for col in df.columns if col != "Outcome"])
    
    # Define title and draw it in bold
    title = "Patient Medical Report"
    d.text((10, 10), title, font=font_bold, fill=(0, 0, 0))
    
    # Add text to the image
    d.text((10, 60), text, font=font, fill=(0, 0, 0))
    
    # Draw a border around the image
    border_color = (0, 0, 0)
    d.rectangle([(5, 5), (795, 395)], outline=border_color, width=5)
    
    # Determine the class directory based on the Outcome value
    outcome_value = row_data['Outcome']
    class_dir = os.path.join(output_dir, class_dirs[outcome_value])
    
    # Save the image with a unique name in the appropriate class folder
    image_filename = os.path.join(class_dir, f"patient_details_row_{row_index + 1}.png")
    img.save(image_filename)
    
    return image_filename

# Generate images for all rows in the dataframe and save them in the appropriate class folders
generated_images = []
for index, row in df.iterrows():
    image_file = create_image_for_row(row, index)
    generated_images.append(image_file)

# Display the names of the first 5 generated images
print(generated_images[:5])
