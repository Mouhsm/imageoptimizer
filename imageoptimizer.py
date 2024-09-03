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

def resize_image(image_path, max_width=800):
    # Open the image and resize it to the specified width
    image = Image.open(image_path)
    width_percent = (max_width / float(image.size[0]))
    height_size = int((float(image.size[1]) * float(width_percent)))
    image = image.resize((max_width, height_size), Image.ANTIALIAS)
    
    # Save resized image to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg', mode='wb') as resized_file:
        resized_path = resized_file.name
        image.save(resized_path, 'JPEG')
    
    return resized_path

# Streamlit app
st.set_page_config(page_title="Image Optimizer", layout="centered")

# Inject custom CSS to hide Streamlit footer, menu, and header
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
            
            # Resize the optimized image for display
            resized_image_path = resize_image(optimized_image_path)
            with open(resized_image_path, "rb") as resized_file:
                st.image(resized_file.read(), caption='Optimized Image Preview', use_column_width=True)
            
            # Provide a download link
            with open(optimized_image_path, "rb") as file:
                st.download_button(
                    label="Download Optimized Image",
                    data=file,
                    file_name=optimized_file_name,
                    mime=f"image/{format_choice.lower()}"
                )
            
            # Clean up the temporary files
            os.remove(optimized_image_path)
            os.remove(resized_image_path)
