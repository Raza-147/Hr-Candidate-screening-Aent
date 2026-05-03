from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List
import os
import shutil
from services.cv_parser import extract_text_from_pdf
from services.ai_agent import score_candidate
from services.notifications import send_slack_notification, send_interview_invite
from services.scheduling import generate_interview_link

app = FastAPI(title="HR Candidate Screening Agent")

# Allow CORS for any external frontend (if used)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)

# Mounted static files
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
def read_root():
    return FileResponse("../frontend/index.html")

@app.post("/api/upload-cv/")
async def upload_cv(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    candidate_name: str = Form(...),
    candidate_email: str = Form(...)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 1. Parse CV
    cv_text = extract_text_from_pdf(file_path)
    
    # 2. AI Scoring
    try:
        score_result = score_candidate(cv_text, job_description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scoring candidate: {str(e)}")

    import time
    candidate_record = {
        "id": int(time.time() * 1000),
        "name": candidate_name,
        "email": candidate_email,
        "filename": file.filename,
        "score": score_result.score,
        "reasoning": score_result.reasoning,
        "status": "Scored"
    }
    
    # 3. Actions based on score
    if score_result.score >= 80:
        # High score - notify recruiter and auto-schedule
        send_slack_notification(candidate_name, score_result.score, job_description)
        interview_link = generate_interview_link(candidate_email)
        send_interview_invite(candidate_email, interview_link)
        candidate_record["status"] = "Interview Scheduled"
        candidate_record["interview_link"] = interview_link
        
    return candidate_record
