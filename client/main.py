import streamlit as st
import requests
from PIL import Image


# Set base URL for API endpoint
BASE_URL = "http://localhost:8000"

if "counter" not in st.session_state:
    st.session_state.counter = 0

# Increment counter when button is clicked
if st.button("Increment"):
    st.session_state.counter += 1
st.write(st.session_state.counter)
if st.button("Decrement"):
    st.session_state.counter -= 1

# Create file uploader widget
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    with Image.open(uploaded_file) :
        st.image(uploaded_file)
# Create search button
if st.button("Search"):
    # Check if file is uploaded
    if uploaded_file is None:
        st.write("Please upload a file.")
    else:
        # Send HTTP GET request to API endpoint
        response = requests.get(f"{BASE_URL}/search/{st.session_state.counter}", files={"file": uploaded_file})
            
                
        with open(f"result{st.session_state.counter}.jpg", "wb") as f:
            f.write(response.content)
            
            # Display image in Streamlit
        st.image(f"result{st.session_state.counter}.jpg")
            