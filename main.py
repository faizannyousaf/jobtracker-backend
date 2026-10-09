from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Job as JobModel

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

class JobCreate(BaseModel):
    user_id: str
    company: str
    role: str
    date_applied: str
    status: str

class JobResponse(BaseModel):
    id: int
    user_id: str
    company: str
    role: str
    date_applied: str
    status: str

    class Config:
        from_attributes = True

@app.get("/")
def home():
    return {"message": "JobTracker API running"}

@app.get("/jobs/{user_id}")
def get_jobs(user_id: str, db: Session = Depends(get_db)):
    jobs = db.query(JobModel).filter(JobModel.user_id == user_id).all()
    return jobs

@app.post("/jobs")
def add_job(job: JobCreate, db: Session = Depends(get_db)):
    db_job = JobModel(
        user_id=job.user_id,
        company=job.company,
        role=job.role,
        date_applied=job.date_applied,
        status=job.status
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted"}

@app.put("/jobs/{job_id}")
def update_job(job_id: int, job: JobCreate, db: Session = Depends(get_db)):
    db_job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db_job.company = job.company
    db_job.role = job.role
    db_job.status = job.status
    db_job.date_applied = job.date_applied
    
    db.commit()
    db.refresh(db_job)
    return db_job