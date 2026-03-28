import requests
from datetime import datetime, timedelta, timezone


def fetch_jobs():
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; JobHunterBot/1.0)"}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        jobs = response.json()
    except Exception as e:
        print(f"[ERROR] Failed to fetch jobs: {e}")
        return []

    filtered_jobs = []
    now = datetime.now(timezone.utc)
    last_24h = now - timedelta(days=1)

    for job in jobs:
        if not isinstance(job, dict):
            continue

        title = job.get("position", "").lower()
        company = job.get("company", "Unknown")
        date_str = job.get("date")

        if not date_str:
            continue

        try:
            job_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            continue

        if job_date < last_24h:
            continue

        if not any(k in title for k in [
            "customer support", "customer success", "support", "customer service", "customer experience"
        ]):
            continue

        filtered_jobs.append({
            "title": job.get("position", "N/A"),
            "company": company,
            "location": job.get("location", "Remote"),
            "link": job.get("url", "#"),
            "description": job.get("description", "")
        })

    print(f"[INFO] Found {len(filtered_jobs)} matching jobs.")
    return filtered_jobs
