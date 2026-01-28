from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .db import Base, engine, SessionLocal
from . import models, schemas

app = FastAPI(title="Job Application Tracker")

# Create tables on startup (simple MVP approach)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/applications", response_model=schemas.ApplicationOut, status_code=201)
def create_application(payload: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    app_row = models.Application(
        company=payload.company,
        role=payload.role,
        status=payload.status,
        notes=payload.notes,
    )
    db.add(app_row)
    db.commit()
    db.refresh(app_row)
    return app_row

@app.get("/applications", response_model=list[schemas.ApplicationOut])
def list_applications(db: Session = Depends(get_db), limit: int = 20, offset: int = 0):
    return (
        db.query(models.Application)
        .order_by(models.Application.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
