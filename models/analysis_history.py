from datetime import datetime
from database import db

class AnalysisHistory(db.Model):
    __tablename__ = "analysis_history"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    resume_name = db.Column(db.String(255), nullable=False)
    resume_hash = db.Column(db.String(64), nullable=False, index=True)
    job_hash = db.Column(db.String(64), nullable=False, index=True)
    job_description = db.Column(db.Text, nullable=False)
    match_score = db.Column(db.Float, nullable=False)
    matching_skills = db.Column(db.Text)
    missing_skills = db.Column(db.Text)
    summary = db.Column(db.Text)
    strengths = db.Column(db.Text)
    weaknesses = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("user_id", "resume_hash", "job_hash",
                            name="unique_applicant_resume_job"),
    )
