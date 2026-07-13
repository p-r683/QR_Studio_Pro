# 📱 QR Studio Pro

Generate, customize, scan, and track QR codes — all in one Streamlit app.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The sidebar will list every page automatically.

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

**New**
- Home dashboard with live counts pulled from the database.
- 📇 Contact (vCard) QR generator.
- 📊 Analytics page (by-type and by-day charts).
- Favorites and labels in History, plus type/search filters and a
  "delete all" safety hatch.
- Shared `utils.py` so every generator page has identical, tested QR/logo
  handling instead of eight copies of similar-but-slightly-different code.
