import os
import streamlit as st
import pandas as pd
from database import get_history, delete_record, delete_all, toggle_favorite
from utils import inject_base_css, page_hero

st.set_page_config(page_title="QR History", page_icon="🗂", layout="wide")
inject_base_css()
page_hero("🗂 QR History", "Every QR code you've generated, in one searchable place.")

records = get_history()

if len(records) == 0:
    st.info("No QR codes generated yet. Head to a generator page and create one!")
    st.stop()

df = pd.DataFrame(records)

col_search, col_type, col_fav = st.columns([2, 1, 1])

with col_search:
    search = st.text_input("🔍 Search by content or label")

with col_type:
    types = ["All"] + sorted(df["qr_type"].unique().tolist())
    type_filter = st.selectbox("Type", types)

with col_fav:
    fav_only = st.checkbox("⭐ Favorites only")

filtered = df.copy()

if search:
    mask = filtered["data"].str.contains(search, case=False, na=False) | \
           filtered["label"].fillna("").str.contains(search, case=False, na=False)
    filtered = filtered[mask]

if type_filter != "All":
    filtered = filtered[filtered["qr_type"] == type_filter]

if fav_only:
    filtered = filtered[filtered["is_favorite"] == 1]

st.caption(f"Showing {len(filtered)} of {len(df)} QR codes")

st.dataframe(
    filtered[["id", "qr_type", "label", "created_at", "is_favorite"]].rename(
        columns={
            "id": "ID", "qr_type": "Type", "label": "Label",
            "created_at": "Created", "is_favorite": "Favorite",
        }
    ),
    use_container_width=True,
    hide_index=True,
)

st.divider()
st.subheader("Manage")

for _, row in filtered.iterrows():
    star = "⭐" if row["is_favorite"] else "☆"
    with st.expander(f"{star} {row['qr_type']} — {row['label'] or 'untitled'} — {row['created_at']}"):
        c1, c2 = st.columns([1, 2])

        with c1:
            if row["file_name"] and os.path.exists(row["file_name"]):
                st.image(row["file_name"], width=180)
            else:
                st.caption("Image file not found on disk.")

        with c2:
            st.write("**Payload:**")
            st.code(row["data"])

            b1, b2, b3 = st.columns(3)
            with b1:
                if row["file_name"] and os.path.exists(row["file_name"]):
                    with open(row["file_name"], "rb") as f:
                        st.download_button(
                            "📥 Download",
                            data=f.read(),
                            file_name=os.path.basename(row["file_name"]),
                            mime="image/png",
                            key=f"dl_{row['id']}",
                        )
            with b2:
                fav_label = "☆ Unfavorite" if row["is_favorite"] else "⭐ Favorite"
                if st.button(fav_label, key=f"fav_{row['id']}"):
                    toggle_favorite(row["id"])
                    st.rerun()
            with b3:
                if st.button("🗑 Delete", key=f"del_{row['id']}"):
                    delete_record(row["id"])
                    st.toast("Deleted", icon="🗑")
                    st.rerun()

st.divider()
with st.expander("⚠️ Danger zone"):
    st.warning("This permanently deletes every history record (image files on disk are kept).")
    if st.button("Delete ALL history"):
        delete_all()
        st.rerun()
