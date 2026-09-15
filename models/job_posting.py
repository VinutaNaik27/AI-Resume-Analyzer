from datetime import datetime
from database import db


class JobPosting(db.Model):
    __tablename__ = "job_posting"

    id = db.Column(db.Integer, primary_key=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)

    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    employment_type = db.Column(db.String(100), nullable=True)

    job_description = db.Column(db.Text, nullable=False)
    job_hash = db.Column(db.String(64), nullable=False, index=True)

    status = db.Column(db.String(30), default="OPEN", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    recruitment_sessions = db.relationship(
        "RecruitmentSession",
        backref="job_posting",
        lazy=True
    )
