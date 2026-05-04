import streamlit as st
from PIL import Image

st.title("✨ AI Photo Upgrader")

st.write("Upload a product image and generate a professional studio-style visual.")

st.warning("Use a clear product image (not full background scene)")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

background = st.selectbox("Choose Background", ["White Studio", "Black Studio"])

if uploaded_file:
    image = Image.open(uploaded_file)

    st.subheader("Original Image")
    st.image(image, use_column_width=True)

    # SIMPLE PROCESSING (Demo)
    if background == "White Studio":
        processed = image.convert("RGB")
    else:
        processed = image.convert("L")  # black/white effect

    st.subheader("Upgraded Image")
    st.image(processed, use_column_width=True)
