import streamlit as st
import requests
import json
 
# AWS API URL for POST request
AWS_API_URL = "https://wacnqhon34.execute-api.us-east-1.amazonaws.com/dev/"
 
# Optional: Set up headers (if using an API key or authentication)
headers = {
 #   "x-api-key": "your-api-key",  # Remove if your API doesn't require a key
    "Content-Type": "application/json",  # Specify the content type for the POST request
}
 
# Streamlit app title
st.title("Streamlit POST Request to AWS API")
 
# Create input fields to collect data for the POST request body
name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=0)
 
# Create a button that triggers the POST request
if st.button("Submit"):
    # Create the payload (data) to be sent in the POST request
    payload = {
     "story_type" : "children",
     "main_character" : "Laila",
     "story_theme" : "Brushing the tooth",
     "moral_lesson" : "develop hygiene practices",
     "setting" : "megical kingdom"
    }

    try:
        # Make a POST request to the AWS API
        response = requests.post(AWS_API_URL, headers=headers, json=payload)
 
        # Check if the request was successful (status code 200-299)
        if response.status_code == 200:
            data = response.json()  # Parse JSON response
            st.success("POST request successful!")
            st.write("Response from API:", data)
        else:
            st.error(f"Failed with status code: {response.status_code}")
            st.write(response.text)  # Display the error message from API
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
# has context menu
