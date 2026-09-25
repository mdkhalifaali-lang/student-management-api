from fastapi import APIRouter, HTTPException, Depends, Query
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
    name: str | None = None,
    course: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(UserDB).filter(
        UserDB.username == current_user
    ).first()

    query = db.query(StudentDB).filter(
        StudentDB.user_id == user.id
    )

    if name is not None:
        query = query.filter(StudentDB.name.ilike(f"%{name}%"))

    if course is not None:
        query = query.filter(StudentDB.course.ilike(f"%{course}%"))

    sort_fields = {
        "id": StudentDB.id,
        "name": StudentDB.name,
        "age": StudentDB.age,
        "course": StudentDB.course,
    }
    if sort_by not in sort_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    normalized_order = order.lower()
    if normalized_order not in {"asc", "desc"}:
        raise HTTPException(status_code=400, detail="Invalid sort order")

    sort_column = sort_fields[sort_by]
    query = query.order_by(
        sort_column.asc() if normalized_order == "asc" else sort_column.desc()
    )

    students = query.offset(skip).limit(limit).all()

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
