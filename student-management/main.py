from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal, engine
import models, schemas

# Create tables
models.Base.metadata.create_all(bind=engine)


# FastAPI app with metadata
app = FastAPI(
    title="Student Management API",
    description="API for managing student records with CRUD operations",
    version="1.0.0"
)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ROOT ENDPOINT
@app.get("/")
def home():
    return {
        "message": "Welcome to Student Management API",
        "usage": "Go to /docs to test API",
        "features": [
            "Create Student",
            "Get Students",
            "Update Student",
            "Delete Student"
        ]
    }

# CREATE STUDENT
@app.post("/students", response_model=schemas.StudentResponse, status_code=201, tags=["Students"])
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    new_student = models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# GET ALL STUDENTS + FILTER (BONUS INCLUDED)
@app.get("/students", tags=["Students"])
def get_students(course: str = None, db: Session = Depends(get_db)):

    # Filter by course (case-insensitive)
    if course:
        students = db.query(models.Student).filter(
            func.lower(models.Student.course) == course.lower()
        ).all()

        return {
            "filter": f"course = {course}",
            "count": len(students),
            "data": students
        }

    # Get all students
    students = db.query(models.Student).all()
    return {
        "message": "All students",
        "count": len(students),
        "data": students
    }

# GET STUDENT BY ID
@app.get("/students/{id}", tags=["Students"])
def get_student(id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# UPDATE STUDENT
@app.put("/students/{id}", tags=["Students"])
def update_student(id: int, updated: schemas.StudentCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.name = updated.name
    student.age = updated.age
    student.course = updated.course

    db.commit()
    db.refresh(student)

    return {
        "message": "Student updated successfully",
        "data": student
    }

# DELETE STUDENT
@app.delete("/students/{id}", tags=["Students"])
def delete_student(id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}

@app.get("/health")
def health_check():
    return {"status": "API is running fine "}