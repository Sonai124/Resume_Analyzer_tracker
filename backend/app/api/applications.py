from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.application import Application

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/")
def create_application(
    company: str,
    role: str,
    status: str = "applied",
    link: str | None = None,
    notes: str | None = None,
    db: Session = Depends(get_db),
):
    app_entry = Application(
        company=company,
        role=role,
        status=status,
        link=link,
        notes=notes,
    )
    db.add(app_entry)
    db.commit()
    db.refresh(app_entry)
    return app_entry


@router.get("/")
def list_applications(db: Session = Depends(get_db)):
    return db.query(Application).order_by(Application.created_at.desc()).all()


@router.get("/{application_id}")
def get_application(application_id: int, db: Session = Depends(get_db)):
    app_entry = db.query(Application).filter(Application.id == application_id).first()
    if not app_entry:
        raise HTTPException(status_code=404, detail="Application not found")
    return app_entry
