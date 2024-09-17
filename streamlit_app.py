import streamlit as st

st.title('🎈 DreamWeaver')

st.write('Hello world!')
x = st.text_input("Enter your favorite story theme")
st.write(f"Your favorite story theme is: {x}")
is_clicked = st.button("Click Me")
st.write("## This is a H2 Title!")
# https://doc-markdown.streamlit.app/
# https://docs.streamlit.io/develop/api-reference
with st.sidebar:
        st.header('About app')
        st.write("This is my first app")
st.header("This is the headline")
st.markdown(" THis is created using st.markdown")
col1, col2 =  st.columns(2)
with col1:
    x = st.slider("Choose an x value", 1, 10)
with col2:
        st.write("The value of :red[***x***] is", x)

chart_data = pd.DataFrame(np.random.randn(20,3), columns=["Column 1", "Column 2", "Column 3"])
