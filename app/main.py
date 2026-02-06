from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from .app.db import Base, engine, SessionLocal
from .app import models, schemas

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
def list_applications(
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: str | None = None,
    company: str | None = None,
):
    q = db.query(models.Application)

    if status:
        q = q.filter(models.Application.status == status)

    if company:
        q = q.filter(models.Application.company.ilike(f"%{company}%"))

    return (
        q.order_by(models.Application.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


@app.get("/applications/{app_id}", response_model=schemas.ApplicationOut)
def get_application(app_id: int, db: Session = Depends(get_db)):
    row = db.query(models.Application).filter(models.Application.id == app_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Application not found")
    return row


@app.patch("/applications/{app_id}", response_model=schemas.ApplicationOut)
def update_application(app_id: int, payload: schemas.ApplicationUpdate, db: Session = Depends(get_db)):
    row = db.query(models.Application).filter(models.Application.id == app_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Application not found")

    data = payload.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(row, key, value)

    db.commit()
    db.refresh(row)
    return row


@app.delete("/applications/{app_id}", status_code=204)
def delete_application(app_id: int, db: Session = Depends(get_db)):
    row = db.query(models.Application).filter(models.Application.id == app_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(row)
    db.commit()
    return None


@app.get("/stats", response_model=schemas.StatsOut)
def stats(db: Session = Depends(get_db)):
    total = db.query(func.count(models.Application.id)).scalar() or 0

    by_status = (
        db.query(models.Application.status, func.count(models.Application.id))
        .group_by(models.Application.status)
        .all()
    )

    return {
        "total": total,
        "by_status": {status: count for status, count in by_status},
    }

