import streamlit as st

st.set_page_config(
    page_title="My Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://extremelycoolapp.com",
        "Report a bug": "https://extremelycoolapp.com",
        "About": "# This is a header. This is an extremely cool app!",
    },
)

# Your normal app code goes here
st.title("Welcome to my App")
