import streamlit as st
from database import add_history
from utils import build_qr_image, render_result, style_controls, inject_base_css, page_hero, unique_path

st.set_page_config(page_title="WiFi QR", page_icon="📶")
inject_base_css()
page_hero("📶 WiFi QR Generator", "Let guests join your WiFi with a single scan — no typing.")

ssid = st.text_input("WiFi Name (SSID)")
password = st.text_input("Password", type="password")
security = st.selectbox("Security", ["WPA/WPA2", "WEP", "None"])
hidden = st.checkbox("Hidden network")

style = style_controls("wifi")

generate = st.button("Generate WiFi QR", type="primary", use_container_width=True)

if generate:
    if not ssid.strip():
        st.error("Please enter the WiFi name.")
        st.stop()
    if security != "None" and not password:
        st.error("Please enter the WiFi password, or set Security to 'None'.")
        st.stop()

    sec_code = {"WPA/WPA2": "WPA", "WEP": "WEP", "None": "nopass"}[security]
    hidden_flag = "true" if hidden else "false"

    if security == "None":
        wifi_data = f"WIFI:T:nopass;S:{ssid};H:{hidden_flag};;"
    else:
        wifi_data = f"WIFI:T:{sec_code};S:{ssid};P:{password};H:{hidden_flag};;"

    img = build_qr_image(
        wifi_data,
        qr_color=style["qr_color"],
        bg_color=style["bg_color"],
        box_size=style["box_size"],
        border=style["border"],
        logo_file=style["logo"],
    )
    st.session_state["_wifi_result"] = {"img": img, "data": wifi_data}

if "_wifi_result" in st.session_state:
    res = st.session_state["_wifi_result"]
    custom_name = render_result(res["img"], "WiFi", res["data"], "WiFi_QR", "wifi_name")

    if st.button("💾 Save to History", key="wifi_save"):
        path = unique_path("WiFi", custom_name)
        res["img"].save(path)
        add_history("WiFi", res["data"], path, label=custom_name)
        st.toast("Saved to history!", icon="✅")
