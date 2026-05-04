import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os

st.set_page_config(page_title="AI Photo Upgrader", layout="centered")

st.title("✨ AI Photo Upgrader")
st.write("Upload a product image and generate a professional studio-style visual.")

st.warning("⚠️ Use a clear product image (not full background scene)")

# 🔐 Secure API key (DO NOT hardcode in real apps)
API_KEY = "FMi6RTjVxuzNamqFSFWGqThk"

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

background_option = st.selectbox(
    "Choose Background",
    ["White Studio", "Office", "Kitchen"]
)

if uploaded_file:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original")
        st.image(uploaded_file, width=250)

    if st.button("✨ Enhance Image"):
        with st.spinner("Processing..."):

            response = requests.post(
                "https://api.remove.bg/v1.0/removebg",
                files={"image_file": uploaded_file.getvalue()},
                data={"size": "auto"},
                headers={"X-Api-Key": API_KEY},
            )

            if response.status_code == requests.codes.ok:
                product_img = Image.open(BytesIO(response.content)).convert("RGBA")

                # 📁 Load background images
                try:
                    if background_option == "White Studio":
                        bg = Image.open("backgrounds/white.jpg")
                    elif background_option == "Office":
                        bg = Image.open("backgrounds/office.jpg")
                    else:
                        bg = Image.open("backgrounds/kitchen.jpg")
                except:
                    st.error("❌ Background images not found. Create a 'backgrounds' folder.")
                    st.stop()

                bg = bg.resize((600, 600)).convert("RGBA")

                # Resize product image
                product_img = product_img.resize((300, 300))

                # Paste product at center
                bg.paste(product_img, (150, 150), product_img)

                with col2:
                    st.subheader("Enhanced")
                    st.image(bg, width=250)

                # Download button
                buf = BytesIO()
                bg.save(buf, format="PNG")

                st.download_button(
                    "⬇ Download Final Image",
                    buf.getvalue(),
                    "final.png",
                    "image/png"
                )

            else:
                st.error("❌ API Error: " + response.text)