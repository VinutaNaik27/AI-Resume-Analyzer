import os
import uuid
import json
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename

from config import Config
from database import db

from models.user import User
from models.analysis_history import AnalysisHistory
from models.job_posting import JobPosting
from models.recruitment_history import RecruitmentSession, CandidateResult

from services.file_hash import hash_file, hash_text
from services.resume_extractor import extract_resume_text
from services.section_chunker import create_semantic_chunks
from services.vector_store import store_resume_chunks
from services.resume_analyzer import analyze_resume


ALLOWED_EXTENSIONS = {"pdf", "docx"}

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

with app.app_context():
    db.create_all()


def allowed(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def get_dashboard_endpoint(role):
    return "recruiter_dashboard" if role == "recruiter" else "applicant_dashboard"


def require_role(role):
    
    return bool(session.get("user_id")) and session.get("role") == role


def role_required(role):
   
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
          
            if not session.get("user_id"):
                flash(f"Please login as a {role} to access this page.")
                return redirect(url_for("login", role=role))

            # Logged in with the wrong role: never allow cross-role access.
            if session.get("role") != role:
                flash("You are not allowed to access that page with your current role.")
                return redirect(url_for(get_dashboard_endpoint(session.get("role"))))

            # Make sure the session still belongs to a real user.
            user = db.session.get(User, session.get("user_id"))
            if not user or user.role != role:
                session.clear()
                flash("Your session is no longer valid. Please login again.")
                return redirect(url_for("login", role=role))

            return view(*args, **kwargs)
        return wrapped
    return decorator


def decode_history(history):
    return {
        "overall_score": history.match_score,
        "matching_skills": json.loads(history.matching_skills or "[]"),
        "missing_skills": json.loads(history.missing_skills or "[]"),
        "summary": history.summary or "",
        "strengths": json.loads(history.strengths or "[]"),
        "weaknesses": json.loads(history.weaknesses or "[]")
    }


def decode_candidate(candidate):
    return {
        "candidate_name": candidate.candidate_name,
        "score": candidate.match_score,
        "status": candidate.status,
        "matching_skills": json.loads(candidate.matching_skills or "[]"),
        "missing_skills": json.loads(candidate.missing_skills or "[]"),
        "summary": candidate.summary or "",
        "strengths": json.loads(candidate.strengths or "[]"),
        "weaknesses": json.loads(candidate.weaknesses or "[]")
    }


def save_upload(file):
    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4()}_{filename}"
    path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
    file.save(path)
    return filename, path



@app.route("/")
def index():
    if session.get("user_id") and session.get("role") in {"applicant", "recruiter"}:
        return redirect(url_for(get_dashboard_endpoint(session["role"])))
    return render_template("index.html")


@app.route("/register/<role>", methods=["GET", "POST"])
def register(role):
    if role not in ["applicant", "recruiter"]:
        return redirect(url_for("index"))

    if session.get("user_id"):
        return redirect(url_for(get_dashboard_endpoint(session.get("role", "applicant"))))

    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            flash("Email already registered.")
            return redirect(request.url)

        user = User(
            username=username,
            email=email,
            role=role
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please login.")
        return redirect(url_for("login", role=role))

    return render_template("register.html", role=role)


@app.route("/login/<role>", methods=["GET", "POST"])
def login(role):
    if role not in ["applicant", "recruiter"]:
        return redirect(url_for("index"))

    # Do not show another login flow while a user is already authenticated.
    if session.get("user_id") and session.get("role") in {"applicant", "recruiter"}:
        return redirect(url_for(get_dashboard_endpoint(session["role"])))

    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = User.query.filter_by(
            email=email,
            role=role
        ).first()

        if user and user.check_password(password):
            session.clear()
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role

            if role == "recruiter":
                return redirect(url_for("recruiter_dashboard"))
            return redirect(url_for("applicant_dashboard"))

        flash("Invalid email or password.")

    return render_template("login.html", role=role)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))




@app.route("/applicant/dashboard", methods=["GET", "POST"])
@role_required("applicant")
def applicant_dashboard():

    if request.method == "POST":
        job_description = request.form.get("job_description", "").strip()
        file = request.files.get("resume")

        if (
            not job_description
            or not file
            or not file.filename
            or not allowed(file.filename)
        ):
            flash("Enter a job description and upload a PDF/DOCX resume.")
            return redirect(request.url)

        filename, path = save_upload(file)

        resume_hash = hash_file(path)
        job_hash = hash_text(job_description)

        old = AnalysisHistory.query.filter_by(
            user_id=session["user_id"],
            resume_hash=resume_hash,
            job_hash=job_hash
        ).first()

        if old:
            return render_template(
                "results.html",
                applicant=True,
                analysis=decode_history(old),
                cached=True,
                cache_message=(
                    "This resume is already analyzed with this job description. "
                    "The saved result has been fetched from the database."
                )
            )

        try:
            resume_text = extract_resume_text(path)
            chunks = create_semantic_chunks(resume_text)

            if not chunks:
                raise ValueError("No meaningful text chunks could be created.")

            resume_id = str(uuid.uuid4())

            store_resume_chunks(
                resume_id=resume_id,
                candidate_name=session["username"],
                chunks=chunks
            )

            analysis = analyze_resume(
                resume_id=resume_id,
                job_description=job_description
            )

            history = AnalysisHistory(
                user_id=session["user_id"],
                resume_name=filename,
                resume_hash=resume_hash,
                job_hash=job_hash,
                job_description=job_description,
                match_score=float(analysis["overall_score"]),
                matching_skills=json.dumps(analysis["matching_skills"]),
                missing_skills=json.dumps(analysis["missing_skills"]),
                summary=analysis["summary"],
                strengths=json.dumps(analysis["strengths"]),
                weaknesses=json.dumps(analysis["weaknesses"])
            )

            db.session.add(history)
            db.session.commit()

            return render_template(
                "results.html",
                applicant=True,
                analysis=analysis,
                cached=False
            )

        except Exception as error:
            flash(f"Analysis error: {error}")
            return redirect(request.url)

    return render_template("applicant_dashboard.html")


@app.route("/applicant/history")
@role_required("applicant")
def applicant_history():

    history = AnalysisHistory.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        AnalysisHistory.created_at.desc()
    ).all()

    return render_template(
        "applicant_history.html",
        history=history
    )


@app.route("/applicant/history/<int:history_id>")
@role_required("applicant")
def applicant_history_details(history_id):

    row = AnalysisHistory.query.filter_by(
        id=history_id,
        user_id=session["user_id"]
    ).first_or_404()

    return render_template(
        "results.html",
        applicant=True,
        analysis=decode_history(row),
        cached=True,
        cache_message="This is a saved result from your analysis history."
    )


# -------------------- RECRUITER JOB POSTINGS --------------------

@app.route("/recruiter/dashboard")
@role_required("recruiter")
def recruiter_dashboard():

    jobs = JobPosting.query.filter_by(
        recruiter_id=session["user_id"],
        status="OPEN"
    ).order_by(
        JobPosting.created_at.desc()
    ).all()

    return render_template(
        "recruiter_dashboard.html",
        jobs=jobs
    )


@app.route("/recruiter/jobs")
@role_required("recruiter")
def job_postings():

    jobs = JobPosting.query.filter_by(
        recruiter_id=session["user_id"]
    ).order_by(
        JobPosting.created_at.desc()
    ).all()

    return render_template("job_postings.html", jobs=jobs)


@app.route("/recruiter/jobs/create", methods=["GET", "POST"])
@role_required("recruiter")
def create_job_posting():

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        company = request.form.get("company", "").strip()
        location = request.form.get("location", "").strip()
        employment_type = request.form.get("employment_type", "").strip()
        job_description = request.form.get(
            "job_description", ""
        ).strip()

        if not title or not company or not job_description:
            flash("Job title, company and job description are required.")
            return redirect(request.url)

        job = JobPosting(
            recruiter_id=session["user_id"],
            title=title,
            company=company,
            location=location,
            employment_type=employment_type,
            job_description=job_description,
            job_hash=hash_text(job_description),
            status="OPEN"
        )

        db.session.add(job)
        db.session.commit()

        flash("Job posting created successfully.")
        return redirect(
            url_for("analyze_job_candidates", job_id=job.id)
        )

    return render_template("create_job.html")


@app.route("/recruiter/jobs/<int:job_id>/toggle", methods=["POST"])
@role_required("recruiter")
def toggle_job_status(job_id):

    job = JobPosting.query.filter_by(
        id=job_id,
        recruiter_id=session["user_id"]
    ).first_or_404()

    job.status = "CLOSED" if job.status == "OPEN" else "OPEN"
    db.session.commit()

    flash(f"Job status changed to {job.status}.")
    return redirect(url_for("job_postings"))


# -------------------- RECRUITER ANALYSIS --------------------

@app.route(
    "/recruiter/jobs/<int:job_id>/analyze",
    methods=["GET", "POST"]
)
@role_required("recruiter")
def analyze_job_candidates(job_id):

    job = JobPosting.query.filter_by(
        id=job_id,
        recruiter_id=session["user_id"]
    ).first_or_404()

    if request.method == "POST":
        try:
            cutoff = float(request.form.get("cutoff_score", 60))
        except ValueError:
            cutoff = 60.0

        cutoff = max(0.0, min(100.0, cutoff))

        uploads = [
            file for file in request.files.getlist("resumes")
            if file and file.filename and allowed(file.filename)
        ]

        if not uploads:
            flash("Upload at least one PDF or DOCX resume.")
            return redirect(request.url)

        recruitment = RecruitmentSession(
            recruiter_id=session["user_id"],
            job_id=job.id,
            job_title=job.title,
            job_description=job.job_description,
            job_hash=job.job_hash,
            cutoff_score=cutoff
        )

        db.session.add(recruitment)
        db.session.commit()

        results = []

        for file in uploads:
            filename, path = save_upload(file)
            resume_hash = hash_file(path)
            candidate_name = os.path.splitext(filename)[0]

            # Look for an existing result for this recruiter + same resume + same JD.
            old = CandidateResult.query.join(
                RecruitmentSession
            ).filter(
                RecruitmentSession.recruiter_id == session["user_id"],
                CandidateResult.resume_hash == resume_hash,
                CandidateResult.job_hash == job.job_hash
            ).order_by(
                CandidateResult.created_at.desc()
            ).first()

            if old:
                result = decode_candidate(old)
                result["status"] = (
                    "SHORTLISTED"
                    if result["score"] >= cutoff
                    else "REJECTED"
                )
                result["cached"] = True

            else:
                try:
                    resume_text = extract_resume_text(path)
                    chunks = create_semantic_chunks(resume_text)

                    if not chunks:
                        raise ValueError(
                            "No meaningful text chunks could be created."
                        )

                    resume_id = str(uuid.uuid4())

                    store_resume_chunks(
                        resume_id=resume_id,
                        candidate_name=candidate_name,
                        chunks=chunks
                    )

                    analysis = analyze_resume(
                        resume_id=resume_id,
                        job_description=job.job_description
                    )

                    score = float(analysis["overall_score"])

                    result = {
                        "candidate_name": candidate_name,
                        "score": score,
                        "status": (
                            "SHORTLISTED"
                            if score >= cutoff
                            else "REJECTED"
                        ),
                        "matching_skills": analysis["matching_skills"],
                        "missing_skills": analysis["missing_skills"],
                        "summary": analysis["summary"],
                        "strengths": analysis["strengths"],
                        "weaknesses": analysis["weaknesses"],
                        "cached": False
                    }

                except Exception as error:
                    results.append({
                        "candidate_name": candidate_name,
                        "error": str(error)
                    })
                    continue

            # Store a result row for this recruitment session.
            candidate = CandidateResult(
                session_id=recruitment.id,
                candidate_name=result["candidate_name"],
                resume_hash=resume_hash,
                job_hash=job.job_hash,
                match_score=float(result["score"]),
                status=result["status"],
                matching_skills=json.dumps(
                    result["matching_skills"]
                ),
                missing_skills=json.dumps(
                    result["missing_skills"]
                ),
                summary=result["summary"],
                strengths=json.dumps(result["strengths"]),
                weaknesses=json.dumps(result["weaknesses"])
            )

            db.session.add(candidate)
            db.session.commit()

            results.append(result)

        results.sort(
            key=lambda item: item.get("score", -1),
            reverse=True
        )

        return render_template(
            "results.html",
            applicant=False,
            results=results,
            cutoff_score=cutoff,
            job=job
        )

    return render_template(
        "analyze_candidates.html",
        job=job
    )


# -------------------- RECRUITER HISTORY --------------------

@app.route("/recruiter/history")
@role_required("recruiter")
def recruiter_history():

    history = RecruitmentSession.query.filter_by(
        recruiter_id=session["user_id"]
    ).order_by(
        RecruitmentSession.created_at.desc()
    ).all()

    return render_template(
        "recruiter_history.html",
        history=history
    )


@app.route("/recruiter/history/<int:session_id>")
@role_required("recruiter")
def recruitment_details(session_id):

    recruitment = RecruitmentSession.query.filter_by(
        id=session_id,
        recruiter_id=session["user_id"]
    ).first_or_404()

    rows = CandidateResult.query.filter_by(
        session_id=recruitment.id
    ).order_by(
        CandidateResult.match_score.desc()
    ).all()

    candidates = [decode_candidate(row) for row in rows]

    return render_template(
        "recruitment_details.html",
        recruitment_session=recruitment,
        candidates=candidates
    )


if __name__ == "__main__":
    app.run(debug=True)
