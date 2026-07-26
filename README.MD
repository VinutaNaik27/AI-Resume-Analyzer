# 🤖 AI Resume Analyzer

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge&logo=flask)
![Gemini AI](https://img.shields.io/badge/Google-Gemini%20AI-4285F4?style=for-the-badge&logo=google)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)
![License](https://img.shields.io/badge/License-Educational-success?style=for-the-badge)

</p>

---

## 📖 About the Project

**AI Resume Analyzer** is an intelligent web application built using **Flask** and **Google Gemini AI**.

The application allows users to upload a **PDF resume**, compare it with a **Job Description**, and receive an AI-powered analysis including:

- 🎯 Match Score
- 🛠 Missing Skills
- 💡 Improvement Suggestions
- 📝 Resume Summary

It also stores previous analyses in a **SQLite database** and provides a dedicated **History Page**.

---

# ✨ Features

✅ Upload PDF Resume

✅ Extract Resume Text Automatically

✅ AI Resume Analysis using Google Gemini

✅ ATS-style Resume Evaluation

✅ Match Score Generation

✅ Missing Skills Identification

✅ Improvement Suggestions

✅ Resume Summary

✅ Analysis History

✅ Delete Previous Analyses

✅ Duplicate Resume Detection using Hashing

---

# 🛠 Tech Stack

| Technology | Usage |
|------------|-------|
| 🐍 Python | Backend Programming |
| 🌐 Flask | Web Framework |
| 🤖 Google Gemini AI | Resume Analysis |
| 📄 PyMuPDF | PDF Text Extraction |
| 🗄 SQLite | Database |
| 🔥 SQLAlchemy | ORM |
| 🎨 Bootstrap 5 | UI Design |
| 💻 HTML/CSS | Frontend |
| ⚡ JavaScript | Dynamic Content |
| 🔑 python-dotenv | Environment Variables |

---

# 📂 Project Structure

```text
AI-Resume-Analyzer/
│
├── uploads/
│   ├── main.py
│   ├── analyse_pdf.py
│   ├── parser.py
│   ├── templates/
│   │   ├── index.html
│   │   └── history.html
│   └── uploads/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/VinutaNaik27/AI-Resume-Analyzer.git

cd AI-Resume-Analyzer
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

---

### 3️⃣ Activate Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Configure Environment Variables

Create a file named **`.env`**

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

# ▶️ Run the Application

```bash
python uploads/main.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

# ⚙️ How It Works

```text
Upload Resume
        │
        ▼
Extract Text from PDF
        │
        ▼
Paste Job Description
        │
        ▼
Google Gemini AI
        │
        ▼
Resume Analysis
        │
        ▼
Match Score
Missing Skills
Suggestions
Summary
        │
        ▼
Store Result in SQLite
```

---

# 🎯 Output Includes

📊 Match Score

❌ Missing Skills

💡 Improvement Suggestions

📝 Resume Summary

📚 Analysis History

🗑 Delete Previous Records

---

# 📌 Future Improvements

- 📄 DOCX Resume Support
- 🖼 Image Resume OCR
- 📥 Export Analysis as PDF
- 👤 User Authentication
- 📈 ATS Score Visualization
- 📊 Resume Analytics Dashboard
- 🌙 Dark Mode
- ☁ Cloud Deployment

---

# 📷 Screenshots

### 🏠 Home Page

><img src="C:\Users\Vinutha\PycharmProjects\PythonProject3\screenshots\home.png">

---

### 📊 Analysis Result

> <img src="{{ result}}" alt="result Page" width="700">

---

### 📜 History Page

><img src="{{ history }}" alt="history Page" width="700">

---

# 👨‍💻 Author

## **Vinuta Ishwar Naik**

🎓 AI & Machine Learning Enthusiast

💻 Python Developer

🚀 Passionate about AI, Machine Learning, and Generative AI

---

# ⭐ If you like this project...

Give this repository a ⭐ on GitHub!

---

# 📄 License

This project is developed for **educational and learning purposes**.
