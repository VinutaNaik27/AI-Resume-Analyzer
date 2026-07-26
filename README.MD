# AI Resume Analyzer

An AI-powered Resume Analyzer built with Flask and Google's Gemini API. The application allows users to upload a resume (PDF), compare it with a job description, and receive an AI-generated analysis including a match score, missing skills, improvement suggestions, and a concise summary.

---

## Features

- Upload PDF resumes
- Extract resume text automatically
- Compare resume against a job description using Gemini AI
- Generate:
  - Match Score
  - Missing Skills
  - Improvement Suggestions
  - Resume Summary
- Store analysis history in SQLite
- View previous analyses
- Delete unwanted history records
- Prevent duplicate analyses using resume hashing

---

## Tech Stack

- Python
- Flask
- Google Gemini API
- PyMuPDF (fitz)
- Flask-SQLAlchemy
- SQLite
- HTML
- Bootstrap 5
- JavaScript
- python-dotenv

---

## Project Structure

```
PythonProject3/
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
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Run the Application

```bash
python uploads/main.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## How It Works

1. Upload a PDF resume.
2. Enter the job description.
3. The application extracts text from the PDF.
4. Gemini AI compares the resume with the job description.
5. The system returns:
   - Match Score
   - Missing Skills
   - Suggestions
   - Summary
6. Results are stored in a SQLite database.
7. Users can view or delete previous analyses from the History page.

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Flask | Backend Framework |
| Gemini AI | Resume Analysis |
| PyMuPDF | PDF Text Extraction |
| SQLAlchemy | Database ORM |
| SQLite | Database |
| Bootstrap 5 | User Interface |
| HTML/CSS | Frontend |
| JavaScript | Dynamic UI |

---

## Future Improvements

- Support DOCX and TXT resume uploads
- Export analysis reports as PDF
- User authentication
- Resume keyword highlighting
- ATS score visualization
- Download analysis reports

---

## Author

**Vinuta Ishwar Naik**

AI & Machine Learning Enthusiast

---

## License

This project is created for educational and learning purposes.
