from fastapi import FastAPI, HTTPException, status
from models import Enrollment, EnrollmentCreate, DashboardResponse, LeaderboardEntry
from database import init_db
import service

# Create all database tables and seed initial data
init_db()
service.seed_database()

# FastAPI app instance with the EduTrack name
app = FastAPI(title="EduTrack — Micro-Learning Progress & Analytics API", version="1.0.0")

# ==========================================
# Enrollments & Progress Endpoints
# ==========================================

@app.post("/enrollments", response_model=Enrollment, status_code=status.HTTP_201_CREATED)
async def create_enrollment(req: EnrollmentCreate):
    """Enrolls a user in a course"""
    success, message, enrollment = service.enroll_user(req.user_id, req.course_id)
    
    if not success:
        if "not found" in message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
        
    return enrollment


@app.post("/enrollments/{enrollment_id}/complete-lesson", status_code=status.HTTP_200_OK)
async def complete_course_lesson(enrollment_id: int):
    """Increments completed lessons and triggers automated achievements"""
    success, message, enrollment = service.complete_lesson(enrollment_id)
    
    if not success:
        if "not found" in message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
        
    return {"message": message, "enrollment": enrollment}

# ==========================================
# Dashboard & Analytics Endpoints
# ==========================================

@app.get("/users/{user_id}/dashboard", response_model=DashboardResponse, status_code=status.HTTP_200_OK)
async def read_user_dashboard(user_id: int):
    """Returns user details, active course progress, and achievements"""
    dashboard_data = service.get_dashboard(user_id)
    
    if dashboard_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    return dashboard_data


@app.get("/analytics/leaderboard", response_model=list[LeaderboardEntry], status_code=status.HTTP_200_OK)
async def read_leaderboard():
    """Returns top 5 users based on total completed lessons"""
    return service.get_leaderboard()


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    """Health check endpoint"""
    return {"message": "EduTrack API is running", "version": "1.0.0"}
