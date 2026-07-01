from models import User, Course, Enrollment, Achievement, ActiveCourseProgress, DashboardResponse, LeaderboardEntry
from database import SessionLocal
from sqlmodel import select, func
from datetime import datetime
from typing import List, Tuple, Any

def seed_database():
    """Seeds the initial courses and a test user if the database is empty."""
    db = SessionLocal()
    try:
        if not db.exec(select(Course)).first():
            courses = [
                Course(title="Python Basics", description="Learn Python from scratch", total_lessons=5),
                Course(title="Intro to FastAPI", description="Build APIs quickly", total_lessons=3),
                Course(title="SQL 101", description="Master databases", total_lessons=10)
            ]
            db.add_all(courses)
            db.add(User(name="Test Student", email="student@example.com"))
            db.commit()
    finally:
        db.close()

def enroll_user(user_id: int, course_id: int) -> Tuple[bool, str, Any]:
    """Enrolls a user in a course. Returns (Success, Message, EnrollmentObject)."""
    db = SessionLocal()
    try:
        user = db.get(User, user_id)
        course = db.get(Course, course_id)
        
        if not user: return False, "User not found", None
        if not course: return False, "Course not found", None

        # Check for existing active enrollment
        existing = db.exec(
            select(Enrollment).where(
                Enrollment.user_id == user_id,
                Enrollment.course_id == course_id,
                Enrollment.status == "active"
            )
        ).first()
        
        if existing:
            return False, "User is already actively enrolled in this course", None

        new_enrollment = Enrollment(user_id=user_id, course_id=course_id)
        db.add(new_enrollment)
        db.commit()
        db.refresh(new_enrollment)
        return True, "Enrolled successfully", new_enrollment
    finally:
        db.close()

def complete_lesson(enrollment_id: int) -> Tuple[bool, str, Any]:
    """Increments lesson count and handles automated achievements."""
    db = SessionLocal()
    try:
        enrollment = db.get(Enrollment, enrollment_id)
        if not enrollment:
            return False, "Enrollment not found", None
            
        if enrollment.status == "completed":
            return False, "Course is already completed", None

        course = db.get(Course, enrollment.course_id)
        enrollment.completed_lessons_count += 1
        messages = ["Lesson completed successfully"]

        # Check for course completion
        if enrollment.completed_lessons_count >= course.total_lessons:
            enrollment.status = "completed"
            enrollment.completed_at = datetime.utcnow()
            messages.append(f"Course '{course.title}' completed!")
            
            # Achievement Logic
            completed_courses = db.exec(
                select(Enrollment).where(
                    Enrollment.user_id == enrollment.user_id, 
                    Enrollment.status == "completed"
                )
            ).all()
            
            if len(completed_courses) == 0: 
                db.add(Achievement(user_id=enrollment.user_id, title="Fast Starter"))
                messages.append("Achievement unlocked: Fast Starter!")

            if course.total_lessons >= 10:
                db.add(Achievement(user_id=enrollment.user_id, title="Deep Diver"))
                messages.append("Achievement unlocked: Deep Diver!")

        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
        return True, " - ".join(messages), enrollment
    finally:
        db.close()

def get_dashboard(user_id: int) -> DashboardResponse | None:
    """Retrieves user dashboard data."""
    db = SessionLocal()
    try:
        user = db.get(User, user_id)
        if not user:
            return None

        active_enrollments = db.exec(
            select(Enrollment, Course)
            .join(Course, Enrollment.course_id == Course.id)
            .where(Enrollment.user_id == user_id, Enrollment.status == "active")
        ).all()

        active_courses = []
        for enr, crs in active_enrollments:
            progress = (enr.completed_lessons_count / crs.total_lessons) * 100
            active_courses.append(
                ActiveCourseProgress(
                    course_id=crs.id,
                    title=crs.title,
                    completed_lessons=enr.completed_lessons_count,
                    total_lessons=crs.total_lessons,
                    progress_percentage=round(progress, 2)
                )
            )

        achievements = db.exec(
            select(Achievement.title).where(Achievement.user_id == user_id)
        ).all()

        return DashboardResponse(
            user_id=user.id,
            name=user.name,
            active_courses=active_courses,
            achievements=achievements
        )
    finally:
        db.close()

def get_leaderboard() -> List[LeaderboardEntry]:
    """Retrieves the top 5 users based on total completed lessons."""
    db = SessionLocal()
    try:
        statement = (
            select(User.id, User.name, func.sum(Enrollment.completed_lessons_count).label("total_lessons"))
            .join(Enrollment, User.id == Enrollment.user_id)
            .group_by(User.id)
            .order_by(func.sum(Enrollment.completed_lessons_count).desc())
            .limit(5)
        )
        results = db.exec(statement).all()
        
        return [
            LeaderboardEntry(
                user_id=row.id,
                name=row.name,
                total_completed_lessons=row.total_lessons or 0
            ) for row in results
        ]
    finally:
        db.close()
