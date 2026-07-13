import io
import os
import re
from datetime import datetime

import qrcode
from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_M
from PIL import Image
import streamlit as st

HISTORY_DIR = "history"

# ----------------------------------------------------------------------------
# Theme — same tokens, fonts and component language as the homepage (app.py)
# ----------------------------------------------------------------------------

_BASE_CSS = """
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600&display=swap');

:root{
  --bg:#060911;
  --bg-alt:#0A0F1A;
  --surface:#10151F;
  --surface-2:#151D2C;
  --border:#232C3F;
  --accent:#39FF9E;
  --accent-dim:#1F8F5C;
  --violet:#8B7FFF;
  --sky:#38BDF8;
  --amber:#FFB84D;
  --danger:#FF6B6B;
  --text:#EDEFF3;
  --muted:#8A93A8;
}

html, body, [class*="css"]{
  font-family:'Inter', sans-serif;
}

.stApp{
  background:
    radial-gradient(circle at 12% -10%, rgba(57,255,158,0.06), transparent 40%),
    radial-gradient(circle at 90% 0%, rgba(139,127,255,0.08), transparent 45%),
    var(--bg);
  color:var(--text);
}

#MainMenu, footer{visibility:hidden;}

section[data-testid="stSidebar"]{
  background:var(--bg-alt);
  border-right:1px solid var(--border);
}

/* ---------- shared eyebrow / dot ---------- */
.eyebrow{
  font-family:'JetBrains Mono', monospace;
  font-size:12px;
  letter-spacing:.14em;
  color:var(--accent);
  text-transform:uppercase;
  display:flex;
  align-items:center;
  gap:8px;
  margin-bottom:10px;
}

.eyebrow .dot{
  width:7px;height:7px;border-radius:50%;
  background:var(--accent);
  box-shadow:0 0 8px var(--accent);
  animation:pulse 1.6s ease-in-out infinite;
}

@keyframes pulse{
  0%,100%{opacity:1;}
  50%{opacity:.35;}
}

@keyframes scan-x{
  0%{transform:translateX(-100%);}
  100%{transform:translateX(100%);}
}

/* ---------- page hero (compact, used on every sub-page) ---------- */
.page-hero{
  position:relative;
  border:1px solid var(--border);
  border-radius:18px;
  padding:26px 30px;
  margin-bottom:26px;
  background:linear-gradient(160deg, var(--surface) 0%, var(--surface-2) 100%);
  overflow:hidden;
}

.page-hero::before{
  content:"";
  position:absolute;
  top:0; left:0; right:0; height:2px;
  background:linear-gradient(90deg, transparent, var(--accent), transparent);
  animation:scan-x 3.5s linear infinite;
}

.page-hero-title{
  font-family:'Space Grotesk', sans-serif;
  font-weight:700;
  font-size:27px;
  margin:2px 0 6px 0;
  letter-spacing:-0.01em;
}

.page-hero-sub{
  color:var(--muted);
  font-size:14.5px;
  line-height:1.5;
  max-width:640px;
}

/* ---------- section headers ---------- */
.section-eyebrow{
  font-family:'JetBrains Mono', monospace;
  font-size:12px;
  color:var(--accent);
  letter-spacing:.12em;
  text-transform:uppercase;
  margin:6px 0 4px 0;
}

.section-title{
  font-family:'Space Grotesk', sans-serif;
  font-weight:700;
  font-size:21px;
  margin:0 0 14px 0;
}

/* ---------- result card ---------- */
.result-frame{
  background:#ffffff;
  border-radius:16px;
  padding:16px;
  border:1px solid var(--border);
  box-shadow:0 20px 50px -25px rgba(57,255,158,0.20);
}

/* ---------- analytics stat boxes ---------- */
.stat-box{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:16px;
  padding:22px;
  text-align:center;
}

.stat-box .num{
  font-family:'Space Grotesk', sans-serif;
  font-size:34px;
  font-weight:700;
  color:var(--accent);
  line-height:1;
}

.stat-box .label{
  font-family:'JetBrains Mono', monospace;
  font-size:11.5px;
  color:var(--muted);
  text-transform:uppercase;
  letter-spacing:.08em;
  margin-top:8px;
}

/* ---------- alerts (st.error / success / info / warning) ---------- */
div[data-testid="stAlert"]{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:12px;
  color:var(--text);
}

/* ---------- inputs ---------- */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
[data-baseweb="select"] > div,
[data-baseweb="base-input"]{
  background:var(--surface) !important;
  border:1px solid var(--border) !important;
  border-radius:10px !important;
  color:var(--text) !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus{
  border-color:var(--accent) !important;
  box-shadow:0 0 0 1px var(--accent) !important;
}

.stSlider [data-baseweb="slider"] div[role="slider"]{
  background:var(--accent) !important;
}

/* ---------- buttons ---------- */
.stButton>button[kind="primary"],
.stDownloadButton>button,
.stLinkButton>a{
  background:linear-gradient(135deg, var(--accent), #1FD98A) !important;
  color:#04140C !important;
  font-weight:600 !important;
  border:none !important;
  border-radius:10px !important;
  font-family:'Space Grotesk', sans-serif !important;
  transition:filter .15s ease, transform .15s ease;
}

.stButton>button[kind="primary"]:hover,
.stDownloadButton>button:hover,
.stLinkButton>a:hover{
  filter:brightness(1.08);
  transform:translateY(-1px);
}

.stButton>button[kind="secondary"]{
  background:var(--surface) !important;
  color:var(--text) !important;
  border:1px solid var(--border) !important;
  border-radius:10px !important;
  font-family:'Space Grotesk', sans-serif !important;
}

.stButton>button[kind="secondary"]:hover{
  border-color:var(--accent) !important;
  color:var(--accent) !important;
}

/* ---------- tabs ---------- */
.stTabs [data-baseweb="tab-list"]{
  gap:6px;
  border-bottom:1px solid var(--border);
}

.stTabs [data-baseweb="tab"]{
  background:transparent;
  color:var(--muted);
  font-family:'JetBrains Mono', monospace;
  font-size:13px;
  border-radius:8px 8px 0 0;
  padding:8px 16px;
}

.stTabs [aria-selected="true"]{
  color:var(--accent) !important;
  border-bottom:2px solid var(--accent) !important;
}

/* ---------- expander ---------- */
[data-testid="stExpander"]{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:12px;
}

/* ---------- file uploader / camera ---------- */
[data-testid="stFileUploaderDropzone"]{
  background:var(--surface);
  border:1px dashed var(--border);
  border-radius:12px;
}

/* ---------- dataframe ---------- */
[data-testid="stDataFrame"]{
  border:1px solid var(--border);
  border-radius:12px;
  overflow:hidden;
}

/* ---------- code blocks ---------- */
.stCodeBlock, pre{
  background:var(--surface) !important;
  border:1px solid var(--border) !important;
  border-radius:10px !important;
}

/* ---------- divider ---------- */
hr, [data-testid="stDivider"]{border-color:var(--border) !important;}

</style>
"""


def inject_base_css():
    """Injects the shared QR Studio Pro theme. Call once near the top of every page."""
    st.markdown(_BASE_CSS, unsafe_allow_html=True)


def page_hero(title: str, subtitle: str = ""):
    """Compact hero banner used at the top of every sub-page."""
    st.markdown(
        f"""
        <div class="page-hero">
          <div class="eyebrow"><span class="dot"></span>QR STUDIO PRO</div>
          <div class="page-hero-title">{title}</div>
          <div class="page-hero-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# Style controls — shared "customize appearance" panel
# ----------------------------------------------------------------------------

def style_controls(key_prefix: str, allow_version: bool = False) -> dict:
    """Renders a compact customization panel and returns the chosen style options.

    Defaults to pure black-on-white, since that combination scans most
    reliably — customization is opt-in, not the default.
    """
    with st.expander("🎨 Customize appearance", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            qr_color = st.color_picker("QR color", "#000000", key=f"{key_prefix}_qr_color")
        with c2:
            bg_color = st.color_picker("Background color", "#FFFFFF", key=f"{key_prefix}_bg_color")

        c3, c4 = st.columns(2)
        with c3:
            box_size = st.slider("Module size", 4, 20, 10, key=f"{key_prefix}_box_size")
        with c4:
            border = st.slider("Border (quiet zone)", 1, 10, 4, key=f"{key_prefix}_border")

        version = None
        if allow_version:
            version = st.slider(
                "QR version — 1 = smallest, 40 = largest / most data",
                1, 40, 1, key=f"{key_prefix}_version",
            )

        logo = st.file_uploader(
            "Embed a logo (optional)",
            type=["png", "jpg", "jpeg"],
            key=f"{key_prefix}_logo",
        )

        if logo is not None:
            st.caption("Tip: logos work best with a high error-correction QR — this is applied automatically.")

    return {
        "qr_color": qr_color,
        "bg_color": bg_color,
        "box_size": box_size,
        "border": border,
        "version": version,
        "logo": logo,
    }


# ----------------------------------------------------------------------------
# QR generation
# ----------------------------------------------------------------------------

def build_qr_image(
    data: str,
    qr_color: str = "#000000",
    bg_color: str = "#FFFFFF",
    box_size: int = 10,
    border: int = 4,
    version=None,
    logo_file=None,
) -> Image.Image:
    """Builds a PIL QR code image, optionally with a centered logo."""
    qr = qrcode.QRCode(
        version=version,
        error_correction=ERROR_CORRECT_H if logo_file is not None else ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=version is None)

    img = qr.make_image(fill_color=qr_color, back_color=bg_color).convert("RGB")

    if logo_file is not None:
        img = _embed_logo(img, logo_file)

    return img


def _embed_logo(img: Image.Image, logo_file) -> Image.Image:
    logo = Image.open(logo_file).convert("RGBA")

    qr_w, qr_h = img.size
    logo_target = qr_w // 4
    logo.thumbnail((logo_target, logo_target), Image.LANCZOS)

    pad = 10
    mount = Image.new("RGBA", (logo.size[0] + pad * 2, logo.size[1] + pad * 2), "white")
    mount.paste(logo, (pad, pad), logo)

    pos = ((qr_w - mount.size[0]) // 2, (qr_h - mount.size[1]) // 2)
    base = img.convert("RGBA")
    base.paste(mount, pos, mount)
    return base.convert("RGB")


# ----------------------------------------------------------------------------
# Result rendering
# ----------------------------------------------------------------------------

def render_result(img: Image.Image, type_label: str, data: str, filename_prefix: str, name_key: str) -> str:
    """Displays the generated QR, a download button, and a label input.
    Returns the label the user typed in, for use with unique_path()."""

    st.markdown('<div class="section-eyebrow">Result</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{type_label} QR is ready</div>', unsafe_allow_html=True)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    col_img, col_meta = st.columns([1, 1.3], gap="large")

    with col_img:
        st.markdown('<div class="result-frame">', unsafe_allow_html=True)
        st.image(img, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.write("")
        st.download_button(
            "📥 Download PNG",
            data=buf.getvalue(),
            file_name=f"{filename_prefix}.png",
            mime="image/png",
            use_container_width=True,
        )

    with col_meta:
        custom_name = st.text_input(
            "Label this QR code",
            placeholder=f"My {type_label} QR",
            key=name_key,
        )
        with st.expander("View raw payload"):
            st.code(data, language="text")

    return custom_name


# ----------------------------------------------------------------------------
# File naming
# ----------------------------------------------------------------------------

def unique_path(qr_type: str, custom_name: str = "") -> str:
    """Builds a unique, filesystem-safe path under history/ to save a QR image."""
    os.makedirs(HISTORY_DIR, exist_ok=True)

    safe_name = re.sub(r"[^a-zA-Z0-9_-]+", "_", (custom_name or "").strip()).strip("_")
    base = f"{qr_type}_{safe_name}" if safe_name else qr_type

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    candidate = os.path.join(HISTORY_DIR, f"{base}_{stamp}.png")

    counter = 1
    while os.path.exists(candidate):
        candidate = os.path.join(HISTORY_DIR, f"{base}_{stamp}_{counter}.png")
        counter += 1

    return candidate
