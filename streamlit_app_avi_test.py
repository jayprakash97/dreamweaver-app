import streamlit as st
from PIL import Image
import streamlit as st
import requests
import json
import base64
import re
from io import BytesIO
from PIL import Image

# Set the page configuration with a wide layout for a book-like feel
st.set_page_config(page_title="Interactive Storybook", page_icon="📖", layout="wide")

def image_decode(image_data_decode):
    image_data = base64.b64decode(image_data_decode)
    return Image.open(BytesIO(image_data))

# Add custom CSS for the storybook theme
st.markdown("""
    <style>
    /* Overall background styling */
    body {
        background-color: #f5f0e1;
        font-family: 'Merriweather', serif;
        color: #4e342e;
    }

    /* Sidebar styling to resemble a table of contents */
    .css-1d391kg {
        background-color: #e8e0d2 !important;
        border-right: 2px solid #bfa989;
    }

    /* Sidebar Title */
    .css-1544g2n {
        color: #4e342e !important;
        font-size: 1.5em;
        font-family: 'Merriweather', serif;
        font-weight: bold;
    }

    /* Menu buttons in the sidebar */
    .css-1vbd788 {
        background-color: #d4c1a7;
        border-radius: 10px;
        border: 2px solid #bfa989;
        padding: 10px;
        font-size: 1.2em;
        color: #4e342e !important;
        margin-bottom: 15px;
    }

    .css-1vbd788:hover {
        background-color: #e0d3b8;
        color: #4e342e !important;
    }

    /* Main content area - text background with borders */
    .storybook-text {
        background-color: #faf3e7;
        padding: 30px;
        border-radius: 15px;
        border: 3px solid #bfa989;
        box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.1);
        font-family: 'Merriweather', serif;
        font-size: 18px;
        line-height: 1.6;
        text-align: justify;
    }

    /* Image styling */
    .storybook-image {
        border-radius: 15px;
        border: 3px solid #bfa989;
        box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.1);
        max-width: 100%;
        height: auto;
    }

    /* Styling for the page navigation buttons */
    .stButton > button {
        background-color: #d4c1a7;
        color: #4e342e;
        border: 2px solid #bfa989;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 1.2em;
    }

    .stButton > button:hover {
        background-color: #e0d3b8;
        color: #4e342e;
    }
    </style>
""", unsafe_allow_html=True)

with st.form("form_key"):
    # st.write("Craft personalized stories that bring adventure to life and ignite imagination and creativity")
    # gender = st.selectbox("Your Gender", options=["Male", "Female", "Don't want to share"])
    # main_character = st.text_input("What will be the name of the main character?", placeholder="Who will star in your story?")
    # audience = st.selectbox("Audience", options=["children", "young adult", "adult", "senior"])
    # story_setting = st.selectbox("Story Setthing", options=["Magical Kingdoms", "Underwater Kingdoms", "Pirate ships", "Exotic locations", "Imaginary world", "Digital words", "Others"])
    # story_type = st.selectbox("Story Type", options=["Fantacy", "Fairy Tales", "Mythology", "Bedtime stories", "Adventure", "Mystery", "Love", "Horror", ])
    # story_theme = st.text_input("What would be topic of the story?", placeholder="Leave brief idea of a story")
    # moral_lesson = st.text_input("What would be the moral of this story?", placeholder="Enter moral lesson from this story")
    # story_length = st.selectbox("Story Length (in words) ", options=["300", "400", "500"])
   
    submit_btn = st.form_submit_button("Submit")

AWS_API_URL = "https://uv56zhs3jc.execute-api.us-east-1.amazonaws.com/dev/ "
 
headers = {
    "Content-Type": "application/json"
}
 
# Create a button that triggers the POST request
if submit_btn:  # st.button("Submit"):
    payload = {
       "apiPath" : 'getStory',
       "storyPrompt" : ''
      }
    # Create the payload (data) to be sent in the POST request
    try:
        requests.get(AWS_API_URL, verify=False)
        json_data = payload
        response = requests.post(AWS_API_URL, headers=headers, json=json_data)
        if response.status_code == 200:
            data = response.json()  # Parse JSON response
            story_texts = data["story_texts"]
            captions = data["captions"]
            st.markdown(story_texts)
            st.markdown(captions)
            st.title("Children's Story")

            # Define the sidebar menu options
            st.sidebar.title("📚 Table of Contents")
            menu_options = ["About", "Storybook"]

            # Initialize session state to track the current page
            if 'current_page' not in st.session_state:
                st.session_state.current_page = "About"  # Default page

            # Sidebar buttons for navigation
            if st.sidebar.button("About"):
                st.session_state.current_page = "About"
            if st.sidebar.button("Storybook"):
                st.session_state.current_page = "Storybook"

            # Content for the 'About' section
            if st.session_state.current_page == "About":
                st.title("Welcome to the Storybook App")
                st.markdown("""
                    This interactive storybook app allows you to journey through a magical story, page by page, with beautiful illustrations accompanying the text.
                    
                    ### Features:
                    - **Interactive pages**: Each page presents a part of the story and a corresponding illustration.
                    - **Easy Navigation**: Use the menu on the left to explore different sections of the book.
                    
                    We hope this app brings the magic of storytelling to life!
                """)

            # Content for the 'Storybook' section
            elif st.session_state.current_page == "Storybook":
                # Define the pages of the story with corresponding images
                story_pages = [
                {
                    "text": "Once upon a time in a land far, far away, there was a magical forest. In the heart of the forest lived a young adventurer named Lily. She was known for her bravery and kindness. ",
                    "image": "img1.png",
                    "caption": "Lily begins her journey"
                },
                {
                    "text": "One morning, while walking through the forest, Lily came across a shimmering pond. As she gazed into the water, a magical creature appeared, offering her a quest.",
                    "image": "img2.png",
                    "caption": "A magical creature appears"
                },
                {
                    "text": "Lily accepted the quest and journeyed deeper into the forest, facing challenges and solving riddles. Eventually, she found a hidden treasure buried beneath an ancient oak tree.",
                    "image": "img3.png",
                    "caption": "Lily finds the hidden treasure"
                },
                {
                    "text": "With the treasure in hand, Lily returned to her village as a hero. The forest remained peaceful, and Lily continued her adventures, always ready to help those in need.",
                    "image": "img4.png",
                    "caption": "The peaceful forest"
                }
            ]

                # Initialize session state for the current story page index
                if 'page_index' not in st.session_state:
                    st.session_state.page_index = 0

                # Functions for navigating between pages
                def next_page():
                    if st.session_state.page_index < len(story_pages) - 1:
                        st.session_state.page_index += 1

                def prev_page():
                    if st.session_state.page_index > 0:
                        st.session_state.page_index -= 1

                # Get the current page's content
                current_page = story_pages[st.session_state.page_index]

                st.title("📖 My Storybook")
                image = Image.open(current_page["image"])
                # Create two columns: one for the story text, one for the image
                col1, col2 = st.columns(2)

                with col1:
                    #st.markdown(f'<div class="storybook-text">{current_page["text"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="storybook-text" style="height: {image.height}px;"><p>{current_page["text"]}</p></div>', unsafe_allow_html=True)
                with col2:
                    # Use custom HTML and CSS for image with the desired style
                    #st.markdown(f'<img src="{current_page["image"]}" alt="{current_page["caption"]}" class="storybook-image">', unsafe_allow_html=True)
                    st.image(image, caption=current_page["caption"], use_column_width=True)

                # Create Previous and Next buttons for navigation
                col1, col2, col3 = st.columns([1, 2, 1])

                with col1:
                    if st.session_state.page_index > 0:
                        st.button("Previous", on_click=prev_page)

                with col3:
                    if st.session_state.page_index < len(story_pages) - 1:
                        st.button("Next", on_click=next_page)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
