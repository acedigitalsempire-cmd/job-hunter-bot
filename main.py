from job_fetcher import fetch_jobs
from keyword_extractor import extract_keywords
from emailer import send_email
from datetime import datetime


SOURCE_COLORS = {
    "RemoteOK": "#3498db",
    "Remotive": "#9b59b6",
    "WeWorkRemotely": "#27ae60",
    "Himalayas": "#e67e22",
}


def generate_html(jobs):
    today = datetime.now().strftime("%A, %B %d, %Y")

    if not jobs:
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: white; border-radius: 10px; padding: 30px; text-align: center;">
                <h2 style="color: #e74c3c;">No Jobs Found Today</h2>
                <p style="color: #555;">No remote customer support jobs were posted in the last 48 hours across all sources.</p>
                <p style="color: #888; font-size: 12px;">Date: {today} | Check back tomorrow!</p>
            </div>
        </body>
        </html>
        """

    rows = ""
    for i, job in enumerate(jobs):
        keywords, skills = extract_keywords(job["description"])
        bg = "#ffffff" if i % 2 == 0 else "#f9f9f9"
        keyword_str = ", ".join(keywords) if keywords else "—"
        skills_str = ", ".join(skills) if skills else "—"
        source = job.get("source", "Unknown")
        source_color = SOURCE_COLORS.get(source, "#555")

        rows += f"""
        <tr style="background: {bg};">
            <td style="padding: 12px; border-bottom: 1px solid #eee;">
                <strong style="color: #2c3e50;">{job['title']}</strong>
            </td>
            <td style="padding: 12px; border-bottom: 1px solid #eee; color: #555;">
                {job['company']}
            </td>
            <td style="padding: 12px; border-bottom: 1px solid #eee; color: #555;">
                {job['location']}
            </td>
            <td style="padding: 12px; border-bottom: 1px solid #eee;">
                <span style="background: {source_color}; color: white; padding: 3px 8px;
                border-radius: 10px; font-size: 11px;">{source}</span>
            </td>
            <td style="padding: 12px; border-bottom: 1px solid #eee;">
                <a href="{job['link']}" style="background: #2ecc71; color: white; padding: 6px 14px;
                   border-radius: 4px; text-decoration: none; font-weight: bold;">Apply →</a>
            </td>
            <td style="padding: 12px; border-bottom: 1px solid #eee; color: #777; font-size: 12px;">
                {keyword_str}
            </td>
            <td style="padding: 12px; border-bottom: 1px solid #eee; color: #e67e22; font-size: 12px;">
                {skills_str}
            </td>
        </tr>
        """

    source_counts = {}
    for job in jobs:
        s = job.get("source", "Unknown")
        source_counts[s] = source_counts.get(s, 0) + 1

    source_summary = " &nbsp;|&nbsp; ".join(
        [f'<span style="color:{SOURCE_COLORS.get(s,"#555")}">⬤</span> {s}: <strong>{c}</strong>'
         for s, c in source_counts.items()]
    )

    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; margin: 0;">
        <div style="max-width: 1000px; margin: auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">

            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 30px; text-align: center;">
                <h1 style="color: #f1c40f; margin: 0; font-size: 24px;">🎯 Daily Job Hunt Report</h1>
                <p style="color: #aaa; margin: 8px 0 0;">{today}</p>
                <p style="color: white; font-size: 18px; margin: 10px 0 0;">
                    <strong>{len(jobs)}</strong> Remote Customer Support Job(s) Found
                </p>
                <p style="color: #ccc; font-size: 13px; margin-top: 8px;">{source_summary}</p>
            </div>

            <div style="padding: 20px; overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                    <thead>
                        <tr style="background: #2c3e50; color: white;">
                            <th style="padding: 12px; text-align: left;">Job Title</th>
                            <th style="padding: 12px; text-align: left;">Company</th>
                            <th style="padding: 12px; text-align: left;">Location</th>
                            <th style="padding: 12px; text-align: left;">Source</th>
                            <th style="padding: 12px; text-align: left;">Apply</th>
                            <th style="padding: 12px; text-align: left;">Keywords</th>
                            <th style="padding: 12px; text-align: left;">Skills</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>

            <div style="background: #f8f8f8; padding: 20px; text-align: center; border-top: 1px solid #eee;">
                <p style="color: #aaa; font-size: 12px; margin: 0;">
                    Sourced from RemoteOK 🔵 &nbsp; Remotive 🟣 &nbsp; WeWorkRemotely 🟢 &nbsp; Himalayas 🟠<br>
                    This email was sent automatically by your Job Hunter Bot 🤖 — runs daily at 10AM Nigeria Time.
                </p>
            </div>

        </div>
    </body>
    </html>
    """


def main():
    print("[INFO] Starting Job Hunter Bot...")
    jobs = fetch_jobs()
    html = generate_html(jobs)
    send_email(html, job_count=len(jobs))
    print("[INFO] Done!")


if __name__ == "__main__":
    main() 
