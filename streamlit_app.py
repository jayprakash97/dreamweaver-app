import streamlit as st
from PIL import Image
import streamlit as st
import requests
import json
import base64
import re
from io import BytesIO
from PIL import Image
import requests
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# def get_aws_credentials():
#     # Create a Secrets Manager client
#     client = boto3.client("secretsmanager", region_name="us-east-1")
    
#     # Retrieve the secret
#     response = client.get_secret_value(SecretId="jaypeeidsecretcode")
#     # response = client.get_secret_value(SecretId=st.secrets["streamlit_s3_credentials"])
    
#     secret_dict = json.loads(response["SecretString"])
#     return secret_dict["AWS_ACCESS_KEY_ID"], secret_dict["AWS_SECRET_ACCESS_KEY"]
 
# # Use the retrieved credentials to access S3
# aws_access_key_id, aws_secret_access_key = get_aws_credentials()

def get_aws_credentials():
    secret_name = "jaypeeidsecretcode"
    # Your secret name
    region_name = "us-east-1"
    # Replace with your region
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name = 'secretsmanager', region_name = region_name)
    try:
        # Retrieve the secret value
        response = client.get_secret_value(SecretId = secret_name)
        # Decrypts secret using the associated KMS CMK
        secret = json.loads(response['SecretString'])
        # Extract AWS credentials
        aws_access_key_id = secret['AWS_ACCESS_KEY_ID']
        aws_secret_access_key = secret['AWS_SECRET_ACCESS_KEY']
        return aws_access_key_id, aws_secret_access_key
    except NoCredentialsError:
	    st.text("Credentials not available.")
	    raise
    except ClientError as e:
	    st.text(f"Error retrieving secret: {e}")
	    raise

aws_access_key_id, aws_secret_access_key = get_aws_credentials()

 
s3client = boto3.client(
    's3',
    aws_access_key_id="aws_access_key_id",
    aws_secret_access_key="aws_secret_access_key"
)
    # aws_access_key_id=aws_access_key_id,
    # aws_secret_access_key=aws_secret_access_key

def image_decode(image_data_decode):
        image_data = base64.b64decode(image_data_decode)
        return Image.open(BytesIO(image_data))
 
@st.cache_data 
def fetch_story_data(payload, _force_refresh=False):
    if _force_refresh:
        st.cache_data.clear()
    AWS_API_URL = "https://wacnqhon34.execute-api.us-east-1.amazonaws.com/dev/"
    headers = {
        "Content-Type": "application/json"
    }
    # payload1 = {
    #     "api_Path" : 'getStory',
    #     "storyPrompt" : ''
    # }
 
    json_data = payload
 
    response = requests.post(AWS_API_URL, headers=headers, json=json_data)
    if response.status_code == 200:
        data = response.json() 
        return data["story_texts"], data["captions"], data["storyfiles"]
    else:
        return [], [], []

@st.cache_data
def fetch_and_decode_images(captions, _force_refresh=False):
    if _force_refresh:
        st.cache_data.clear()
    AWS_API_URL = "https://wacnqhon34.execute-api.us-east-1.amazonaws.com/dev/"
    headers = {
        "Content-Type": "application/json"
    }
    decoded_images = []
    
    for index, caption in enumerate(captions):
        if index == 0:
            payload2 = {
                "api_Path" : 'getImage',
                "storyPrompt" : caption,
                "previousPrompt" : ''
            }
        else:
            payload2 = {
                "api_Path" : 'getImage',
                "storyPrompt" : caption,
                "previousPrompt" : captions[index - 1]
            }   
        json_data = payload2
        response = requests.post(AWS_API_URL, headers=headers, json=json_data)
        if response.status_code == 200:
            data = response.json()
            decoded_images.append(data["image_data_decode1"])
    return decoded_images
 
 
def main():
    if 'cache_cleared' not in st.session_state:
        st.session_state.cache_cleared = False
      
    # Set the page configuration with a wide layout for a book-like feel
    st.set_page_config(page_title="Interactive Storybook", page_icon="📖", layout="wide")
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
        st.write("Craft personalized stories that bring adventure to life and ignite imagination and creativity")
        gender = st.selectbox("Your Gender", options=["Male", "Female", "Don't want to share"])
        main_character = st.text_input("What will be the name of the main character?", placeholder="Who will star in your story?")
        audience = st.selectbox("Audience", options=["children", "young adult", "adult", "senior"])
        story_setting = st.selectbox("Story Setthing", options=["Magical Kingdoms", "Underwater Kingdoms", "Pirate ships", "Exotic locations", "Imaginary world", "Digital words", "Others"])
        story_type = st.selectbox("Story Type", options=["Fantacy", "Fairy Tales", "Mythology", "Bedtime stories", "Adventure", "Mystery", "Love", "Horror", ])
        story_theme = st.text_input("What would be topic of the story?", placeholder="Leave brief idea of a story")
        moral_lesson = st.text_input("What would be the moral of this story?", placeholder="Enter moral lesson from this story")
        story_length = st.selectbox("Story Length (in words) ", options=["300", "400", "500"])
        story_lang = st.selectbox("Story lang", options=["English", "Spanish", "French", "Mandarin","German", "Hindi","Vietnamese", "Tagalog", "Urdu", "Arabic"])
        
        submit_btn = st.form_submit_button("Submit")
 
    try:
        # st.title("Children's Story")
        if submit_btn:
           # Creating a session varibale to maintain the state
           st.session_state.submit_btn = True
         
        st.sidebar.title("📚 Table of Contents")
        menu_options = ["About", "Storybook"]

        # st.write( st.session_state )
        # st.write( st.session_state.submit_btn )
        
        st.session_state.current_page = "Storybook"
        # if 'current_page' not in st.session_state:
        #     st.session_state.current_page = "About"  # Default page
 
        # if st.sidebar.button("About"):
        #     st.session_state.current_page = "About"
        # if st.sidebar.button("Storybook"):
        #     st.session_state.current_page = "Storybook"


        if submit_btn:   # st.sidebar.button("Reset Cache"):
            st.cache_data.clear()
            st.session_state.cache_cleared = True
            st.success("Cache has been cleared! Refresh the page to fetch new data.")
            st.session_state.submit_btn = True
            st.session_state.page_index = 0
          


        # if st.session_state.current_page == "About":
        #     st.title("Welcome to the Storybook App")
        #     st.markdown("""
        #             This interactive storybook app allows you to journey through a magical story, page by page, with beautiful illustrations accompanying the text.
        #            """)

        
        # Content for the 'Storybook' section

        if st.session_state.submit_btn and st.session_state.current_page == "Storybook": 
            payload = {
                "audience" : audience,
                "story_type" : story_type,
                "main_character" : main_character,
                "story_theme" : story_theme, # 'Brushing the tooth',
                "moral_lesson" : moral_lesson,
                "setting" : story_setting, 
                "word_count" : story_length,
                 "story_lang" : story_lang,
                 "api_Path" : "getStory"
               }
     
            story_texts, captions, storyfiles = fetch_story_data(payload)
            decoded_images = fetch_and_decode_images(captions)
         
            audioStoryFiles = []
            for storyFile in storyfiles:
                output = s3client.generate_presigned_url('get_object',
                                                    Params={'Bucket': 'wonderstorytexttoaudiofile',
                                                            'Key': storyFile},
                                                    ExpiresIn=3600)
                audioStoryFiles.append(output)

         
            # Reset the cache_cleared flag. Don't clear the cache
            st.session_state.cache_cleared = False
         
            story_pages = [
                {
                    "text": story_texts[0],
                    #"image": "img1.png",
                    "image": decoded_images[0],
                    "caption": captions[0],
                    "audio": audioStoryFiles[0]
                },
                {
                    "text": story_texts[1],
                    #"image": "img2.png",
                    "image": decoded_images[1],
                    "caption": captions[1],
                    "audio": audioStoryFiles[1]
                },
                {
                    "text": story_texts[2],
                    #"image": "img3.png",
                    "image": decoded_images[2],
                    "caption": captions[2],
                    "audio": audioStoryFiles[2]
                },
                {
                    "text": story_texts[3],
                    #"image": "img4.png",
                    "image": decoded_images[3],
                    "caption": captions[3],
                    "audio": audioStoryFiles[3]
                },
                {
                    "text": story_texts[4],
                    #"image": "img4.png",
                    "image": decoded_images[4],
                    "caption": captions[4],
                    "audio": audioStoryFiles[4]
                },
                {
                    "text": story_texts[5],
                    #"image": "img4.png",
                    "image": decoded_images[5],
                    "caption": captions[5],
                    "audio": audioStoryFiles[5]
                },
                {
                    "text": story_texts[6],
                    #"image": "img4.png",
                    "image": decoded_images[6],
                    "caption": captions[6],
                    "audio": audioStoryFiles[6]
                }
            ]
 
            #st.markdown(story_pages[0]["image"])
            # Initialize session state for the current story page index
            if 'page_index' not in st.session_state:
                st.session_state.page_index = 0
 
            # Functions for navigating between pages
            def next_page():
                if st.session_state.page_index < len(story_pages) - 1:
                    st.session_state.page_index += 1
                    st.session_state.submit_btn = True
 
            def prev_page():
                if st.session_state.page_index > 0:
                    st.session_state.page_index -= 1
                    st.session_state.submit_btn = True
 
            # Get the current page's content
            current_page = story_pages[st.session_state.page_index]
 
            st.title("📖 My Storybook")
            #image = Image.open(current_page["image"])
            image = image_decode(current_page["image"])
            st.write(current_page["audio"])
            # st.audio(current_page["audio"], format='audio/mp3')
            # Create two columns: one for the story text, one for the image
            col1, col2 = st.columns(2)
 
            with col1:
                #st.markdown(f'<div class="storybook-text">{current_page["text"]}</div>', unsafe_allow_html=True)
                #st.markdown(f'<div class="storybook-text" style="height: {image.height}px;"><p>{current_page["text"]}</p></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="storybook-text"><p>{current_page["text"]}</p></div>', unsafe_allow_html=True)
                st.audio(current_page["audio"], format='audio/mp3')
            with col2:
                # Use custom HTML and CSS for image with the desired style
                #st.markdown(f'<img src="{current_page["image"]}" alt="{current_page["caption"]}" class="storybook-image">', unsafe_allow_html=True)
                st.image(image, caption=current_page["caption"], use_column_width=True)
 
            # Create Previous and Next buttons for navigation
            col1, col2, col3 = st.columns([1, 2, 1])

            st.write("Page No:", st.session_state.page_index + 1)
            with col1:
                if st.session_state.page_index > 0:
                    st.button("Previous", on_click=prev_page)
                    st.session_state.submit_btn = True
 
            with col3:
                if st.session_state.page_index < len(story_pages) - 1:
                    st.button("Next", on_click=next_page)
                    st.session_state.submit_btn = True
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
 
if __name__ == "__main__":
    main()
