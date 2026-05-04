import os
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from openai import OpenAI

# Read API keys from environment (DO NOT hardcode)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REMOVE_BG_API_KEY = os.getenv("REMOVE_BG_API_KEY")

# Init OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(page_title="AI Photo Upgrader", layout="centered")

st.title("✨ AI Photo Upgrader")
st.write("Upload a product image and generate a professional studio-style visual.")

st.warning("⚠️ Use a clear product image (not a full background scene)")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

# ---- OpenAI: background ideas ----
if st.button("💡 Generate Background Ideas"):
    if not OPENAI_API_KEY:
        st.error("OpenAI API key not set.")
    else:
        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{
                "role": "user",
                "content": "Suggest 3 short background ideas for product photography (1 line each)."
            }]
        )
        st.info(resp.choices[0].message.content)

# ---- Background choice ----
background_option = st.selectbox(
    "Choose Background",
    ["White Studio", "Office", "Kitchen"]
)

# ---- Main flow ----
if uploaded_file:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original")
        st.image(uploaded_file, width=260)

    if st.button("✨ Enhance Image"):
        if not REMOVE_BG_API_KEY:
            st.error("Remove.bg API key not set.")
        else:
            with st.spinner("Processing..."):

                # 1) Remove background via Remove.bg
                r = requests.post(
                    "https://api.remove.bg/v1.0/removebg",
                    files={"image_file": uploaded_file},
                    data={"size": "auto"},
                    headers={"X-Api-Key": REMOVE_BG_API_KEY},
                )

                if r.status_code != requests.codes.ok:
                    st.error("❌ Remove.bg error: " + r.text)
                else:
                    # 2) Load cutout
                    product = Image.open(BytesIO(r.content)).convert("RGBA")

                    # 3) Load selected background
                    if background_option == "White Studio":
                        bg = Image.open("backgrounds/white.jpg")
                    elif background_option == "Office":
                        bg = Image.open("backgrounds/office.jpg")
                    else:
                        bg = Image.open("backgrounds/kitchen.jpg")

                    bg = bg.resize((600, 600)).convert("RGBA")

                    # 4) Resize & paste product
                    product = product.resize((300, 300))
                    bg.paste(product, (150, 150), product)

                    # 5) Show result
                    with col2:
                        st.subheader("Enhanced")
                        st.image(bg, width=260)

                    # 6) Download
                    buf = BytesIO()
                    bg.save(buf, format="PNG")
                    st.download_button(
                        "⬇ Download Final Image",
                        buf.getvalue(),
                        "final.png",
                        "image/png"
                    )
