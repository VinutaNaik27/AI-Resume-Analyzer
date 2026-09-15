from flask import Flask, request, render_template, redirect
import fitz
from analyse_pdf import analyse_resume_gemini
import os
from flask_sqlalchemy import SQLAlchemy
import hashlib
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class ResumeAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_hash = db.Column(db.String(64), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    result = db.Column(db.Text, nullable=False)

def get_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def extract_text_from_resume(pdf_path: str):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        resume_file = request.files.get("resume")
        job_description = request.form.get("job_description")
        if resume_file and resume_file.filename.endswith(".pdf"):
            filename = resume_file.filename
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume_file.save(pdf_path)
            resume_content = extract_text_from_resume(pdf_path)
            resume_hash = get_hash(resume_content + job_description)
            existing = ResumeAnalysis.query.filter_by(
                resume_hash=resume_hash
            ).first()
            if existing:
                return render_template(
                    "index.html",
                    result=existing.result,
                    message="This resume was already analyzed. Showing previous result."
                )
            result = analyse_resume_gemini(resume_content, job_description)
            new_entry = ResumeAnalysis(
                resume_hash=resume_hash,
                job_description=job_description,
                result=result
            )
            db.session.add(new_entry)
            db.session.commit()

            return render_template(
                "index.html",
                result=result,
                message="Analysis completed successfully"
            )

    return render_template("index.html", result=None)
@app.route("/history")
def history():
    data = ResumeAnalysis.query.order_by(ResumeAnalysis.id.desc()).all()
    return render_template("history.html", data=data)

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    item = ResumeAnalysis.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect("/history")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
