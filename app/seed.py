
from .database import SessionLocal
from .models import University, Programme, Course
from .academic_data import ACADEMIC_CATALOG


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
        university = db.query(University).filter_by(
            code="FUO"
        ).first()

        if not university:
            university = University(
                name="Federal University Otuoke",
                code="FUO"
            )

            db.add(university)
            db.flush()

        # Create programmes if they do not exist.
        for name, faculty in PROGRAMMES:

            programme = db.query(Programme).filter_by(
                university_id=university.id,
                name=name
            ).first()

            if not programme:
                programme = Programme(
                    university_id=university.id,
                    name=name,
                    faculty=faculty
                )

                db.add(programme)

        db.flush()

        # Register courses from the academic catalogue.
        for course_key, data in ACADEMIC_CATALOG.items():

            programme = db.query(Programme).filter_by(
                university_id=university.id,
                name=data["programme"]
            ).first()

            if not programme:
                continue

            course = db.query(Course).filter_by(
                programme_id=programme.id,
                code=data["code"]
            ).first()

            if not course:

                course = Course(
                    programme_id=programme.id,
                    code=data["code"],
                    title=data["title"],
                    level=data["level"],
                    semester=data["semester"]
                )

                db.add(course)

            else:

                course.title = data["title"]
                course.level = data["level"]
                course.semester = data["semester"]

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
