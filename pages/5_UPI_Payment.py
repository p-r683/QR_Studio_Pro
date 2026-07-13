import streamlit as st
from urllib.parse import quote
from database import add_history
from utils import build_qr_image, render_result, style_controls, inject_base_css, page_hero, unique_path

st.set_page_config(page_title="UPI Payment QR", page_icon="💳")
inject_base_css()
page_hero("💳 UPI Payment QR Generator", "Generate QR codes for Google Pay, PhonePe, Paytm, BHIM & more.")

upi = st.text_input("UPI ID", placeholder="example@upi")
name = st.text_input("Payee Name", placeholder="Pranshu Verma")
amount = st.number_input("Amount (₹) — leave 0 for an open-amount QR", min_value=0.0, value=0.0, step=1.0)
note = st.text_input("Payment Note", placeholder="Project Payment")

style = style_controls("upi")

generate = st.button("Generate UPI QR", type="primary", use_container_width=True)

if generate:
    if not upi.strip() or not name.strip():
        st.error("Please enter both UPI ID and Payee Name.")
        st.stop()
    if "@" not in upi:
        st.error("UPI ID looks invalid — it should look like name@bank.")
        st.stop()

    qr_data = f"upi://pay?pa={quote(upi)}&pn={quote(name)}&cu=INR"
    if amount > 0:
        qr_data += f"&am={amount}"
    if note:
        qr_data += f"&tn={quote(note)}"

    img = build_qr_image(
        qr_data,
        qr_color=style["qr_color"],
        bg_color=style["bg_color"],
        box_size=style["box_size"],
        border=style["border"],
        logo_file=style["logo"],
    )
    st.session_state["_upi_result"] = {"img": img, "data": qr_data}

if "_upi_result" in st.session_state:
    res = st.session_state["_upi_result"]
    custom_name = render_result(res["img"], "UPI", res["data"], "UPI_QR", "upi_name")

    if st.button("💾 Save to History", key="upi_save"):
        path = unique_path("UPI", custom_name)
        res["img"].save(path)
        add_history("UPI", res["data"], path, label=custom_name)
        st.toast("Saved to history!", icon="✅")
