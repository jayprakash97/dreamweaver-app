import streamlit as st
import requests
import json
import base64 
import re
from io import BytesIO 
from PIL import Image

# Set the page configuration
st.set_page_config(page_title="Storybook", page_icon="📖", layout="wide")

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
    return Image.open(BytesIO(image_data))

def fetch_story_data(payload):
    # This function takes the payload ( useriput) and return story_text and captions
    AWS_API_URL = "https://wacnqhon34.execute-api.us-east-1.amazonaws.com/dev/"
    headers = {
        "Content-Type": "application/json"
    }
    
    # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.post(AWS_API_URL, headers=headers, json=payload, verify=False)
   
    if response.status_code == 200:
        data = response.json()
        return data["story_texts"], data["captions"]
    else:
        return [], []
 
 
def fetch_and_decode_images(captions):
    # This function takes caption of an story as an input and return encoded image data array
    AWS_API_URL = "https://wacnqhon34.execute-api.us-east-1.amazonaws.com/dev/"
    headers = {
        "Content-Type": "application/json"
    }
   
    decoded_images = []
    for caption in captions:
        payload2 = {
            "api_Path" : 'getImage',
            "storyPrompt" : caption
        }  
        json_data = payload2
        # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.post(AWS_API_URL, headers=headers, json=json_data, verify=False)
        if response.status_code == 200:
            data = response.json()
            decoded_images.append(data["image_data_decode1"])
    return decoded_images

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

# Create a button that triggers the POST request
try: 
    if submit_btn:  # st.button("Submit"):
        payload = {
           "audience" : audience,
           "story_type" : story_type,
           "main_character" : main_character,
           "story_theme" : story_theme, # 'Brushing the tooth',
           "moral_lesson" : moral_lesson,
           "setting" : story_setting, 
           "word_count" : story_length,
            "api_Path" : "getStory"
          }
        # Create the payload (data) to be sent in the POST request
     
        story_texts, captions = fetch_story_data(payload)
        decoded_images = fetch_and_decode_images(captions)

        image1 = image_decode(decoded_images[0])
        # st.image(image1, caption='Decoded Image', use_column_width=True)
                
        image2 = image_decode(decoded_images[1])
        # st.image(image2, caption='Decoded Image', use_column_width=True)
    
        image3 = image_decode(decoded_images[2])
        # st.image(image3, caption='Decoded Image', use_column_width=True)
                
        image4 = image_decode(decoded_images[3])
        # st.image(image4, caption='Decoded Image', use_column_width=True)
    
        image5 = image_decode(decoded_images[4])
  
        st.markdown("""
            <style>
                .storybook {
                            font-family: 'Courier New', Courier, monospace;
                            background-color: #f9f5ec;
                            padding: 50px;
                            border-radius: 10px;
                            box-shadow: 2px 2px 15px rgba(0, 0, 0, 0.1);
                            line-height: 1.6;
                        }
                        h1 {
                            color: #8B4513;
                        }
                        p {
                            font-size: 18px;
                            color: #5a4a3f;
                        }
                        .center {
                            display: block;
                            margin-left: auto;
                            margin-right: auto;
                            width: 50%;
                        }
                        .container {
                            display: flex;
                            justify-content: space-between;
                        }
            </style>
        """, unsafe_allow_html=True)
         
        # Title for the storybook
        st.title("📖 My Storybook")
    
        col1, col2, col3, col4, col5 = st.columns(5)
            
        with col1:
            st.markdown(f'<div class="storybook"><p>{story_texts[0]}</p></div>', unsafe_allow_html=True)
            st.image(image1, caption=captions[0], use_column_width=True)
        with col2:
            st.markdown(f'<div class="storybook"><p>{story_texts[1]}</p></div>', unsafe_allow_html=True)
            st.image(image2, caption=captions[1], use_column_width=True)
        with col3:
            st.markdown(f'<div class="storybook"><p>{story_texts[2]}</p></div>', unsafe_allow_html=True)
            st.image(image3, caption=captions[2], use_column_width=True)
        with col4:
            st.markdown(f'<div class="storybook"><p>{story_texts[3]}</p></div>', unsafe_allow_html=True)
            st.image(image4, caption=captions[3], use_column_width=True)
        with col5:
            st.markdown(f'<div class="storybook"><p>{story_texts[4]}</p></div>', unsafe_allow_html=True)
            st.image(image5, caption=captions[4], use_column_width=True)

    else:
        st.error(f"Failed with status code:  ")
        
except Exception as e:
    st.error(f"An error occurred: {str(e)}")

st.sidebar.success("Select a page above.")
st.sidebar.text("Made with 💕 by WonderScribe")
