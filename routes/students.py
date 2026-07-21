from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from db import students

router = APIRouter()
from models import Student

@router.get("/students")
def get_students(branch: Optional[str] = None):

    result = []

    if branch:
        cursor = students.find({"branch": branch})
    else:
        cursor = students.find()

    for student in cursor:
        student["_id"] = str(student["_id"])
        result.append(student)

    return result


@router.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: Student):

    result = students.insert_one(student.model_dump())

    return {
        "message": "Student created successfully",
        "id": str(result.inserted_id)
    }


@router.put("/students/{roll_no}")
def update_student(roll_no: str, student: Student):

    result = students.update_one(
        {"roll_no": roll_no},
        {
            "$set": student.model_dump()
        }
    )

    if result.matched_count == 0:
        return {
            "message": "Student not found"
        }

    return {
        "message": "Student updated successfully"
    }


@router.delete("/students/{roll_no}")
def delete_student(roll_no: str):

    result = students.delete_one(
        {"roll_no": roll_no}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student deleted successfully"
    }