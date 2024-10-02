import streamlit as st
import requests
import json
import base64 
import re
from io import BytesIO 
from PIL import Image

# pip install googletrans
from googletrans import Translator





# st.set_page_config(page_title="Multiple App", page_icon="👌")
# st.write(print(st.__version__))
col1, col2  = st.columns(2, vertical_alignment="center")
# col1, col2 = st.columns(2, horizontal_alignment="left")
with col1:
    st.image("pages/WS_Logo.png", width=200)
with col2:
    st.write("")
   
# Streamlit app title
# st.title("Welcome to WonderScribe Page", font_size="20px")
st.title("Welcome to WonderScribe Page")
 
# # Create input fields to collect data for the POST request body
# name = st.text_input("Enter your name")
# age = st.number_input("Enter your age", min_value=0)

def image_decode(image_data_decode):
    image_data = base64.b64decode(image_data_decode)
    return image.open(BytesIO(image_data))



with st.form("form_key"):
    st.write("Craft personalized stories that bring adventure to life and ignite imagination and creativity")
    gender = st.selectbox("Your Gender", options=["Male", "Female", "Don't want to share"])
    main_character = st.text_input("What will be the name of the main character?", placeholder="Who will star in your story?")
    audience = st.selectbox("Audience", options=["children", "young adult", "adult", "senior"])
    story_setting = st.selectbox("Story Setthing", options=["Magical Kingdoms", "Underwater Kingdoms", "Pirate ships", "Exotic locations", "Imaginary world", "Digital words", "Others"])
    story_type = st.selectbox("Story Type", options=["Fantacy", "Fairy Tales", "Mythology", "Bedtime stories", "Adventure", "Mystery", "Love", "Horror", ])
    story_theme = st.text_input("What would be topic of the story?", placeholder="Leave brief idea of a story")
    moral_lesson = st.text_input("What would be the moral of this story?", placeholder="Enter moral lesson from this story")
    story_length = st.selectbox("Story Length (in words) ", options=["300", "400", "500"])
    
    submit_btn = st.form_submit_button("Submit")

# st.write(f"""Your story summary:\n
# Audience: {audience} \n
# Main Character: {main_character} \n
# Story Setting: {story_setting} \n
# Story Type: {story_type} \n
# Story Theme: {story_theme} \n
# Moral Lesson: {moral_lesson} \n
# Story Size (in words) : {story_length}
# """)

# story_theme_value = st.text_input( value=story_theme)

# AWS API URL for POST request
AWS_API_URL = "https://wacnqhon34.execute-api.us-east-1.amazonaws.com/dev/"
 
# Optional: Set up headers (if using an API key or authentication)
headers = {
 #   "x-api-key": "your-api-key",  # Remove if your API doesn't require a key
    "Content-Type": "application/json",  # Specify the content type for the POST request
}
 
# Create a button that triggers the POST request
if submit_btn:  # st.button("Submit"):
    payload = {
       "story_type" : story_type,
       "main_character" : main_character,
       "story_theme" : story_theme, # 'Brushing the tooth',
       "moral_lesson" : moral_lesson,
       "setting" : story_setting, 
       "word_count" : story_length
      }
    # Create the payload (data) to be sent in the POST request

      
    try:
        json_data = payload
        # Make a POST request to the AWS API
        response = requests.post(AWS_API_URL, headers=headers, json=json_data)
    
        # Check if the request was successful (status code 200-299)
        if response.status_code == 200:
            data = response.json()  # Parse JSON response
            st.success("POST request successful!")
     
            # Extract the body content, which is a JSON string itself
            body_content = json.loads(data["body"])
            #st.write("Response from API:", body_content)
            # Extract the story text
            story_text = body_content["text"]
            st.title("Children's Story")
            st.write(story_text)

            translator = Translator()
            english_tax_term = story_text
            target_language = "french"  # Replace with your desired target language

            translated_tax_term = translator.translate(english_tax_term, dest=target_language).text
            st.write(translated_tax_term)
         
            # Base64 encoded image string
            # image1 = image_decode(body_content["image_data_decode"])
            # st.image(image1, caption='Decoded Image', use_column_width=True)
             
            # Alternatively, you can directly pass the binary image data
            # st.image(BytesIO(image_data), caption='Decoded Image', use_column_width=True)

            # image2 = image_decode(body_content["image_data_decode2"])
            # st.image(image2, caption='Decoded Image', use_column_width=True)

            # image3 = image_decode(body_content["image_data_decode3"])
            # st.image(image3, caption='Decoded Image', use_column_width=True)

            # image4 = image_decode(body_content["image_data_decode4"])
            # st.image(image4, caption='Decoded Image', use_column_width=True)

            # image1 = image_decode(body_content["image_data_decode"])
            # st.image(image1, caption='Decoded Image', use_column_width=True)
           
            base64_string = body_content["image_data_decode"]
            image_data = base64.b64decode(base64_string)
            image = Image.open(BytesIO(image_data))
            st.image(image, caption='Decoded Image', use_column_width=True)
        else:
            st.error(f"Failed with status code: {response.status_code}")
            st.write(response.text)  # Display the error message from API
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

st.sidebar.success("Select a page above.")
st.sidebar.text("Made with 💕 by WonderScribe")




