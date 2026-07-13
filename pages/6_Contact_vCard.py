import streamlit as st
from database import add_history
from utils import build_qr_image, render_result, style_controls, inject_base_css, page_hero, unique_path

st.set_page_config(page_title="Contact QR", page_icon="📇")
inject_base_css()
page_hero("📇 Contact (vCard) QR Generator", "Share a full digital business card in one scan.")

col1, col2 = st.columns(2)
with col1:
    first_name = st.text_input("First Name")
    org = st.text_input("Company / Organization")
    phone = st.text_input("Phone Number", placeholder="+919876543210")
    website = st.text_input("Website", placeholder="https://example.com")

with col2:
    last_name = st.text_input("Last Name")
    title = st.text_input("Job Title")
    email = st.text_input("Email", placeholder="you@example.com")
    address = st.text_input("Address")

style = style_controls("vcard")

generate = st.button("Generate Contact QR", type="primary", use_container_width=True)

if generate:
    if not first_name.strip() and not last_name.strip():
        st.error("Please enter at least a first or last name.")
        st.stop()

    vcard_lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:{last_name};{first_name};;;",
        f"FN:{first_name} {last_name}".strip(),
    ]
    if org:
        vcard_lines.append(f"ORG:{org}")
    if title:
        vcard_lines.append(f"TITLE:{title}")
    if phone:
        vcard_lines.append(f"TEL;TYPE=CELL:{phone}")
    if email:
        vcard_lines.append(f"EMAIL:{email}")
    if website:
        vcard_lines.append(f"URL:{website}")
    if address:
        vcard_lines.append(f"ADR:;;{address};;;;")
    vcard_lines.append("END:VCARD")

    qr_data = "\n".join(vcard_lines)

    img = build_qr_image(
        qr_data,
        qr_color=style["qr_color"],
        bg_color=style["bg_color"],
        box_size=style["box_size"],
        border=style["border"],
        logo_file=style["logo"],
    )
    st.session_state["_vcard_result"] = {"img": img, "data": qr_data}

if "_vcard_result" in st.session_state:
    res = st.session_state["_vcard_result"]
    custom_name = render_result(res["img"], "Contact", res["data"], "Contact_QR", "vcard_name")

    if st.button("💾 Save to History", key="vcard_save"):
        path = unique_path("Contact", custom_name)
        res["img"].save(path)
        add_history("Contact", res["data"], path, label=custom_name)
        st.toast("Saved to history!", icon="✅")
