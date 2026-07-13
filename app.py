import streamlit as st
from database import get_stats
from utils import inject_base_css, page_hero

st.set_page_config(
    page_title="QR Studio Pro",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_base_css()

page_hero(
    "📱 QR Studio Pro",
    "Generate • Customize • Scan • Track — everything QR, in one place.",
)

stats = get_stats()

st.write("")
s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown(
        f'<div class="stat-box"><div class="num">{stats["total"]}</div>'
        f'<div class="label">QR Codes Generated</div></div>',
        unsafe_allow_html=True,
    )
with s2:
    types_count = len(stats["by_type"])
    st.markdown(
        f'<div class="stat-box"><div class="num">{types_count}</div>'
        f'<div class="label">QR Types Used</div></div>',
        unsafe_allow_html=True,
    )
with s3:
    st.markdown(
        f'<div class="stat-box"><div class="num">{stats["favorites"]}</div>'
        f'<div class="label">Favorites</div></div>',
        unsafe_allow_html=True,
    )
with s4:
    top_type = stats["by_type"][0]["qr_type"] if stats["by_type"] else "—"
    st.markdown(
        f'<div class="stat-box"><div class="num" style="font-size:22px">{top_type}</div>'
        f'<div class="label">Most Used Type</div></div>',
        unsafe_allow_html=True,
    )

st.write("")
st.write("")

c1, c2, c3 = st.columns(3)
with c1:
    st.info("🌐 **Website QR**\n\nGenerate QR codes for any website or link.")
with c2:
    st.success("📶 **WiFi QR**\n\nShare WiFi access without typing passwords.")
with c3:
    st.warning("📧 **Email QR**\n\nInstant, pre-filled email QR codes.")

c4, c5, c6 = st.columns(3)
with c4:
    st.info("📞 **Phone / SMS / WhatsApp**\n\nOne tap to call, text, or chat.")
with c5:
    st.success("💳 **UPI Payment QR**\n\nGoogle Pay, PhonePe, Paytm & BHIM ready.")
with c6:
    st.warning("📇 **Contact (vCard) QR**\n\nShare a full contact card instantly.")

c7, c8, c9 = st.columns(3)
with c7:
    st.info("📷 **QR Scanner**\n\nScan from an image or your webcam.")
with c8:
    st.success("🗂 **History**\n\nEvery QR you've made, searchable and downloadable.")
with c9:
    st.warning("📊 **Analytics**\n\nSee your QR usage trends at a glance.")

st.divider()

left, right = st.columns(2)
with left:
    st.subheader("🚀 Included")
    for item in [
        "Website QR", "WiFi QR", "Email QR", "Phone / SMS / WhatsApp QR",
        "UPI Payment QR", "Contact (vCard) QR",
    ]:
        st.checkbox(item, True, disabled=True, key=f"inc_{item}")

with right:
    st.subheader("✨ Extras")
    for item in [
        "Logo Embedding (with transparency)", "Custom Colors",
        "QR Scanner (image + webcam)", "Searchable History", "Usage Analytics",
    ]:
        st.checkbox(item, True, disabled=True, key=f"ext_{item}")

st.divider()
st.success("👈 Pick a page from the sidebar to get started.")
