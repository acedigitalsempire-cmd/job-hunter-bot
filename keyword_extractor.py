from collections import Counter
import re

TECH_SKILLS_LIST = [
    "zendesk", "intercom", "crm", "slack", "ticketing",
    "saas", "support", "freshdesk", "hubspot", "salesforce",
    "jira", "confluence", "notion", "live chat", "helpdesk"
]

STOP_WORDS = {
    "the", "and", "for", "with", "that", "this", "you", "are",
    "will", "have", "from", "our", "your", "can", "all", "not",
    "we", "be", "a", "an", "in", "of", "to", "is", "it", "as",
    "or", "on", "at", "by", "do", "if", "up"
}


def extract_keywords(text):
    if not text:
        return [], []

    # Strip HTML tags
    clean = re.sub(r'<[^>]+>', ' ', text)
    words = re.findall(r'\b\w+\b', clean.lower())

    # Filter stop words
    meaningful = [w for w in words if w not in STOP_WORDS and len(w) > 3]
    common = Counter(meaningful).most_common(8)
    keywords = [word for word, _ in common[:5]]

    # Extract tech skills
    tech_skills = list(set(w for w in words if w in TECH_SKILLS_LIST))[:5]

    return keywords, tech_skills
