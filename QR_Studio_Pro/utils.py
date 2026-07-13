"""
QR Studio Pro — shared helpers.
Keeps every generator page consistent: same sidebar controls, same logo
handling (with real transparency support), same safe file naming.
"""

import os
import re
import uuid
from datetime import datetime
from io import BytesIO

import qrcode
import streamlit as st
from PIL import Image

GENERATED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated")
os.makedirs(GENERATED_DIR, exist_ok=True)


# --------------------------------------------------------------------------
# Styling — shared CSS injected by every page for a consistent look
# --------------------------------------------------------------------------
BASE_CSS = """
<style>
.stApp { background: #0E1117; }

.qr-hero{
    padding: 22px 25px;
    border-radius: 18px;
    background: linear-gradient(135deg,#3b82f6,#8b5cf6);
    color: white;
    margin-bottom: 10px;
}
.qr-hero h1{ margin:0; font-size: 28px; }
.qr-hero p{ margin:4px 0 0 0; color:#e5e7eb; font-size:15px; }

.qr-card{
    background:#1f2937;
    padding:20px;
    border-radius:15px;
    border:1px solid #374151;
}

.stat-box{
    background:#1f2937;
    border-radius:14px;
    padding:16px 18px;
    border:1px solid #374151;
    text-align:center;
}
.stat-box .num{ font-size:30px; font-weight:700; color:#ffffff; }
.stat-box .label{ font-size:13px; color:#9ca3af; }

div[data-testid="stImage"] img{
    border-radius: 12px;
    border: 6px solid white;
}
</style>
"""


def inject_base_css():
    st.markdown(BASE_CSS, unsafe_allow_html=True)


def page_hero(title, subtitle):
    st.markdown(
        f"""<div class="qr-hero"><h1>{title}</h1><p>{subtitle}</p></div>""",
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------
# Shared sidebar controls for every generator page
# --------------------------------------------------------------------------
def style_controls(key_prefix, allow_version=False):
    """Renders the shared 'Design' controls in the sidebar and returns a dict."""
    st.sidebar.header("🎨 Design")

    qr_color = st.sidebar.color_picker("QR Color", "#000000", key=f"{key_prefix}_qc")
    bg_color = st.sidebar.color_picker("Background", "#FFFFFF", key=f"{key_prefix}_bg")

    box_size = st.sidebar.slider("Box Size", 5, 20, 10, key=f"{key_prefix}_box")
    border = st.sidebar.slider("Border", 1, 10, 4, key=f"{key_prefix}_border")

    version = None
    if allow_version:
        version = st.sidebar.slider("QR Version (density)", 1, 40, 5, key=f"{key_prefix}_ver")

    logo = st.sidebar.file_uploader(
        "Logo (optional)", type=["png", "jpg", "jpeg"], key=f"{key_prefix}_logo"
    )

    return {
        "qr_color": qr_color,
        "bg_color": bg_color,
        "box_size": box_size,
        "border": border,
        "version": version,
        "logo": logo,
    }


# --------------------------------------------------------------------------
# Core QR generation
# --------------------------------------------------------------------------
def build_qr_image(data, qr_color="#000000", bg_color="#FFFFFF", box_size=10,
                    border=4, version=None, logo_file=None):
    """Builds a PIL QR image, with proper transparent-logo support."""
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=qr_color, back_color=bg_color).convert("RGB")

    if logo_file is not None:
        img = _embed_logo(img, logo_file)

    return img


def _embed_logo(img, logo_file):
    logo_img = Image.open(logo_file).convert("RGBA")

    qr_w, qr_h = img.size
    logo_size = qr_w // 4
    logo_img = logo_img.resize((logo_size, logo_size))

    # White padded backdrop behind the logo so the QR stays scannable
    pad = int(logo_size * 0.12)
    backdrop = Image.new("RGBA", (logo_size + pad * 2, logo_size + pad * 2), "white")
    backdrop.paste(logo_img, (pad, pad), mask=logo_img)

    pos = ((qr_w - backdrop.width) // 2, (qr_h - backdrop.height) // 2)
    img = img.convert("RGBA")
    img.paste(backdrop, pos, mask=backdrop)
    return img.convert("RGB")


def image_to_png_bytes(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def safe_filename(name, fallback="MyQR"):
    name = (name or "").strip()
    if not name:
        name = fallback
    name = re.sub(r"[^A-Za-z0-9_\-]+", "_", name)
    return name[:60] or fallback


def unique_path(qr_type, custom_name=None):
    """Builds a collision-free path under /generated so repeated QRs never overwrite each other."""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    short_id = uuid.uuid4().hex[:6]
    base = safe_filename(custom_name, fallback=qr_type)
    file_name = f"{base}_{stamp}_{short_id}.png"
    return os.path.join(GENERATED_DIR, file_name)


def render_result(img, qr_type, data, download_name, filename_key):
    """Common 'result' block: filename input, save-to-history, preview, download."""
    st.success("✅ QR Code Generated Successfully!")

    col_img, col_meta = st.columns([1, 1])

    with col_img:
        st.image(img, width=320)

    with col_meta:
        st.markdown("**Save as**")
        custom_name = st.text_input(
            "File name", value=qr_type.replace(" ", "_"), key=filename_key,
            label_visibility="collapsed",
        )
        buffer = image_to_png_bytes(img)
        st.download_button(
            "📥 Download PNG",
            data=buffer,
            file_name=f"{safe_filename(custom_name)}.png",
            mime="image/png",
            use_container_width=True,
        )
        with st.expander("Raw QR payload"):
            st.code(data)

    return custom_name
