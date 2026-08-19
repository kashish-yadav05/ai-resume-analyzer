# AI Resume Analyzer

An AI-powered web application that analyzes resumes against a target job role and provides a match score, strengths, missing skills, weaknesses, suggestions, and recommended skills.

Built with **Python, Flask, SQLite, and Google Gemini AI**.


## Features

* User registration and login
* Secure resume upload
* PDF text extraction
* Target job role selection
* Optional job description input
* AI-powered resume analysis using Google Gemini
* Resume match score
* Strengths identification
* Missing skills detection
* Weakness identification
* Personalized improvement suggestions
* Recommended skills for the target role
* Analysis results stored in SQLite database
* Responsive and user-friendly interface


## Tech Stack

* **Python**
* **Flask**
* **SQLite & Flask-SQLAlchemy**
* **Google Gemini API**
* **PyPDF2**
* **HTML, CSS & Jinja2**
* **Git & GitHub**


## How It Works

1. User creates an account and logs in.
2. User uploads a resume in PDF format.
3. The application extracts text from the PDF using PyPDF2.
4. User enters a target job role and optional job description.
5. The resume content and job requirements are sent to Google Gemini.
6. Gemini analyzes the resume and returns structured results.
7. The application stores the analysis in SQLite.
8. The user receives a match score, strengths, missing skills, weaknesses, suggestions, and recommended skills.


## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/kashish-yadav05/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Set up the Gemini API key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your own Google Gemini API key.

### 6. Run the application

```bash
python run.py
```

Then open the local URL shown in the terminal.


## Future Improvements

* Improve resume analysis accuracy and scoring
* Add support for more resume file formats
* Add resume history and comparison
* Add downloadable analysis reports
* Improve UI with more visual analytics
* Add deployment and production configuration


## Security

* API keys are stored in environment variables using a `.env` file.
* The `.env` file is excluded from Git using `.gitignore`.
* Uploaded resumes and local database files are excluded from version control.
* Users can only access their own uploaded resumes and analysis results.
