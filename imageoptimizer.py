import streamlit as st
from PIL import Image
import io
import tempfile
import os

def optimize_image_file(image_file, format_choice):
    # Open the image using Pillow
    image = Image.open(image_file)
    
    # Convert image to RGB if saving as JPEG
    if format_choice == 'JPEG' and image.mode in ('RGBA', 'P'):
        image = image.convert('RGB')
    
    # Get the original file name without extension
    original_file_name, _ = os.path.splitext(image_file.name)
    
    # Create a temporary file for the optimized image
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{format_choice.lower()}', mode='wb') as temp_file:
        temp_file_path = temp_file.name

        # Save the image to the temporary file in the desired format with optimization
        image.save(temp_file_path, format=format_choice, quality=85, optimize=True)
    
    # Return the file path and original file name
    return temp_file_path, f"{original_file_name}.{format_choice.lower()}"

# Streamlit app
st.set_page_config(page_title="Image Optimizer", layout="centered")

# Inject custom CSS to hide Streamlit footer, menu, and header and center the download button
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Style for the Optimize button */
    .stButton>button {
        background-color: #007bff; /* Bootstrap blue */
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #0056b3; /* Darker blue on hover */
    }

    /* Center the download button with reduced space */
    .stDownloadButton {
        display: flex;
        justify-content: center;
        margin-top: 5px; /* Reduced space */
    }
    .stDownloadButton>button {
        background-color: #c8553d; /* Updated color */
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    .stDownloadButton>button:hover {
        background-color: #a73e2d; /* Slightly darker on hover */
    }
    </style>
    """, unsafe_allow_html=True)

# Upload file
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "webp"])

# Format selection
format_choice = st.selectbox("Select format to optimize", ["PNG", "JPEG", "WEBP"])

if uploaded_file and format_choice:
    # Optimize button
    if st.button("Optimize"):
        with st.spinner('Optimizing your image, please wait...'):
            # Optimize image
            optimized_image_path, optimized_file_name = optimize_image_file(uploaded_file, format_choice)
            
            # Load the optimized image
            with open(optimized_image_path, "rb") as file:
                img_data = file.read()
            
            # Display the download button centered with reduced space
            st.markdown('<div class="stDownloadButton">', unsafe_allow_html=True)
            st.download_button(
                label="Download Optimized Image",
                data=img_data,
                file_name=optimized_file_name,
                mime=f"image/{format_choice.lower()}"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display the optimized image
            st.image(img_data, caption='Optimized Image', use_column_width=True)
            
            # Clean up the temporary file
            os.remove(optimized_image_path)
