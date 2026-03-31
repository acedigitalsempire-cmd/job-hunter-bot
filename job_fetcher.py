import requests
from datetime import datetime, timedelta, timezone
import xml.etree.ElementTree as ET

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; JobHunterBot/1.0)"}

KEYWORDS = [
    "customer support", "customer success", "support specialist",
    "customer service", "customer experience", "support agent",
    "help desk", "helpdesk", "client support", "technical support"
]

# Locations that mean USA-only — exclude these
USA_ONLY = [
    "usa only", "us only", "united states only", "u.s. only",
    "must be based in the us", "must reside in the us",
    "must be located in the us", "north america only",
    "canada and us", "us and canada", "usa and canada",
    "residents of the united states", "authorized to work in the us",
    "eligible to work in the us", "work authorization in the us",
]

# Locations that confirm worldwide/global — prefer these
GLOBAL_KEYWORDS = [
    "worldwide", "global", "anywhere", "international",
    "remote - global", "remote global", "all countries",
    "work from anywhere", "fully remote", ""
]

def matches_keywords(title):
    title = title.lower()
    return any(k in title for k in KEYWORDS)

def is_usa_only(job):
    """Returns True if job is restricted to USA residents"""
    location = (job.get("location") or "").lower()
    description = (job.get("description") or "").lower()

    # Check location field
    for phrase in USA_ONLY:
        if phrase in location:
            return True

    # If location explicitly says USA/US with no global mention
    if location in ["usa", "us", "united states", "u.s."]:
        return True

    # Check description for USA-only work authorization language
    for phrase in USA_ONLY:
        if phrase in description:
            return True

    return False

def is_global(job):
    """Returns True if job is explicitly worldwide/global"""
    location = (job.get("location") or "").lower()
    description = (job.get("description") or "").lower()

    for phrase in GLOBAL_KEYWORDS:
        if phrase and (phrase in location or phrase in description):
            return True

    # Empty location often means global on remote boards
    if not location or location.strip() == "":
        return True

    return False

def is_recent(date_str, fmt="%Y-%m-%dT%H:%M:%S%z", days=1):
    try:
        job_date = datetime.strptime(date_str, fmt)
        return job_date >= datetime.now(timezone.utc) - timedelta(days=days)
    except Exception:
        return False

def fetch_remoteok():
    jobs = []
    try:
        res = requests.get("https://remoteok.com/api", headers=HEADERS, timeout=20)
        data = res.json()
        for job in data:
            if not isinstance(job, dict):
                continue
            title = job.get("position", "")
            if not matches_keywords(title):
                continue
            date_str = job.get("date", "")
            if not date_str or not is_recent(date_str):
                continue
            if is_usa_only(job):
                continue
            jobs.append({
                "title": title,
                "company": job.get("company", "N/A"),
                "location": job.get("location") or "Worldwide",
                "link": job.get("url", "#"),
                "description": job.get("description", ""),
                "source": "RemoteOK"
            })
        print(f"[RemoteOK] {len(jobs)} global jobs found")
    except Exception as e:
        print(f"[RemoteOK ERROR] {e}")
    return jobs

def fetch_remotive():
    jobs = []
    try:
        url = "https://remotive.com/api/remote-jobs?category=customer-support&limit=50"
        res = requests.get(url, headers=HEADERS, timeout=20)
        data = res.json()
        for job in data.get("jobs", []):
            title = job.get("title", "")
            if not matches_keywords(title):
                continue
            location = (job.get("candidate_required_location") or "").lower()
            # Skip USA-only
            if is_usa_only({"location": location, "description": job.get("description", "")}):
                continue
            # Skip if location restricts to specific non-global regions
            if location and location not in ["", "worldwide", "global", "anywhere"] and "worldwide" not in location and "global" not in location and "anywhere" not in location:
                # Allow if location doesn't mention specific country restrictions
                if any(x in location for x in ["usa", "us only", "united states", "canada only", "uk only", "eu only", "europe only"]):
                    continue
            jobs.append({
                "title": title,
                "company": job.get("company_name", "N/A"),
                "location": job.get("candidate_required_location") or "Worldwide",
                "link": job.get("url", "#"),
                "description": job.get("description", ""),
                "source": "Remotive"
            })
        print(f"[Remotive] {len(jobs)} global jobs found")
    except Exception as e:
        print(f"[Remotive ERROR] {e}")
    return jobs

def fetch_weworkremotely():
    jobs = []
    try:
        url = "https://weworkremotely.com/categories/remote-customer-support-jobs.rss"
        res = requests.get(url, headers=HEADERS, timeout=20)
        root = ET.fromstring(res.content)
        for item in root.findall(".//item"):
            title_el = item.find("title")
            link_el = item.find("link")
            desc_el = item.find("description")
            pub_el = item.find("pubDate")
            title = title_el.text if title_el is not None else ""
            if not matches_keywords(title):
                continue
            if pub_el is not None:
                try:
                    pub_date = datetime.strptime(pub_el.text.strip(), "%a, %d %b %Y %H:%M:%S %z")
                    if pub_date < datetime.now(timezone.utc) - timedelta(days=2):
                        continue
                except Exception:
                    pass
            desc_text = desc_el.text if desc_el is not None else ""
            if is_usa_only({"location": "", "description": desc_text}):
                continue
            parts = title.split(":")
            company = parts[0].strip() if len(parts) > 1 else "N/A"
            clean_title = parts[1].strip() if len(parts) > 1 else title
            jobs.append({
                "title": clean_title,
                "company": company,
                "location": "Worldwide",
                "link": link_el.text if link_el is not None else "#",
                "description": desc_text,
                "source": "WeWorkRemotely"
            })
        print(f"[WeWorkRemotely] {len(jobs)} global jobs found")
    except Exception as e:
        print(f"[WeWorkRemotely ERROR] {e}")
    return jobs

def fetch_himalayas():
    jobs = []
    try:
        url = "https://himalayas.app/jobs/api?q=customer+support&limit=30"
        res = requests.get(url, headers=HEADERS, timeout=20)
        data = res.json()
        for job in data.get("jobs", []):
            title = job.get("title", "")
            if not matches_keywords(title):
                continue
            location = (job.get("locationRestrictions") or "").lower()
            if is_usa_only({"location": location, "description": job.get("description", "")}):
                continue
            jobs.append({
                "title": title,
                "company": job.get("companyName", "N/A"),
                "location": job.get("locationRestrictions") or "Worldwide",
                "link": job.get("applicationLink", job.get("url", "#")),
                "description": job.get("description", ""),
                "source": "Himalayas"
            })
        print(f"[Himalayas] {len(jobs)} global jobs found")
    except Exception as e:
        print(f"[Himalayas ERROR] {e}")
    return jobs

def fetch_jobs():
    all_jobs = []
    all_jobs += fetch_remoteok()
    all_jobs += fetch_remotive()
    all_jobs += fetch_weworkremotely()
    all_jobs += fetch_himalayas()

    seen = set()
    unique_jobs = []
    for job in all_jobs:
        key = (job["title"].lower().strip(), job["company"].lower().strip())
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    print(f"[TOTAL] {len(unique_jobs)} unique global jobs across all sources")
    return unique_jobs
