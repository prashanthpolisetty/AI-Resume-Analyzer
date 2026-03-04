import re

def extract_score(output_text):
    """
    Extracts the first integer score from a string like 'JD Match Score: 21/25'
    """
    match = re.search(r'(\d{1,3})', output_text)
    return int(match.group(1)) if match else 0

def compute_final_score(jd_score, exp_score, grammar_score, keyword_score, skill_score):
    """
    Combine all individual scores to calculate final ATS score.
    Returns both the total and a breakdown string.
    """
    final_score = jd_score + exp_score + grammar_score + keyword_score + skill_score

    breakdown = (
        f"JD Match: {jd_score}/25\n"
        f"Experience: {exp_score}/15\n"
        f"Grammar: {grammar_score}/10\n"
        f"Keyword Density: {keyword_score}/15\n"
        f"Skill Gap: {skill_score}/20\n"
        f"ATS Score: {final_score}/100"
    )
    return final_score, breakdown

def get_final_score_from_outputs(outputs):
    jd_score       = extract_score(outputs.get("jd_match", ""))
    exp_score      = extract_score(outputs.get("experience", ""))
    grammar_score  = extract_score(outputs.get("grammar", ""))
    keyword_score  = extract_score(outputs.get("keyword_density", ""))
    skill_score    = extract_score(outputs.get("skill_gap", ""))

    final_score, breakdown = compute_final_score(jd_score, exp_score, grammar_score, keyword_score, skill_score)

    return {
        "final_score": final_score,
        "ats_display": f"ATS Score: {final_score}/100",
        "breakdown": breakdown
    }
