from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    resumes = db.Relationship("Resume", backref="user", lazy=True)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    extracted_text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    resume_id = db.Column(db.Integer, db.ForeignKey("resume.id"), nullable=False)

    job_role = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text, nullable=True)
    match_score = db.Column(db.Integer, nullable=True)
    strengths = db.Column(db.Text, nullable=True)
    missing_skills = db.Column(db.Text, nullable=True)
    weaknesses = db.Column(db.Text, nullable=True)
    suggestions = db.Column(db.Text, nullable=True)
    recommended_skills = db.Column(db.Text, nullable=True)