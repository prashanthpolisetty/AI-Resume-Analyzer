from __future__ import annotations

import re
from collections import Counter
from typing import Iterable

COMMON_STOP_WORDS = {
    "about", "above", "after", "again", "against", "being", "between", "could",
    "from", "have", "into", "more", "other", "should", "their", "there", "these",
    "those", "using", "will", "with", "your", "that", "this", "they", "and", "the",
    "for", "are", "you", "our", "but", "not", "can", "all", "any", "has", "its",
    "job", "work", "role", "skills", "experience", "years", "required", "preferred",
}

SKILL_TERMS = {
    "python", "java", "javascript", "typescript", "react", "next.js", "node.js", "sql",
    "postgresql", "mysql", "mongodb", "aws", "azure", "gcp", "docker", "kubernetes",
    "git", "rest", "graphql", "fastapi", "django", "flask", "pandas", "numpy",
    "machine learning", "data analysis", "figma", "excel", "communication", "leadership",
    "testing", "ci/cd", "linux", "terraform", "html", "css",
}

BUZZWORDS = {
    "hard worker": "reliable contributor who consistently delivered [specific result]",
    "team player": "collaborated with [team/role] to [specific outcome]",
    "go-getter": "initiated [project/action] that led to [result]",
    "synergy": "cross-functional collaboration",
    "results-driven": "achieved [measurable result] by [action]",
    "detail-oriented": "improved [quality/accuracy metric] through [specific process]",
    "responsible for": "delivered / led / implemented",
    "passionate": "built / researched / shipped [specific thing]",
}


def words(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z0-9+#./-]{1,}", text.lower())


def extract_keywords(text: str, limit: int = 30) -> list[str]:
    counts = Counter(word for word in words(text) if word not in COMMON_STOP_WORDS and len(word) > 2)
    return [word for word, _ in counts.most_common(limit)]


def find_skills(text: str) -> list[str]:
    lowered = text.lower()
    return sorted(skill for skill in SKILL_TERMS if skill in lowered)


def clamp(value: int, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, int(round(value))))


def sections(text: str) -> set[str]:
    known = {"summary", "objective", "education", "experience", "projects", "skills", "certifications", "awards"}
    return {line.strip(" :#-\t").lower() for line in text.splitlines() if line.strip(" :#-\t").lower() in known}


def analyze_resume(text: str, jd: str | None = None, job_title: str | None = None) -> dict:
    resume_words = set(words(text))
    resume_skills = find_skills(text)
    present_sections = sections(text)
    if jd and jd.strip():
        jd_keywords = extract_keywords(jd, 40)
        missing_keywords = [keyword for keyword in jd_keywords if keyword not in resume_words][:15]
        jd_skills = find_skills(jd)
        missing_skills = [skill for skill in jd_skills if skill not in resume_skills]
        keyword_score = clamp(100 * (len(jd_keywords) - len(missing_keywords)) / max(len(jd_keywords), 1))
        skill_score = clamp(100 * (len(jd_skills) - len(missing_skills)) / max(len(jd_skills), 1)) if jd_skills else 70
        impact = min(100, 45 + 12 * len(re.findall(r"\b\d+(?:%|\+)?\b", text)))
        score = clamp(keyword_score * 0.45 + skill_score * 0.35 + impact * 0.20)
        mode = "targeted"
        feedback = [
            f"Add evidence for {missing_skills[0]} in a project or experience bullet." if missing_skills else "Your listed skills align well with this job description.",
            f"Use these missing terms naturally where truthful: {', '.join(missing_keywords[:6])}." if missing_keywords else "Your resume uses the main terms from the job description.",
        ]
        return {
            "mode": mode, "score": score, "score_label": f"{score}/100", "job_title": job_title,
            "match_score": score, "missing_keywords": missing_keywords,
            "skill_gaps": missing_skills, "strengths": resume_skills[:10],
            "feedback": feedback, "sections_found": sorted(present_sections),
            "next_steps": ["Replace generic claims with measurable outcomes.", "Keep only keywords supported by real experience."],
        }

    grammar_issues = []
    if re.search(r"\bi am\b", text, re.I): grammar_issues.append("Use concise resume language instead of first-person statements.")
    if re.search(r"\s{2,}", text): grammar_issues.append("Remove repeated spaces; they can affect ATS parsing.")
    if not re.search(r"\b(?:19|20)\d{2}\b", text): grammar_issues.append("Add dates to education, projects, or experience where relevant.")
    section_score = min(100, len(present_sections) * 16)
    metric_score = min(100, 40 + len(re.findall(r"\b\d+(?:%|\+)?\b", text)) * 15)
    format_score = clamp(section_score * 0.7 + metric_score * 0.3)
    impact_score = clamp(50 + len(resume_skills) * 4 + len(re.findall(r"\b(?:built|led|improved|increased|reduced|launched|designed)\b", text, re.I)) * 6)
    score = clamp(format_score * 0.35 + impact_score * 0.4 + (100 - min(40, len(grammar_issues) * 12)) * 0.25)
    return {
        "mode": "general", "score": score, "score_label": f"{score}/100", "job_title": None,
        "grammar_issues": grammar_issues, "format_score": format_score, "impact_score": impact_score,
        "strengths": resume_skills[:10], "sections_found": sorted(present_sections),
        "feedback": [
            "Add numbers, time saved, users served, or quality improvements to project bullets.",
            "Lead each bullet with a strong action verb and keep formatting consistent.",
        ],
        "next_steps": ["Add or strengthen a summary, skills, projects, education, and experience section.", "Tailor the resume to each role before applying."],
    }


def boost_project(notes: str, role: str | None = None) -> list[str]:
    clean = re.sub(r"\s+", " ", notes).strip().rstrip(".")
    focus = f" for {role}" if role else ""
    return [
        f"Built{focus} {clean}, using [tools/technologies], to solve [specific problem].",
        f"Designed and implemented {clean}, improving [metric] by [amount] through [key action].",
        f"Collaborated with [team/users] to test and refine {clean}, resulting in [measurable outcome].",
    ]


def skill_proof(skills: Iterable[str], resume_text: str) -> list[dict]:
    result = []
    lowered = resume_text.lower()
    for skill in skills:
        name = skill.strip()
        if not name: continue
        found = name.lower() in lowered
        evidence = [line.strip() for line in resume_text.splitlines() if name.lower() in line.lower()][:2]
        result.append({"skill": name, "supported": found and len(evidence) > 0, "evidence": evidence, "advice": None if found else f"Add a project, course, or result that demonstrates {name}."})
    return result


def buzzword_report(text: str) -> list[dict]:
    lowered = text.lower()
    return [{"phrase": phrase, "replacement": replacement} for phrase, replacement in BUZZWORDS.items() if phrase in lowered]
