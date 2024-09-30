import streamlit as st

st.title("Contact with WonderScriber Team")

with st.form("form_key"):
    st.write("Craft personalized stories that bring adventure to life and ignite imagination and creativity")
    Department = st.selectbox("Department", options=["Sales", "Human Resources", "Information Technology", "Public Relation", "Complaince", "Marketing", "Data Engineering", "Data Science", "Data Analytics"])
    Full_name = st.text_input("Enter your full name. (Frist Name, Middle Name, Last Name)")
    Company = st.text_input("Enter your Company Name"])
    audience = st.selectbox("Audience", options=["children", "young adult", "adult", "senior"])
    story_setting = st.selectbox("Story Setthing", options=["Magical Kingdoms", "Underwater Kingdoms", "Pirate ships", "Exotic locations", "Imaginary world", "Digital words", "Others"])
    story_type = st.selectbox("Story Type", options=["Fantacy", "Fairy Tales", "Mythology", "Bedtime stories", "Adventure", "Mystery", "Love", "Horror", ])
    story_theme = st.text_input("What would be topic of the story?", placeholder="Leave brief idea of a story")
    moral_lesson = st.text_input("What would be the moral of this story?")
    story_length = st.selectbox("Story Length (in words) ", options=["300", "400", "500"])
    
    submit_btn = st.form_submit_button("Submit")

