from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class University(Base):
    __tablename__ = "universities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    code: Mapped[str] = mapped_column(String(30), unique=True, index=True)

class Programme(Base):
    __tablename__ = "programmes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(ForeignKey("universities.id"), index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    faculty: Mapped[str | None] = mapped_column(String(200), nullable=True)
    university = relationship("University")

class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    programme_id: Mapped[int] = mapped_column(ForeignKey("programmes.id"), index=True)
    code: Mapped[str] = mapped_column(String(40), index=True)
    title: Mapped[str] = mapped_column(String(250))
    level: Mapped[int] = mapped_column(Integer)
    semester: Mapped[str] = mapped_column(String(30))
    programme = relationship("Programme")

class Resource(Base):
    __tablename__ = "resources"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(300))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    resource_type: Mapped[str] = mapped_column(String(80), index=True)
    file_key: Mapped[str | None] = mapped_column(String(600), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    course_id: Mapped[int | None] = mapped_column(ForeignKey("courses.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(40), default="published", index=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    course = relationship("Course")

class Upload(Base):
    __tablename__ = "uploads"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_filename: Mapped[str] = mapped_column(String(500))
    title: Mapped[str] = mapped_column(String(300))
    resource_type: Mapped[str] = mapped_column(String(80))
    file_key: Mapped[str | None] = mapped_column(String(600), nullable=True)
    submitter_email: Mapped[str | None] = mapped_column(String(320), nullable=True)
    status: Mapped[str] = mapped_column(String(40), default="pending", index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class ResourceNotification(Base):
    __tablename__ = "resource_notifications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(320), index=True)
    resource_id: Mapped[int] = mapped_column(ForeignKey("resources.id"))
    sent: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resource = relationship("Resource")

# Reserved for Phase  future: Nigeria-wide student communities/chat.
class Community(Base):
    __tablename__ = "communities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    scope: Mapped[str] = mapped_column(String(80), default="university")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
