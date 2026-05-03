import os
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

class CandidateScore(BaseModel):
    score: int = Field(description="A score from 0 to 100 indicating how well the candidate fits the job description.")
    reasoning: str = Field(description="A brief explanation of why the score was given.")

def score_candidate(cv_text: str, job_description: str) -> CandidateScore:
    """Uses LLM to score the candidate's CV against the job description."""
    
    # Using the Gemini API key provided by the user
    api_key = "AIzaSyC_GqMbFwgahlJEiMZqdCIt42F4LYNsiHk"
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, google_api_key=api_key)
    
    parser = PydanticOutputParser(pydantic_object=CandidateScore)
    
    prompt = PromptTemplate(
        template="You are an expert HR recruiter. Evaluate the candidate's CV against the Job Description.\n"
                 "{format_instructions}\n\n"
                 "Job Description:\n{job_description}\n\n"
                 "Candidate CV:\n{cv_text}\n",
        input_variables=["job_description", "cv_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | llm | parser
    
    result = chain.invoke({
        "job_description": job_description,
        "cv_text": cv_text
    })
    
    return result
