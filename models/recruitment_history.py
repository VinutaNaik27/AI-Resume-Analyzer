from datetime import datetime
from database import db


class RecruitmentSession(db.Model):
    __tablename__ = "recruitment_session"

    id = db.Column(db.Integer, primary_key=True)

    recruiter_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("job_posting.id"),
        nullable=False
    )

    # Snapshot values are stored so old history remains understandable.
    job_title = db.Column(db.String(200), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    job_hash = db.Column(db.String(64), nullable=False, index=True)

    cutoff_score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    candidates = db.relationship(
        "CandidateResult",
        backref="recruitment_session",
        lazy=True,
        cascade="all, delete-orphan"
    )


class CandidateResult(db.Model):
    __tablename__ = "candidate_result"

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("recruitment_session.id"),
        nullable=False
    )

    candidate_name = db.Column(db.String(255), nullable=False)
    resume_hash = db.Column(db.String(64), nullable=False, index=True)
    job_hash = db.Column(db.String(64), nullable=False, index=True)

    match_score = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    matching_skills = db.Column(db.Text)
    missing_skills = db.Column(db.Text)
    summary = db.Column(db.Text)
    strengths = db.Column(db.Text)
    weaknesses = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
