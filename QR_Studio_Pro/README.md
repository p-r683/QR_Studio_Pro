# 📱 QR Studio Pro

Generate, customize, scan, and track QR codes — all in one Streamlit app.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The sidebar will list every page automatically (Streamlit's native multipage
support, driven by the numbered files in `pages/`).

## Pages

| Page | What it does |
|---|---|
| 🌐 Website | QR for any URL |
| 📶 WiFi | Join-WiFi QR (WPA/WEP/open, hidden network support) |
| 📧 Email | Pre-filled `mailto:` QR |
| 📞 Phone & WhatsApp | Call / SMS / WhatsApp-chat QR |
| 💳 UPI Payment | Google Pay / PhonePe / Paytm / BHIM payment QR |
| 📇 Contact (vCard) | Full digital business card QR |
| 📷 Scanner | Decode a QR from an upload or your **browser** camera |
| 🗂 History | Search, filter, favorite, download-again, delete |
| 📊 Analytics | Usage stats by type and over time |

## What changed from the original prototype

**Bugs fixed**
- The "File Name" box used to render *after* the button click and *after*
  the file was already saved — renaming did nothing until you clicked
  Generate again. Generation and saving are now separate steps, so the name
  field always applies.
- Every generated QR overwrote `generated/MyQR.png`. Files now get a unique,
  timestamped name, so nothing is lost.
- `database.py` kept one global SQLite connection/cursor for the whole app.
  Under Streamlit's multi-threaded reruns this can throw or silently
  corrupt writes. Every DB call now opens its own short-lived connection
  (WAL mode) instead.
- Logo embedding pasted logos as opaque rectangles, hiding QR modules
  underneath transparent PNG corners. Logos are now composited with their
  alpha channel and a white safety backdrop so the code stays scannable.
- The webcam scanner used `cv2.VideoCapture(0)`, which opens a camera **on
  the server**, not the visitor's device — it silently does nothing on a
  real deployment. It's replaced with `st.camera_input`, which uses the
  visitor's own browser camera and works when hosted anywhere.
- "Open Link" used to call `webbrowser.open()` server-side (same class of
  bug). It's now a proper `st.link_button` that opens in the visitor's
  browser.
- Pages lived as loose top-level files, so Streamlit's automatic multipage
  sidebar never found them. They now live under `pages/` with numeric
  prefixes for a stable, deliberate order.

**New**
- Home dashboard with live counts pulled from the database.
- 📇 Contact (vCard) QR generator.
- 📊 Analytics page (by-type and by-day charts).
- Favorites and labels in History, plus type/search filters and a
  "delete all" safety hatch.
- Shared `utils.py` so every generator page has identical, tested QR/logo
  handling instead of eight copies of similar-but-slightly-different code.
