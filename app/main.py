
import json
import os
import urllib.error
import urllib.request

from fastapi import (
    Depends,
    FastAPI,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .config import settings
from .models import (
    University,
    Programme,
    Course,
    Resource,
    Upload,
    ResourceNotification,
)
from .storage import save_file, validate_pdf
from .seed import seed
from .academic_data import ACADEMIC_CATALOG


# DATABASE INITIALIZATION

Base.metadata.create_all(bind=engine)
seed()


# APPLICATION

app = FastAPI(
    title="CampusCorrect",
    version="0.5.0"
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

templates = Jinja2Templates(
    directory="app/templates"
)


# CONSTANTS

VALID_LEVELS = [100, 200, 300, 400, 500]
VALID_SEMESTERS = [1, 2]


# HOMEPAGE

@app.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    db: Session = Depends(get_db)
):
    university = db.query(University).filter_by(
        code="FUO"
    ).first()

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "university": university,
        },
    )


# STEP 1: SELECT LEVEL

@app.get(
    "/level/{level}",
    response_class=HTMLResponse
)
def select_level(
    request: Request,
    level: int,
    db: Session = Depends(get_db)
):
    if level not in VALID_LEVELS:
        raise HTTPException(
            status_code=404,
            detail="Level not found"
        )

    university = db.query(University).filter_by(
        code="FUO"
    ).first()

    if not university:
        raise HTTPException(
            status_code=404,
            detail="University not found"
        )

    programmes = (
        db.query(Programme)
        .filter(
            Programme.university_id == university.id
        )
        .order_by(Programme.name)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="programmes.html",
        context={
            "level": level,
            "programmes": programmes,
        },
    )


# STEP 2: SELECT PROGRAMME

@app.get(
    "/level/{level}/programme/{programme_id}",
    response_class=HTMLResponse
)
def select_programme(
    request: Request,
    level: int,
    programme_id: int,
    db: Session = Depends(get_db)
):
    if level not in VALID_LEVELS:
        raise HTTPException(
            status_code=404,
            detail="Level not found"
        )

    university = db.query(University).filter_by(
        code="FUO"
    ).first()

    if not university:
        raise HTTPException(
            status_code=404,
            detail="University not found"
        )

    programme = db.query(Programme).filter(
        Programme.id == programme_id,
        Programme.university_id == university.id
    ).first()

    if not programme:
        raise HTTPException(
            status_code=404,
            detail="Programme not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="semester.html",
        context={
            "level": level,
            "programme": programme,
        },
    )


# STEP 3: SELECT SEMESTER

@app.get(
    "/level/{level}/programme/{programme_id}/semester/{semester}",
    response_class=HTMLResponse
)
def select_semester(
    request: Request,
    level: int,
    programme_id: int,
    semester: int,
    db: Session = Depends(get_db)
):
    if level not in VALID_LEVELS:
        raise HTTPException(
            status_code=404,
            detail="Level not found"
        )

    if semester not in VALID_SEMESTERS:
        raise HTTPException(
            status_code=404,
            detail="Semester not found"
        )

    university = db.query(University).filter_by(
        code="FUO"
    ).first()

    if not university:
        raise HTTPException(
            status_code=404,
            detail="University not found"
        )

    programme = db.query(Programme).filter(
        Programme.id == programme_id,
        Programme.university_id == university.id
    ).first()

    if not programme:
        raise HTTPException(
            status_code=404,
            detail="Programme not found"
        )

    courses = (
        db.query(Course)
        .filter(
            Course.programme_id == programme.id,
            Course.level == level,
            Course.semester == str(semester)
        )
        .order_by(Course.code)
        .all()
    )

    semester_name = (
        "First Semester"
        if semester == 1
        else "Second Semester"
    )

    return templates.TemplateResponse(
        request=request,
        name="courses.html",
        context={
            "level": level,
            "semester": semester,
            "semester_name": semester_name,
            "programme": programme,
            "courses": courses,
        },
    )


# INDIVIDUAL COURSE PAGE

@app.get(
    "/course/{course_id}",
    response_class=HTMLResponse
)
def course_page(
    request: Request,
    course_id: int,
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter_by(
        id=course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    resources = (
        db.query(Resource)
        .filter(
            Resource.course_id == course.id,
            Resource.status == "published"
        )
        .order_by(Resource.created_at.desc())
        .all()
    )

    course_key = course.code.replace(" ", "").upper()

    course_data = ACADEMIC_CATALOG.get(
        course_key,
        {}
    )

    return templates.TemplateResponse(
        request=request,
        name="course.html",
        context={
            "course": course,
            "course_data": course_data,
            "resources": resources,
        },
    )


# AI COURSE SUMMARY

@app.post("/api/courses/{course_id}/summary")
def generate_course_summary(
    course_id: int,
    db: Session = Depends(get_db)
):
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="AI summaries are not configured yet. Please try again later."
        )

    course = db.query(Course).filter_by(
        id=course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found."
        )

    course_key = course.code.replace(" ", "").upper()

    course_data = ACADEMIC_CATALOG.get(
        course_key,
        {}
    )

    # Only use information belonging to this course.

    course_information = {
        "course_code": course.code,
        "course_title": course.title or course.code,
        "level": f"{course.level} Level",
        "semester": (
            "First Semester"
            if course.semester == "1"
            else "Second Semester"
        ),
        "definition": course_data.get("definition", ""),
        "outline": course_data.get("outline", []),
        "notes": course_data.get("notes", []),
        "textbooks": course_data.get("textbooks", []),
    }

    prompt = f"""
You are CampusCorrect's academic study assistant.

Create a useful university-level study summary for the course below.

COURSE INFORMATION:
{json.dumps(course_information, ensure_ascii=False, default=str)}

INSTRUCTIONS:

1. Explain what the course is about.
2. Explain the important topics in the supplied course outline.
3. Organize the topics into a logical learning structure.
4. Explain important concepts in understandable language.
5. Identify the foundational knowledge students should understand.
6. Finish with a section called "What to focus on".
7. Use headings and clear paragraphs.
8. Keep the explanation educational and detailed enough to be useful.
9. Do not invent topics, textbooks, lecturer instructions or examination predictions.
10. Do not pretend that missing course information was supplied.
11. If the outline is incomplete, clearly mention that the summary is based on limited information.

Make the summary specific to this course.
Do not give a generic summary that could apply to every course.
"""

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-2.5-flash:generateContent"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 1800
        }
    }

    request_data = json.dumps(payload).encode("utf-8")

    api_request = urllib.request.Request(
        url,
        data=request_data,
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(
            api_request,
            timeout=45
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        summary = (
            result["candidates"][0]
            ["content"]["parts"][0]["text"]
        )

        if not summary.strip():
            raise ValueError("Empty AI response")

        return {
            "course": course.code,
            "summary": summary.strip()
        }

    except urllib.error.HTTPError as error:

        if error.code == 429:
            raise HTTPException(
                status_code=429,
                detail="AI usage is temporarily limited. Please try again later."
            )

        raise HTTPException(
            status_code=502,
            detail="The AI service could not generate your summary."
        )

    except (
        urllib.error.URLError,
        TimeoutError,
        KeyError,
        IndexError,
        ValueError,
        json.JSONDecodeError
    ):

        raise HTTPException(
            status_code=502,
            detail="Unable to generate the summary right now. Please try again."
        )


# EXISTING RESOURCE LIBRARY

@app.get(
    "/resources",
    response_class=HTMLResponse
)
def resources(
    request: Request,
    programme_id: int | None = None,
    level: int | None = None,
    semester: str | None = None,
    db: Session = Depends(get_db)
):
    if not request.session.get("pledged"):
        return RedirectResponse(
            "/pledge",
            status_code=303
        )

    query = db.query(Resource).filter(
        Resource.status == "published"
    )

    if programme_id is not None and level is not None:
        course_ids = [
            course.id
            for course in db.query(Course).filter_by(
                programme_id=programme_id,
                level=level
            ).all()
        ]

        if course_ids:
            query = query.filter(
                Resource.course_id.in_(course_ids)
            )
        else:
            query = query.filter(False)

    resource_items = query.order_by(
        Resource.created_at.desc()
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="resources.html",
        context={
            "resources": resource_items,
            "programme_id": programme_id,
            "level": level,
            "semester": semester,
        },
    )


# PLEDGE PAGE

@app.get(
    "/pledge",
    response_class=HTMLResponse
)
def pledge(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pledge.html",
        context={},
    )


@app.post("/pledge")
def accept_pledge(request: Request):
    request.session["pledged"] = True

    return RedirectResponse(
        "/",
        status_code=303
    )


# ABOUT PAGE

@app.get("/about", response_class=HTMLResponse)
def about_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={},
    )


# CONTRIBUTIONS PAGE

@app.get("/contributions", response_class=HTMLResponse)
def contributions_page(request: Request):

    contributors = [
        {
            "name": "Ebimem Nickson",
            "department": "Computer Science and Informatics",
            "level": "200L",
            "number": "01",
            "initials": "EN",
        }
    ]

    return templates.TemplateResponse(
        request=request,
        name="contributions.html",
        context={
            "contributors": contributors,
        },
    )


# UPLOAD PAGE

@app.get(
    "/upload",
    response_class=HTMLResponse
)
def upload_page(
    request: Request,
    db: Session = Depends(get_db)
):
    university = db.query(University).filter_by(
        code="FUO"
    ).first()

    programmes = []

    if university:
        programmes = (
            db.query(Programme)
            .filter_by(university_id=university.id)
            .order_by(Programme.name)
            .all()
        )

    return templates.TemplateResponse(
        request=request,
        name="upload.html",
        context={
            "programmes": programmes,
        },
    )


# SUBMIT MATERIAL

@app.post("/upload")
async def upload_material(
    title: str = Form(...),
    resource_type: str = Form(...),
    submitter_email: str = Form(""),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not validate_pdf(
        file.filename or "",
        file.content_type
    ):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted in the MVP."
        )

    key = save_file(
        file.file,
        file.filename or "material.pdf"
    )

    item = Upload(
        original_filename=file.filename or "material.pdf",
        title=title,
        resource_type=resource_type,
        file_key=key,
        submitter_email=submitter_email or None,
        status="pending",
    )

    db.add(item)
    db.commit()

    return RedirectResponse(
        "/upload?submitted=1",
        status_code=303
    )


# RESOURCE NOTIFICATIONS

@app.post("/notify")
def notify_when_ready(
    email: str = Form(...),
    resource_id: int = Form(...),
    db: Session = Depends(get_db)
):
    db.add(
        ResourceNotification(
            email=email,
            resource_id=resource_id
        )
    )

    db.commit()

    return RedirectResponse(
        "/resources",
        status_code=303
    )


# HEALTH CHECK

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "campuscorrect"
    }


# PROGRAMME API

@app.get("/api/programmes")
def api_programmes(
    db: Session = Depends(get_db)
):
    university = db.query(University).filter_by(
        code="FUO"
    ).first()

    if not university:
        return []

    programmes = (
        db.query(Programme)
        .filter_by(university_id=university.id)
        .order_by(Programme.name)
        .all()
    )

    return [
        {
            "id": programme.id,
            "name": programme.name,
            "faculty": programme.faculty
        }
        for programme in programmes
    ]


# ACADEMIC CATALOGUE API

@app.get("/api/courses")
def api_courses(
    level: int | None = None,
    semester: str | None = None,
    programme_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Course)

    if programme_id is not None:
        query = query.filter(
            Course.programme_id == programme_id
        )

    if level is not None:
        query = query.filter(
            Course.level == level
        )

    if semester is not None:
        query = query.filter(
            Course.semester == semester
        )

    courses = query.order_by(
        Course.code
    ).all()

    return [
        {
            "id": course.id,
            "code": course.code,
            "title": course.title,
            "level": course.level,
            "semester": course.semester,
            "programme": (
                course.programme.name
                if course.programme
                else None
            ),
        }
        for course in courses
    ]
