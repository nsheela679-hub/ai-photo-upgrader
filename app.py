import streamlit as st
from PIL import Image, ImageOps
import io

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Photo Upgrader", layout="centered")

st.markdown(
    """
    <style>
    .main {
        text-align: center;
    }
    .stButton>button {
        background-color: #000;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("✨ AI Photo Upgrader")
st.write("Upload a product image and generate a clean studio-style visual")

st.warning("Use a clear product image (not full background scene)")

# ------------------ FILE UPLOAD ------------------
uploaded_file = st.file_uploader("📤 Upload Image", type=["jpg", "png", "jpeg"])

# ------------------ BACKGROUND OPTION ------------------
bg_option = st.selectbox(
    "🎨 Choose Background",
    ["White Studio", "Black Studio", "Gray Studio"]
)

# ------------------ PROCESS IMAGE ------------------
def apply_background(image, bg_option):
    image = image.convert("RGBA")

    if bg_option == "White Studio":
        bg_color = (255, 255, 255)
    elif bg_option == "Black Studio":
        bg_color = (0, 0, 0)
    else:
        bg_color = (200, 200, 200)

    background = Image.new("RGB", image.size, bg_color)
    background.paste(image, mask=image.split()[3])  # Use alpha channel

    return background

# ------------------ MAIN LOGIC ------------------
if uploaded_file:
    image = Image.open(uploaded_file)

    st.subheader("🖼 Uploaded Image")
    st.image(image, use_column_width=True)

    processed_image = apply_background(image, bg_option)

    st.subheader("✨ Processed Image")
    st.image(processed_image, use_column_width=True)

    # Convert image to bytes
    img_bytes = io.BytesIO()
    processed_image.save(img_bytes, format="PNG")

    st.download_button(
        label="⬇ Download Image",
        data=img_bytes.getvalue(),
        file_name="ai_upgraded.png",
        mime="image/png"
    )

else:
    st.info("Upload an image to get started 🚀")
