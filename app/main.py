from pathlib import Path
from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .config import settings
from .models import University, Programme, Course, Resource, Upload, ResourceNotification
from .storage import save_file, validate_pdf
from .seed import seed

Base.metadata.create_all(bind=engine)
seed()

app = FastAPI(title="CampusCorrect", version="0.1.0")
app.add_middleware(SessionMiddleware, secret_key=settings.session_secret)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    university = db.query(University).filter_by(code="FUO").first()
    programmes = db.query(Programme).filter_by(university_id=university.id).order_by(Programme.name).all()
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "university": university,
            "programmes": programmes,
        },
    )

@app.get("/resources", response_class=HTMLResponse)
def resources(request: Request, programme_id: int | None = None, level: int | None = None,
              semester: str | None = None, db: Session = Depends(get_db)):
    if not request.session.get("pledged"):
        return RedirectResponse("/pledge", status_code=303)
    query = db.query(Resource).filter(Resource.status == "published")
    if programme_id and level:
        course_ids = [c.id for c in db.query(Course).filter_by(programme_id=programme_id, level=level).all()]
        query = query.filter(Resource.course_id.in_(course_ids)) if course_ids else query.filter(False)
    resources = query.order_by(Resource.created_at.desc()).all()
    return templates.TemplateResponse(
        request=request,
        name="resources.html",
        context={
            "resources": resources,
            "programme_id": programme_id,
            "level": level,
            "semester": semester,
        },
    )

@app.get("/pledge", response_class=HTMLResponse)
def pledge(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pledge.html",
        context={},
    )

@app.post("/pledge")
def accept_pledge(request: Request):
    request.session["pledged"] = True
    return RedirectResponse("/resources", status_code=303)

@app.get("/upload", response_class=HTMLResponse)
def upload_page(request: Request, db: Session = Depends(get_db)):
    university = db.query(University).filter_by(code="FUO").first()
    programmes = db.query(Programme).filter_by(university_id=university.id).order_by(Programme.name).all()
    return templates.TemplateResponse(
        request=request,
        name="upload.html",
        context={"programmes": programmes},
    )

@app.post("/upload")
async def upload_material(
    title: str = Form(...),
    resource_type: str = Form(...),
    submitter_email: str = Form(""),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not validate_pdf(file.filename or "", file.content_type):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted in the MVP.")

    key = save_file(file.file, file.filename or "material.pdf")
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
    return RedirectResponse("/upload?submitted=1", status_code=303)

@app.post("/notify")
def notify_when_ready(email: str = Form(...), resource_id: int = Form(...), db: Session = Depends(get_db)):
    db.add(ResourceNotification(email=email, resource_id=resource_id))
    db.commit()
    return RedirectResponse("/resources", status_code=303)

@app.get("/health")
def health():
    return {"status": "ok", "service": "campuscorrect"}

@app.get("/api/programmes")
def api_programmes(db: Session = Depends(get_db)):
    university = db.query(University).filter_by(code="FUO").first()
    return [{"id": p.id, "name": p.name, "faculty": p.faculty} for p in db.query(Programme).filter_by(university_id=university.id).all()]
