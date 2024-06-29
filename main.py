import streamlit as st
import datetime
import model_inference
from PIL import Image


# Multi select
selections = st.multiselect("Photo style:", ["Kuindzhi", "Kandinsky", "Malevich"])

# Number input
choice = st.number_input("Choose the number of epochs", 0, 50)

# File upload
data = st.file_uploader("Share png file", type=['png'])

if data != None:
     edited_image = model_inference.inference_edit_image(data)

     # User image show
     st.image(edited_image, caption="Your image", use_column_width=True)

