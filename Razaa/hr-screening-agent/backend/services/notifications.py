def send_slack_notification(candidate_name: str, score: int, job_description: str):
    """
    Mocks sending a Slack notification to the HR team.
    In production, this would use a webhook URL or Slack SDK.
    """
    print(f"[SLACK MOCK] 🔔 New High-Scoring Candidate!")
    print(f"[SLACK MOCK] Name: {candidate_name}")
    print(f"[SLACK MOCK] Match Score: {score}")
    print(f"[SLACK MOCK] Review the candidate on the dashboard.")

def send_interview_invite(candidate_email: str, interview_link: str):
    """
    Mocks sending an email to the candidate with an interview link.
    In production, this would use an email service like SendGrid, Resend, or SMTP.
    """
    print(f"[EMAIL MOCK] 📧 Sending email to {candidate_email}...")
    print(f"[EMAIL MOCK] Subject: Invitation to Interview")
    print(f"[EMAIL MOCK] Body: Congratulations! Your application stood out. "
          f"Please schedule your interview using this link: {interview_link}")
