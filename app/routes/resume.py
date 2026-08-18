import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from google import genai
from dotenv import load_dotenv
import json
from app import db
from app.models import Resume
from app.models import Analysis

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

resume_bp = Blueprint("resume", __name__)

@resume_bp.route("/upload", methods=["GET", "POST"])
def upload():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        file = request.files.get("resume")

        if not file or file.filename == "":
            return "Please select a resume."

        if not file.filename.lower().endswith(".pdf"):
            flash("Please upload a PDF file.")
            return redirect(url_for("resume.upload"))

        filename = secure_filename(file.filename)
        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        reader = PdfReader(file_path)

        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        if not text.strip():
            flash("Could not extract text from this PDF. Please upload a text-based resume.")
            return redirect(url_for("resume.upload"))
        new_resume = Resume(filename=filename, extracted_text=text, user_id=session["user_id"])

        db.session.add(new_resume)
        db.session.commit()
        return redirect(url_for("resume.result", resume_id=new_resume.id))
    return render_template("upload.html")

@resume_bp.route("/result/<int:resume_id>")
def result(resume_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    resume = Resume.query.filter_by(id=resume_id, user_id=session["user_id"]).first_or_404()

    analysis = Analysis.query.filter_by(
        resume_id=resume.id
    ).order_by(Analysis.id.desc()).first()

    if analysis:
       analysis.strengths = json.loads(analysis.strengths or "[]")
       analysis.missing_skills = json.loads(analysis.missing_skills or "[]")
       analysis.weaknesses = json.loads(analysis.weaknesses or "[]")
       analysis.suggestions = json.loads(analysis.suggestions or "[]")
       analysis.recommended_skills = json.loads(analysis.recommended_skills or "[]")

    return render_template("result.html", resume=resume, analysis=analysis)

@resume_bp.route("/analyze/<int:resume_id>", methods=["POST"])
def analyze(resume_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    resume = Resume.query.filter_by(id=resume_id, user_id=session["user_id"]).first_or_404()

    job_role = request.form.get("job_role")
    job_description = request.form.get("job_description")

    if not job_role:
       flash("Please enter a target job role.")
       return redirect(url_for("resume.result", resume_id=resume.id))
    
    prompt = f"""
    Analyze the following resume for the target job role.

    Target Role:
    {job_role}

    Job Description:
    {job_description}

    Resume:
    {resume.extracted_text}

    Return ONLY valid JSON in this format:

    {{
       "match_score": 0,
       "strengths": [],
       "missing_skills": [],
       "weaknesses": [],
       "suggestions": [],
       "recommended_skills": []
    }}
    """ 
    try:
        response = client.interactions.create(model="gemini-3-flash-preview", input=prompt)
        analysis_data = json.loads(response.output_text)
    except Exception as e:
        print("Gemini Error:", e)
        flash("Something went wrong while analyzing your resume. Please try again.")
        return redirect(url_for("resume.result", resume_id=resume.id))

    analysis = Analysis(
    resume_id=resume.id,
    job_role=job_role,
    job_description=job_description,
    match_score=analysis_data.get("match_score", 0),
    strengths=json.dumps(analysis_data.get("strengths", [])),
    missing_skills=json.dumps(analysis_data.get("missing_skills", [])),
    weaknesses=json.dumps(analysis_data.get("weaknesses", [])),
    suggestions=json.dumps(analysis_data.get("suggestions", [])),
    recommended_skills=json.dumps(analysis_data.get("recommended_skills", []))
)
    try:
      db.session.add(analysis)
      db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Database Error:", e)
        flash("Something went wrong while saving your analysis.")
        return redirect(url_for("resume.result", resume_id=resume.id))

    return redirect(url_for("resume.result", resume_id=resume.id))