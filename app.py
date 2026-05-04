import streamlit as st
from PIL import Image
import io
from rembg import remove

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Photo Upgrader", layout="centered")

st.title("✨ AI Photo Upgrader")
st.write("Upload a product image and generate a studio-style visual")

st.warning("Use a clear product image (not full background scene)")

# ------------------ UPLOAD ------------------
uploaded_file = st.file_uploader("📤 Upload Image", type=["jpg", "png", "jpeg"])

# ------------------ BACKGROUND OPTION ------------------
bg_option = st.selectbox(
    "🎨 Choose Background",
    ["White Studio", "Black Studio", "Gray Studio"]
)

# ------------------ FUNCTIONS ------------------

# Remove background (AI)
def remove_background(image):
    return remove(image)

# Add background color
def add_background(image, bg_option):
    image = image.convert("RGBA")

    if bg_option == "White Studio":
        bg_color = (255, 255, 255)
    elif bg_option == "Black Studio":
        bg_color = (0, 0, 0)
    else:
        bg_color = (200, 200, 200)

    background = Image.new("RGB", image.size, bg_color)
    background.paste(image, mask=image.split()[3])

    return background

# ------------------ MAIN ------------------
if uploaded_file:
    image = Image.open(uploaded_file)

    st.subheader("🖼 Uploaded Image")
    st.image(image, use_column_width=True)

    # Remove background
    with st.spinner("Removing background..."):
        no_bg = remove_background(image)

    st.subheader("✨ Background Removed")
    st.image(no_bg, use_column_width=True)

    # Add selected background
    final_image = add_background(no_bg, bg_option)

    st.subheader("🎨 Final Image")
    st.image(final_image, use_column_width=True)

    # Download
    img_bytes = io.BytesIO()
    final_image.save(img_bytes, format="PNG")

    st.download_button(
        "⬇ Download Image",
        data=img_bytes.getvalue(),
        file_name="ai_output.png",
        mime="image/png"
    )

else:
    st.info("Upload an image to get started 🚀")
