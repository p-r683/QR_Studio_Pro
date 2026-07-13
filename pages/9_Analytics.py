import pandas as pd
import streamlit as st
from database import get_stats
from utils import inject_base_css, page_hero

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")
inject_base_css()
page_hero("📊 Analytics", "Understand how you're using QR Studio Pro.")

stats = get_stats()

if stats["total"] == 0:
    st.info("No data yet — generate a few QR codes first.")
    st.stop()

s1, s2, s3 = st.columns(3)
with s1:
    st.markdown(
        f'<div class="stat-box"><div class="num">{stats["total"]}</div>'
        f'<div class="label">Total QR Codes</div></div>',
        unsafe_allow_html=True,
    )
with s2:
    st.markdown(
        f'<div class="stat-box"><div class="num">{len(stats["by_type"])}</div>'
        f'<div class="label">Distinct Types</div></div>',
        unsafe_allow_html=True,
    )
with s3:
    st.markdown(
        f'<div class="stat-box"><div class="num">{stats["favorites"]}</div>'
        f'<div class="label">Favorites</div></div>',
        unsafe_allow_html=True,
    )

st.write("")

col1, col2 = st.columns(2)

with col1:
    st.subheader("By Type")
    type_df = pd.DataFrame(stats["by_type"]).rename(columns={"qr_type": "Type", "c": "Count"})
    type_df = type_df.set_index("Type")
    st.bar_chart(type_df)

with col2:
    st.subheader("Over Time")
    day_df = pd.DataFrame(stats["by_day"]).rename(columns={"day": "Date", "c": "Count"})
    day_df = day_df.set_index("Date")
    st.line_chart(day_df)

st.divider()
st.subheader("Breakdown")
st.dataframe(
    pd.DataFrame(stats["by_type"]).rename(columns={"qr_type": "Type", "c": "Count"}),
    use_container_width=True,
    hide_index=True,
)
