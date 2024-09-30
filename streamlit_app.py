import streamlit as st
import requests
import json
import base64 
from io import BytesIO 
from PIL import Image
st.logo("WS_Logo.png")
st.set_page_config(page_title="Multiple App", page_icon="👌",)

# Streamlit app title
st.title("Welcome to WonderScribe Page")
st.sidebar.success("Select a page above.")
 
# # Create input fields to collect data for the POST request body
# name = st.text_input("Enter your name")
# age = st.number_input("Enter your age", min_value=0)

with st.form("form_key"):
    st.write("Craft personalized stories that bring adventure to life and ignite imagination and creativity")
    gender = st.selectbox("Your Gender", options=["Male", "Female", "Don't want to share"])
    main_character = st.text_input("What will be the name of the main character?")
    audience = st.selectbox("Audience", options=["children", "young adult", "adult", "senior"])
    story_setting = st.selectbox("Story Setthing", options=["Magical Kingdoms", "Underwater Kingdoms", "Pirate ships", "Exotic locations", "Imaginary world", "Digital words", "Others"])
    story_type = st.selectbox("Story Type", options=["Fantacy", "Fairy Tales", "Mythology", "Bedtime stories", "Adventure", "Mystery", "Love", "Horror", ])
    story_theme = st.text_input("What would be topic of the story?", placeholder="Leave brief idea of a story")
    moral_lesson = st.text_input("What would be the moral of this story?")
    story_length = st.selectbox("Story Length (in words) ", options=["300", "400", "500"])
    
    submit_btn = st.form_submit_button("Submit")

st.write(f"""Your story summary:\n
Audience: {audience} \n
Main Character: {main_character} \n
Story Setting: {story_setting} \n
Story Type: {story_type} \n
Story Theme: {story_theme} \n
Moral Lesson: {moral_lesson} \n
Story Size (in words) : {story_length}
""")

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
 
    # payload = {
    #  "story_type" : {story_type},
    #  "main_character" : {main_character},
    #  "story_theme" : story_theme,
    #  "moral_lesson" : {moral_lesson},
    #  "setting" :  {story_setting}
    # }

      
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
         
            # Base64 encoded image string
            base64_string = body_content["image_data_decode"]
             
            # Decode the base64 string
            image_data = base64.b64decode(base64_string)
             
            # Convert the binary data into an image using PIL
            image = Image.open(BytesIO(image_data))
             
            # Display the image in Streamlit
            st.image(image, caption='Decoded Image', use_column_width=True)
             
            # Alternatively, you can directly pass the binary image data
            # st.image(BytesIO(image_data), caption='Decoded Image', use_column_width=True)

        else:
            st.error(f"Failed with status code: {response.status_code}")
            st.write(response.text)  # Display the error message from API
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

st.sidebar.text("Made with 💕 by WonderScribe")


