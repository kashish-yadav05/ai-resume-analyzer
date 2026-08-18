SKILLS = [
    "Python", "Java", "JavaScript", "C", "C++", "SQL", "HTML", "CSS", "Flask", "Django", "React",
    "Node.js", "Git", "GitHub", "Docker", "AWS", "Machine Learning", "Tensor Flow", "PyTorch",
    "Pandas", "NumPy", "MongoDB",
]

def detect_skills(text):
    text_lower = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    return found_skills