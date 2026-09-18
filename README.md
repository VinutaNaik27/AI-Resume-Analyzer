# AI Resume Analyzer

An AI-powered web application that analyzes resumes against job descriptions using **Retrieval-Augmented Generation (RAG)**, semantic embeddings, and Google Gemini.

The system helps **applicants** understand how well their resume matches a job description and helps **recruiters** analyze and compare multiple candidates for a job role.

---

## 📌 Project Overview

The **AI Resume Analyzer** is a Flask-based web application designed to simplify the resume screening and job-matching process.

Instead of relying only on traditional keyword matching, the application uses **semantic search and RAG** to understand the meaning and context of information present in resumes and job descriptions.

The application supports two types of users:

* 👤 **Applicant**
* 🧑‍💼 **Recruiter**

---

## ✨ Features

### 👤 Applicant Features

* Applicant registration and login
* Secure password-based authentication
* Upload resume in **PDF** or **DOCX** format
* Enter a job description
* AI-powered resume analysis
* Resume-to-job match score
* Matching skills identification
* Missing skills identification
* Strengths and weaknesses analysis
* AI-generated resume summary
* Analysis history
* Previous analysis retrieval
* Duplicate analysis detection

---

### 🧑‍💼 Recruiter Features

* Recruiter registration and login
* Recruiter dashboard
* Create job postings
* Add job title, company, location, employment type, and job description
* Upload multiple candidate resumes
* Analyze multiple candidates against a job
* Generate AI-based candidate match scores
* Identify matching skills
* Identify missing skills
* View candidate strengths and weaknesses
* View candidate summaries
* Set a cutoff score
* Review candidates based on the cutoff
* Maintain recruitment history
* View previous recruitment sessions

---

## 🤖 AI and RAG Features

The application uses a **Retrieval-Augmented Generation (RAG)** approach for resume analysis.

The basic workflow is:

```text
Resume
   ↓
Text Extraction
   ↓
Section Detection
   ↓
Semantic Chunking
   ↓
Gemini Embeddings
   ↓
ChromaDB
   ↓
Semantic Retrieval
   ↓
Relevant Resume Chunks
   ↓
Google Gemini
   ↓
Resume Analysis
```

The system retrieves the most relevant parts of the resume before sending the information to the AI model.

This allows the model to focus on the sections of the resume that are most relevant to the job description.

---

## 🧠 Why RAG?

Traditional resume screening systems often depend heavily on exact keyword matching.

For example:

**Job Description:**

```text
Experience in developing predictive models.
```

**Resume:**

```text
Developed machine learning models for classification and prediction.
```

A simple keyword-based system may not fully understand that these two statements are related.

With semantic embeddings, the application can identify content based on **meaning and context**, not just exact words.

RAG helps the system:

* Retrieve relevant resume information
* Reduce unnecessary information sent to the AI model
* Improve contextual understanding
* Provide analysis based on actual resume content
* Compare resumes and job descriptions more intelligently

---

# 🛠️ Technology Stack

| Category              | Technology        |
| --------------------- | ----------------- |
| Programming Language  | Python            |
| Backend               | Flask             |
| Frontend              | HTML, CSS, Jinja2 |
| Database              | SQLite            |
| ORM                   | Flask-SQLAlchemy  |
| AI Model              | Google Gemini     |
| Embeddings            | Gemini Embeddings |
| Vector Database       | ChromaDB          |
| Text Processing       | LangChain         |
| PDF Processing        | PyMuPDF           |
| DOCX Processing       | python-docx       |
| Authentication        | Flask Sessions    |
| Password Security     | Werkzeug          |
| Environment Variables | python-dotenv     |

---

# 📂 Project Structure

```text
AI-Resume-Analyzer/
│
├── app.py
├── config.py
├── database.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── job_posting.py
│   ├── analysis_history.py
│   └── recruitment_history.py
│
├── services/
│   ├── embedding_service.py
│   ├── resume_analyzer.py
│   ├── resume_extractor.py
│   ├── section_chunker.py
│   ├── vector_store.py
│   └── email_service.py
│
├── utils/
│   ├── hash_utils.py
│   └── timezone.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── applicant_dashboard.html
│   ├── recruiter_dashboard.html
│   ├── create_job.html
│   ├── analyze_candidates.html
│   ├── results.html
│   ├── history.html
│   ├── recruiter_history.html
│   └── recruitment_details.html
│
├── static/
│   └── style.css
│
├── uploads/
│   └── resumes/
│
├── chroma_db/
│
└── instance/
    └── resume_analyzer.db
```

---

# 🔄 Application Workflow

## Applicant Workflow

```text
Applicant Registration
        ↓
Applicant Login
        ↓
Upload Resume
        ↓
Enter Job Description
        ↓
Extract Resume Text
        ↓
Create Resume Chunks
        ↓
Generate Embeddings
        ↓
Store in ChromaDB
        ↓
Retrieve Relevant Chunks
        ↓
Google Gemini Analysis
        ↓
Display Results
        ↓
Save Analysis History
```

---

## Recruiter Workflow

```text
Recruiter Registration
        ↓
Recruiter Login
        ↓
Create Job Posting
        ↓
Enter Job Description
        ↓
Upload Multiple Resumes
        ↓
Process Candidate Resumes
        ↓
Generate Embeddings
        ↓
Semantic Retrieval
        ↓
Google Gemini Analysis
        ↓
Generate Candidate Scores
        ↓
Apply Cutoff Score
        ↓
Review Candidate Results
        ↓
Save Recruitment History
```

---

# 📄 Resume Processing

The application supports the following resume formats:

```text
PDF
DOCX
```

### PDF

PDF resume text is extracted using:

```text
PyMuPDF
```

### DOCX

DOCX resume text is extracted using:

```text
python-docx
```

After extracting the text, the application processes the content and identifies different resume sections.

Common sections include:

* Summary
* Profile
* Objective
* Skills
* Technical Skills
* Experience
* Internship
* Projects
* Education
* Certifications
* Achievements

---

# ✂️ Semantic Chunking

Large resume text is divided into smaller chunks before generating embeddings.

The application uses a recursive text splitter.

Example configuration:

```python
chunk_size = 800
chunk_overlap = 100
```

### Why chunking?

A complete resume can contain a large amount of information.

Instead of embedding the entire resume as one large piece, it is divided into smaller meaningful sections.

For example:

```text
Resume
│
├── Summary
├── Skills
├── Experience
├── Projects
├── Education
└── Certifications
```

Each chunk can then be searched independently.

### Chunk Metadata

Each chunk can contain information such as:

```text
resume_id
candidate_name
section
content
embedding
```

This allows the application to identify where retrieved information came from.

---

# 🔎 Semantic Search

After resume chunks are stored in ChromaDB, the application performs semantic retrieval.

The job description is used to identify the most relevant resume chunks.

For example:

```text
Job Requirement:
Python + Machine Learning + SQL
```

The system searches the vector database for resume sections that are semantically related to these requirements.

The retrieved chunks are then provided to the Gemini model for analysis.

---

# 🗄️ ChromaDB

The application uses **ChromaDB** as the vector database.

ChromaDB stores:

* Resume chunks
* Embeddings
* Resume IDs
* Candidate information
* Section metadata

Example:

```text
Resume Chunk
     ↓
Embedding
     ↓
ChromaDB
     ↓
Semantic Search
     ↓
Relevant Resume Content
```

The local vector database is stored in:

```text
chroma_db/
```

---

# 🤖 AI Analysis

Google Gemini is used to analyze the retrieved resume content against the job description.

The analysis can include:

* Overall match score
* Matching skills
* Missing skills
* Strengths
* Weaknesses
* Summary

Example response:

```json
{
    "overall_score": 82.5,
    "matching_skills": [
        "Python",
        "Machine Learning",
        "SQL"
    ],
    "missing_skills": [
        "Docker",
        "AWS"
    ],
    "summary": "The candidate has a strong foundation in Python and machine learning and matches several core requirements of the role.",
    "strengths": [
        "Strong Python knowledge",
        "Relevant machine learning projects"
    ],
    "weaknesses": [
        "Limited cloud experience"
    ]
}
```

---

# 🔐 Authentication

The application provides separate authentication for:

```text
Applicant
Recruiter
```

User passwords are not stored directly.

Instead, passwords are securely hashed using **Werkzeug password hashing**.

The application also uses Flask sessions to maintain logged-in users.

Role-based access prevents applicants from accessing recruiter-specific functionality.

---

# ♻️ Duplicate Analysis Detection

The application uses hashing to avoid unnecessary repeated AI analysis.

Hashes can be generated for:

```text
Resume
Job Description
```

The application can check whether the same resume has already been analyzed for the same job description.

Conceptually:

```text
Resume Hash
     +
Job Description Hash
     ↓
Check Database
     ↓
Already Exists?
   /       \
 Yes        No
 ↓           ↓
Reuse       Analyze
Result      Using AI
```

This helps reduce unnecessary API requests and saves processing time.

---

# 🗃️ Database Models

The application uses **SQLite** with **Flask-SQLAlchemy**.

## User

Stores user information such as:

* User ID
* Name
* Email
* Password hash
* Role

---

## JobPosting

Stores recruiter job information such as:

* Job ID
* Recruiter ID
* Job title
* Company
* Location
* Employment type
* Job description
* Job hash
* Job status

---

## AnalysisHistory

Stores applicant resume analysis information.

It can contain:

* Resume information
* Job description
* Match score
* Matching skills
* Missing skills
* Strengths
* Weaknesses
* Summary
* Analysis timestamp

---

## RecruitmentSession

Stores information about a recruiter's candidate analysis session.

It can contain:

* Recruiter
* Job
* Job title
* Job description
* Cutoff score
* Session information

---

## CandidateResult

Stores individual candidate results for a recruitment session.

It can contain:

* Candidate information
* Resume information
* Match score
* Matching skills
* Missing skills
* Strengths
* Weaknesses
* Summary
* Selection status

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/VinutaNaik27/AI-Resume-Analyzer.git
```

Move into the project directory:

```bash
cd AI-Resume-Analyzer
```

---

## 2. Create a Virtual Environment

For Windows:

```bash
python -m venv venv
```

Activate the environment:

```bash
venv\Scripts\activate
```

For PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the root directory.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_secret_key
```

### GEMINI_API_KEY

This is the API key used to access Google Gemini services.

### SECRET_KEY

The Flask secret key is used for securely signing session-related data.

For example:

```env
SECRET_KEY=my-secure-secret-key
```

**Do not publish your actual API key or secret key on GitHub.**

Add `.env` to `.gitignore`:

```text
.env
```

---

# ▶️ Running the Application

After activating the virtual environment, run:

```bash
python app.py
```

The Flask application will normally be available at:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

---

# 👤 Applicant Usage

1. Open the application.
2. Select **Applicant**.
3. Register an account.
4. Log in.
5. Upload a PDF or DOCX resume.
6. Enter the job description.
7. Start the analysis.
8. Wait for the AI analysis.
9. View the resume match score.
10. Review matching and missing skills.
11. Read the strengths, weaknesses, and summary.
12. Access previous analyses through the history section.

---

# 🧑‍💼 Recruiter Usage

1. Open the application.
2. Select **Recruiter**.
3. Register or log in.
4. Open the recruiter dashboard.
5. Create a job posting.
6. Enter the job description.
7. Upload multiple candidate resumes.
8. Start candidate analysis.
9. View candidate match scores.
10. Review matching and missing skills.
11. Set a cutoff score.
12. Review candidates based on the score.
13. View recruitment history.

---

# 📊 Example Matching

Suppose a job description requires:

```text
Python
Machine Learning
SQL
Flask
Git
```

A candidate's resume contains:

```text
Python
Machine Learning
SQL
Flask
```

The system may identify:

```text
Matching Skills:
Python
Machine Learning
SQL
Flask

Missing Skills:
Git
```

The final score is generated by the AI based on the retrieved resume information and job requirements.

---

# 🔒 Security Considerations

The project includes basic security practices such as:

* Password hashing
* Session-based authentication
* Role-based access
* Secure filename handling
* Environment variables for API keys
* Protected recruiter routes

For production deployment, additional security improvements are recommended:

* CSRF protection
* HTTPS
* Stronger session configuration
* File-size restrictions
* File-content validation
* Production database
* Rate limiting
* Secure deployment configuration

---

# ⚠️ Important Notes

### Gemini API

The application depends on Google Gemini APIs.

API model availability, quotas, rate limits, and pricing may change.

If a configured model is unavailable, the model name in the relevant service file may need to be updated.

---

### Resume Privacy

Uploaded resumes may contain personal information.

Do not upload real candidate resumes to a public GitHub repository.

The following folders should generally not contain publicly committed personal data:

```text
uploads/
chroma_db/
instance/
```

---

### `.env`

Never commit:

```text
.env
```

to GitHub.

Your API key should remain private.

---

# 🚀 Future Enhancements

Possible improvements include:

* Candidate ranking
* Advanced skill normalization
* OCR support for scanned resumes
* More document formats
* Better resume section detection
* Applicant AI doubt assistant
* Email notifications
* Advanced recruiter analytics
* Candidate filtering
* Production PostgreSQL database
* Cloud deployment
* Automated testing
* Improved AI prompt evaluation
* Resume recommendation system
* Job recommendation based on resume
* Skill-gap learning recommendations

---


Then they can be displayed in the README using:

```markdown
![Home Page](screenshots/home.png)
```

---

# 👥 Team Members

This project was developed as a **group project**.



# 🎓 Project Purpose

This project was developed as an academic/group project to demonstrate the practical application of:

* Python
* Flask
* Machine Learning concepts
* Generative AI
* RAG
* Semantic Search
* Vector Databases
* Embeddings
* Natural Language Processing
* Database Management
* Web Application Development

The project demonstrates how AI can be integrated into a real-world recruitment and resume-screening workflow.

---

# ⚖️ Disclaimer

The AI-generated match scores, recommendations, and candidate insights are intended to assist users in resume analysis and recruitment workflows.

They should **not be used as the sole basis for making employment decisions**. Human review and judgment should always be considered.

---

## ⭐ Acknowledgement

This project was developed collaboratively by the team as part of our learning and practical implementation of AI-powered application development.

## 👥 Team Members

This project was developed as a **group project** by:

* **Vasant Kumar**
* **Vinod A**
* **Vinuta Naik**
* **Vishalakshi N R**
