from .database import SessionLocal
from .models import University, Programme

PROGRAMMES = [
    ("Computer Science & Informatics", "Science"),
    ("Nursing Science", "Nursing Science"),
    ("Law", "Law"),
    ("Accounting", "Management Sciences"),
    ("Business Administration", "Management Sciences"),
    ("Political Science", "Social Sciences"),
    ("Economics & Development Studies", "Social Sciences"),
    ("Civil Engineering", "Engineering"),
    ("Electrical/Electronics Engineering", "Engineering"),
    ("Mechanical Engineering", "Engineering"),
]

def seed():
    db = SessionLocal()
    try:
        university = db.query(University).filter_by(code="FUO").first()
        if not university:
            university = University(name="Federal University Otuoke", code="FUO")
            db.add(university)
            db.flush()

        for name, faculty in PROGRAMMES:
            exists = db.query(Programme).filter_by(
                university_id=university.id, name=name
            ).first()
            if not exists:
                db.add(Programme(university_id=university.id, name=name, faculty=faculty))

        db.commit()
    finally:
        db.close()
