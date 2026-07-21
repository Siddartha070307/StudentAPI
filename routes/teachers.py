from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from db import teachers
from models import Teacher
router = APIRouter()



@router.get("/teachers")
def get_teachers(department: Optional[str] = None):

    result = []

    if department:
        cursor = teachers.find({"department": department})
    else:
        cursor = teachers.find()

    for teacher in cursor:
        teacher["_id"] = str(teacher["_id"])
        result.append(teacher)

    return result


@router.post("/teachers", status_code=status.HTTP_201_CREATED)
def create_teacher(teacher: Teacher):

    result = teachers.insert_one(teacher.model_dump())

    return {
        "message": "Teacher created successfully",
        "id": str(result.inserted_id)
    }


@router.put("/teachers/{teacher_id}")
def update_teacher(teacher_id: str, teacher: Teacher):

    result = teachers.update_one(
        {"teacher_id": teacher_id},
        {
            "$set": teacher.model_dump()
        }
    )

    if result.matched_count == 0:
        return {
            "message": "Teacher not found"
        }

    return {
        "message": "Teacher updated successfully"
    }


@router.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: str):

    result = teachers.delete_one(
        {"teacher_id": teacher_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return {
        "message": "Teacher deleted successfully"
    }