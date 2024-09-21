import streamlit as st

with st.form("form_key"):
    st.write("Craft personalized stories that bring adventure to life and ignite imagination and creativity")
    
    gender = st.selectbox("Your Gender", options=["Male", "Female", "Don't want to share"])
    main_character = st.data_input("What will be the name of main character?")
    # audience = st.selectbox("Audience", options=["children", "young adult", "adult", "senior"]
    story_setting = st.selectbox("Story Setthing", options=["Magical Kingdoms", "Underwater Kingdoms", "Pirate ships", "Exotic locations", "Imaginary world", "Digital words", "Others"])
    story_type = st.selectbox("Story Type", options=["Fantacy", "Fairy Tales", "Mythology", "Bedtime stories", "Adventure", "Mystery", "Love", "Horror", ])
    story_theme = st.text_area("What would be topic of the story?", placeholder="Leave brief idea of a story")
    moral_lesson = st.data_input("What would be the moral of this story?")
    story_length = st.selectbox("Story Length", options=["300 Characters", "400 characters", "500 characters"])
    
    submit_btn = st.form_submit_button("Submit")

st.write(f"""Your story summary:
Audience: {audience}
Main Character: {main_character}
Story Setting: {story_setting}
Story Type: {story_type}
Story Theme: {story_theme}
Moral Lesson: {moral_lesson}
Story Size (in words) : {story_length}
]

Your story is here
""")
