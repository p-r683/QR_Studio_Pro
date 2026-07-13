# 📱 QR Studio Pro
<p align="center">
  <link="https://qrstudiopro-9oxbmqsiednmrtiqyhxhlb.streamlit.app/Website">
</p>

<p align="center">
  <b>A modern multipurpose QR Code Generator, Scanner, and Manager built with Streamlit.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg">
  <img src="https://img.shields.io/badge/Streamlit-Latest-red.svg">
  <img src="https://img.shields.io/badge/OpenCV-4.x-green.svg">
  <img src="https://img.shields.io/badge/SQLite-Database-orange.svg">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg">
</p>

---

# 📖 Overview

QR Studio Pro is a feature-rich Streamlit application that enables users to generate, customize, scan, organize, and analyze QR codes from a single dashboard.

The application supports multiple QR code formats including Website URLs, WiFi credentials, Email, Phone, SMS, WhatsApp, UPI Payment, and Digital Contact Cards (vCard).

Unlike basic QR generators, QR Studio Pro also provides:

- 📊 Analytics Dashboard
- 🗂 QR History Management
- ❤️ Favorites
- 🎨 QR Customization
- 🖼 Logo Embedding
- 📷 QR Scanner
- 💾 Local SQLite Database

---

# ✨ Features

## 🌐 QR Code Generators

- Website QR
- WiFi QR
- Email QR
- Phone QR
- SMS QR
- WhatsApp QR
- UPI Payment QR
- Contact (vCard) QR

---

## 🎨 Customization

- Custom QR Colors
- Background Colors
- Adjustable Border
- QR Version Selection
- Logo Embedding
- High Resolution PNG Download

---

## 📷 QR Scanner

- Scan QR from uploaded images
- Scan QR using webcam
- Detect URLs automatically
- Open detected links directly

---

## 🗂 History

- Save generated QR Codes
- Search History
- Label QR Codes
- Favorite QR Codes
- Delete Individual Records
- Delete All Records

---

## 📊 Analytics

- Total QR Codes Generated
- Most Used QR Type
- Favorites Count
- QR Usage by Type
- QR Usage by Date

---

# 🖥 Application Pages

| Page | Description |
|------|-------------|
| 🏠 Home | Dashboard with statistics |
| 🌐 Website | Generate QR from URLs |
| 📶 WiFi | WiFi QR Generator |
| 📧 Email | Pre-filled Email QR |
| 📞 Phone/SMS/WhatsApp | Communication QR Codes |
| 💳 UPI Payment | Payment QR |
| 📇 Contact | Digital Business Card |
| 📷 Scanner | QR Code Scanner |
| 🗂 History | Saved QR Codes |
| 📊 Analytics | Usage Statistics |

---

# 📂 Project Structure

```
QR-Studio-Pro/
│
├── app.py
├── database.py
├── utils.py
├── history.db
├── requirements.txt
├── README.md
├── .gitignore
│
├── pages/
│   ├── 1_Website.py
│   ├── 2_WiFi.py
│   ├── 3_Email.py
│   ├── 4_Phone_and_WhatsApp.py
│   ├── 5_UPI_Payment.py
│   ├── 6_Contact_vCard.py
│   ├── 7_Scanner.py
│   ├── 8_History.py
│   └── 9_Analytics.py
│
└── .streamlit/
    └── config.toml
```

---

# ⚙ Technologies Used

- Python
- Streamlit
- SQLite
- OpenCV
- Pillow
- NumPy
- Pandas
- QRCode Library

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/QR-Studio-Pro.git

cd QR-Studio-Pro
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---



# 📊 Database

QR Studio Pro uses **SQLite** for storing:

- QR Type
- QR Data
- File Name
- Labels
- Favorites
- Date & Time

---

# 🎯 Future Improvements

- PDF QR Generator
- Social Media QR Codes
- Calendar Event QR
- Bulk QR Generator
- CSV Import
- QR Templates
- User Authentication
- Cloud Storage
- Dark/Light Themes
- Export Analytics

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository

2. Create a new branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Added new feature"
```

4. Push the branch

```bash
git push origin feature-name
```

5. Open a Pull Request

# 👨‍💻 Developer

**Pranshu Verma**

B.Tech CSE (Data Science)

AI | Machine Learning | Python | Streamlit


---

## ⭐ Support

If you like this project, please consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates future development.

---

<p align="center">
Made with ❤️ using Python & Streamlit
</p>
