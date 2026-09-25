from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import StudentDB
from auth_models import UserDB
from schemas import Student, StudentResponse, StudentCreateResponse
from routers.auth import get_current_user


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.get("/", response_model=list[StudentResponse])
def get_students(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(UserDB).filter(
        UserDB.username == current_user
    ).first()

    students = db.query(StudentDB).filter(
        StudentDB.user_id == user.id
    ).all()

    return students


@router.post("/", response_model=StudentCreateResponse)
def add_student(
    student: Student,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    existing_student = db.query(StudentDB).filter(
        StudentDB.id == student.id
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="Student ID already exists"
        )

    user = db.query(UserDB).filter(
        UserDB.username == current_user
    ).first()

    new_student = StudentDB(
        id=student.id,
        name=student.name,
        age=student.age,
        course=student.course,
        user_id=user.id
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Student added successfully",
        "student": new_student
    }


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(UserDB).filter(
        UserDB.username == current_user
    ).first()

    student = db.query(StudentDB).filter(
        StudentDB.id == student_id,
        StudentDB.user_id == user.id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student

@router.put("/{student_id}", response_model=StudentCreateResponse)
def update_student(
    student_id: int,
    updated_student: Student,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(UserDB).filter(
        UserDB.username == current_user
    ).first()

    student = db.query(StudentDB).filter(
        StudentDB.id == student_id,
        StudentDB.user_id == user.id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.name = updated_student.name
    student.age = updated_student.age
    student.course = updated_student.course

    db.commit()
    db.refresh(student)

    return {
        "message": "Student updated successfully",
        "student": student
    }


@router.delete("/{student_id}", response_model=StudentCreateResponse)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(UserDB).filter(
        UserDB.username == current_user
    ).first()

    student = db.query(StudentDB).filter(
        StudentDB.id == student_id,
        StudentDB.user_id == user.id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully",
        "student": student
    }