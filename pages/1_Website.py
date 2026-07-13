import streamlit as st
from database import add_history
from utils import build_qr_image, render_result, style_controls, inject_base_css, page_hero

st.set_page_config(page_title="Website QR", page_icon="🌐")
inject_base_css()
page_hero("🌐 Website QR Generator", "Turn any link into a scannable QR code.")

url = st.text_input("Website URL", placeholder="https://example.com")

style = style_controls("website", allow_version=True)

generate = st.button("Generate QR", type="primary", use_container_width=True)

if generate:
    if not url.strip():
        st.error("Please enter a website URL.")
        st.stop()
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url

    img = build_qr_image(
        url,
        qr_color=style["qr_color"],
        bg_color=style["bg_color"],
        box_size=style["box_size"],
        border=style["border"],
        version=style["version"],
        logo_file=style["logo"],
    )
    st.session_state["_website_result"] = {"img": img, "data": url}

if "_website_result" in st.session_state:
    res = st.session_state["_website_result"]
    custom_name = render_result(res["img"], "Website", res["data"], "Website_QR", "website_name")

    if st.button("💾 Save to History", key="website_save"):
        from utils import unique_path
        path = unique_path("Website", custom_name)
        res["img"].save(path)
        add_history("Website", res["data"], path, label=custom_name)
        st.toast("Saved to history!", icon="✅")
