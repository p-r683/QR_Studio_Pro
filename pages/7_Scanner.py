import streamlit as st
import cv2
import numpy as np
from PIL import Image
from utils import inject_base_css, page_hero

st.set_page_config(page_title="QR Scanner", page_icon="📷")
inject_base_css()
page_hero("📷 QR Scanner", "Scan a QR code from an uploaded image or your camera.")

detector = cv2.QRCodeDetector()


def _decode(pil_image):
    img = np.array(pil_image.convert("RGB"))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    data, points, _ = detector.detectAndDecode(img)
    return data


def _show_result(data):
    if data:
        st.success("✅ QR Code Detected")
        st.code(data)
        if data.startswith("http://") or data.startswith("https://"):
            st.link_button("🌐 Open Link", data, use_container_width=True)
    else:
        st.error("❌ No QR Code Found. Try a clearer, well-lit photo.")


tab1, tab2 = st.tabs(["🖼 Upload Image", "📷 Camera"])

with tab1:
    uploaded = st.file_uploader("Upload QR Image", type=["png", "jpg", "jpeg"])
    if uploaded:
        image = Image.open(uploaded)
        st.image(image, caption="Uploaded Image", width=320)
        _show_result(_decode(image))

with tab2:
    st.caption("Uses your browser's camera — works even when the app is hosted remotely.")
    snapshot = st.camera_input("Take a photo of the QR code")
    if snapshot:
        image = Image.open(snapshot)
        _show_result(_decode(image))
