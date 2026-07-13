import streamlit as st
from urllib.parse import quote
from database import add_history
from utils import build_qr_image, render_result, style_controls, inject_base_css, page_hero, unique_path

st.set_page_config(page_title="Email QR", page_icon="📧")
inject_base_css()
page_hero("📧 Email QR Generator", "Generate a QR code that opens a pre-filled email draft.")

email = st.text_input("Recipient Email", placeholder="example@gmail.com")
subject = st.text_input("Subject", placeholder="Meeting Invitation")
body = st.text_area("Email Body", placeholder="Type your message...")

style = style_controls("email")

generate = st.button("Generate Email QR", type="primary", use_container_width=True)

if generate:
    if "@" not in email or "." not in email.split("@")[-1]:
        st.error("Please enter a valid email address.")
        st.stop()

    qr_data = f"mailto:{email}?subject={quote(subject)}&body={quote(body)}"

    img = build_qr_image(
        qr_data,
        qr_color=style["qr_color"],
        bg_color=style["bg_color"],
        box_size=style["box_size"],
        border=style["border"],
        logo_file=style["logo"],
    )
    st.session_state["_email_result"] = {"img": img, "data": qr_data}

if "_email_result" in st.session_state:
    res = st.session_state["_email_result"]
    custom_name = render_result(res["img"], "Email", res["data"], "Email_QR", "email_name")

    if st.button("💾 Save to History", key="email_save"):
        path = unique_path("Email", custom_name)
        res["img"].save(path)
        add_history("Email", res["data"], path, label=custom_name)
        st.toast("Saved to history!", icon="✅")
