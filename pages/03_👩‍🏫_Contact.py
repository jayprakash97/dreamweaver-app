import streamlit as st

st.title("Contact with WonderScriber Team")

with st.form("form_key"):
    st.write("Craft personalized stories that bring adventure to life and ignite imagination and creativity")
    Department = st.selectbox("Department", options=["Sales", "Human Resources", "Information Technology", "Public Relation", "Complaince", "Marketing", "Data Engineering", "Data Science", "Data Analytics"])
    Full_name = st.text_input("Enter your full name. (First Name, Middle Name, Last Name)")
    Company = st.text_input("Enter your Company Name")
    Country = st.text_input("Enter your Country Name")
    State = st.text_input("Enter your State or Province Name")
    email = st.text_input("Enter your email address")
    phone = st.text_input("Enter your phone# (country code, city code, and local phone number)")
    question = st.text_input("Question or Comments")
    submit_btn = st.form_submit_button("Submit")

