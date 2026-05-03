import urllib.parse

def generate_interview_link(candidate_email: str) -> str:
    """
    Mocks generating a scheduling link for the candidate.
    In production, this could interact with Calendly API, Google Calendar API, etc.
    """
    base_url = "https://calendly.com/mock-hr-scheduling/30min"
    
    # Optionally append email as a query parameter if the scheduling service supports it
    encoded_email = urllib.parse.quote(candidate_email)
    return f"{base_url}?email={encoded_email}"
