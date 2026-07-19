from typing import Optional

from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi import HTTPException
from db import students, teachers

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Welcome to Student API"
    }


@app.get("/about")
def about():
    return {
        "course": "Backend Bootcamp",
        "name": "Sid"
    }


@app.get("/college")
def college():
    return {
        "college": "LBRCE",
        "branch": "CSE"
    }


@app.get("/contact")
def contact():
    return {
        "email": "sid@example.com"
    }


# -------------------- Models --------------------

class Student(BaseModel):
    name: str
    age: int
    roll_no: str
    branch: str


class Teacher(BaseModel):
    name: str
    teacher_id: str
    department: str


# -------------------- Student Routes --------------------

@app.get("/students")
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


@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: Student):

    result = students.insert_one(student.model_dump())

    return {
        "message": "Student created successfully",
        "id": str(result.inserted_id)
    }
@app.put("/students/{roll_no}")
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

@app.delete("/students/{roll_no}")
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

# -------------------- Teacher Routes --------------------

@app.get("/teachers")
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


@app.post("/teachers", status_code=status.HTTP_201_CREATED)
def create_teacher(teacher: Teacher):

    result = teachers.insert_one(teacher.model_dump())

    return {
        "message": "Teacher created successfully",
        "id": str(result.inserted_id)
    }

@app.put("/teachers/{teacher_id}")
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
        "message": "teacher updated successfully"
    }

@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: str):

    result = teachers.delete_one(
        {"teacher_id": teacher_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="teacher not found"
        )

    return {
        "message":" Teacher deleted successfully"
    }