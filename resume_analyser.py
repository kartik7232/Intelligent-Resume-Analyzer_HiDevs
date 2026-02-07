def load_resume(file):
    try:
        with open(file, "r") as f:
            return f.read()
    except FileNotFoundError:
        print("Resume file not found")


def parse_resume(text):
    resume = {
        "name": "",
        "email": "",
        "skills": [],
        "experience": 0,
        "education": ""
    }

    for line in text.split("\n"):
        line = line.strip()

        if line.lower().startswith("name"):
            resume["name"] = line.split(":")[1].strip()

        elif line.lower().startswith("email"):
            resume["email"] = line.split(":")[1].strip()
            
        elif line.lower().startswith("skills"):
            resume["skills"] = [
                skill.strip().lower()
                for skill in line.split(":")[1].split(",")
            ]

        elif line.lower().startswith("experience"):
            resume["experience"] = int(
                line.split(":")[1].replace("years", "").strip()
            )

        elif line.lower().startswith("education"):
            resume["education"] = line.split(":")[1].strip()

    return resume


def analyze_candidate(candidate, job):
    matched_skills = set(candidate["skills"]) & set(job["required_skills"])
    missing_skills = set(job["required_skills"]) - set(candidate["skills"])

    score = len(matched_skills) * 10

    if candidate["experience"] >= job["min_experience"]:
        score += 30

    if candidate["education"].lower() in job["education"]:
        score += 20

    return score, matched_skills, missing_skills


def generate_report(candidate, job, score, matched_skills, missing_skills):
    if score >= 80:
        recommendation = " STRONGLY RECOMMENDED"
    elif score >= 60:
        recommendation = " RECOMMENDED"
    elif score >= 40:
        recommendation = " MAYBE"
    else:
        recommendation = " NOT RECOMMENDED"

    report = f"""
<<--------- RESUME ANALYSIS REPORT --------->>
Candidate Name : {candidate["name"]}
Job Role       : {job["title"]}
Match Score    : {score}/100

<<-- SKILLS -->>
Matched Skills : {', '.join(matched_skills)}
Missing Skills : {', '.join(missing_skills)}

<<--- EXPERIENCE -->>
Candidate Experience : {candidate["experience"]} years
Required Experience  : {job["min_experience"]} years

<<-- FINAL DECISION -->>
{recommendation}
----------------------
"""
    return report


# --------------------
# MAIN PROGRAM
# --------------------

job_requirements = {
    "title": "Python Developer",
    "required_skills": ["python", "sql", "machine learning", "git"],
    "min_experience": 2,
    "education": ["b.tech", "bachelor","Master's","Phd"]
}

resume_text = load_resume("resume.txt")
candidate = parse_resume(resume_text)

score, matched, missing = analyze_candidate(candidate, job_requirements)
report = generate_report(candidate, job_requirements, score, matched, missing)

print(report)
