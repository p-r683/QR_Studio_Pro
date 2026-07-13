import streamlit as st
from urllib.parse import quote
from database import add_history
from utils import build_qr_image, render_result, style_controls, inject_base_css, page_hero, unique_path

st.set_page_config(page_title="Phone & WhatsApp QR", page_icon="📞")
inject_base_css()
page_hero("📞 Phone • SMS • WhatsApp QR", "One tap to call, text, or start a WhatsApp chat.")

style = style_controls("phone")

tab1, tab2, tab3 = st.tabs(["📞 Phone", "💬 SMS", "🟢 WhatsApp"])


def _generate_and_show(qr_type, data, session_key, filename_key, save_key):
    img = build_qr_image(
        data,
        qr_color=style["qr_color"],
        bg_color=style["bg_color"],
        box_size=style["box_size"],
        border=style["border"],
        logo_file=style["logo"],
    )
    st.session_state[session_key] = {"img": img, "data": data, "type": qr_type}


def _show_result(session_key, filename_key, save_key):
    if session_key in st.session_state:
        res = st.session_state[session_key]
        custom_name = render_result(res["img"], res["type"], res["data"], f"{res['type']}_QR", filename_key)
        if st.button("💾 Save to History", key=save_key):
            path = unique_path(res["type"], custom_name)
            res["img"].save(path)
            add_history(res["type"], res["data"], path, label=custom_name)
            st.toast("Saved to history!", icon="✅")


with tab1:
    st.subheader("Phone Call QR")
    phone = st.text_input("Phone Number", placeholder="+919876543210", key="phone_num")
    if st.button("Generate Phone QR", key="phone_btn"):
        if not phone.strip():
            st.error("Enter a phone number.")
        else:
            _generate_and_show("Phone", f"tel:{phone.strip()}", "_phone_result", "phone_name", "phone_save")
    _show_result("_phone_result", "phone_name", "phone_save")

with tab2:
    st.subheader("SMS QR")
    sms_number = st.text_input("Phone Number", placeholder="+919876543210", key="sms_num")
    sms_msg = st.text_area("SMS Message", key="sms_msg")
    if st.button("Generate SMS QR", key="sms_btn"):
        if not sms_number.strip():
            st.error("Enter a phone number.")
        else:
            _generate_and_show("SMS", f"SMSTO:{sms_number.strip()}:{sms_msg}", "_sms_result", "sms_name", "sms_save")
    _show_result("_sms_result", "sms_name", "sms_save")

with tab3:
    st.subheader("WhatsApp QR")
    wa_number = st.text_input("WhatsApp Number (with country code, no +)", placeholder="919876543210", key="wa_num")
    wa_msg = st.text_area("Message", key="wa_msg")
    if st.button("Generate WhatsApp QR", key="wa_btn"):
        if not wa_number.strip().isdigit():
            st.error("Enter a valid WhatsApp number, digits only, including country code.")
        else:
            data = f"https://wa.me/{wa_number.strip()}?text={quote(wa_msg)}"
            _generate_and_show("WhatsApp", data, "_wa_result", "wa_name", "wa_save")
    _show_result("_wa_result", "wa_name", "wa_save")
