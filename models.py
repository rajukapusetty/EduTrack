from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ==========================================
# Database Entities (SQLModel)
# ==========================================
class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Course(SQLModel, table=True):
    __tablename__ = "courses"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    total_lessons: int

class Enrollment(SQLModel, table=True):
    __tablename__ = "enrollments"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    course_id: int = Field(foreign_key="courses.id")
    completed_lessons_count: int = Field(default=0)
    status: str = Field(default="active")  # "active" or "completed"
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)

class Achievement(SQLModel, table=True):
    __tablename__ = "achievements"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    title: str
    unlocked_at: datetime = Field(default_factory=datetime.utcnow)

# ==========================================
# Pydantic Schemas (Request/Response)
# ==========================================
class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int

class ActiveCourseProgress(BaseModel):
    course_id: int
    title: str
    completed_lessons: int
    total_lessons: int
    progress_percentage: float

class DashboardResponse(BaseModel):
    user_id: int
    name: str
    active_courses: List[ActiveCourseProgress]
    achievements: List[str]

class LeaderboardEntry(BaseModel):
    user_id: int
    name: str
    total_completed_lessons: int
