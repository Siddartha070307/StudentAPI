from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

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


students = {
    1: {
        "name": "Sid",
        "roll_no": "23CS001",
        "branch": "CSE"
    },
    2: {
        "name": "Rahul",
        "roll_no": "23CS002",
        "branch": "ECE"
    },
    3: {
        "name": "Anitha",
        "roll_no": "23CS003",
        "branch": "CSE"
    }
}


class Student(BaseModel):
    name: str
    age: int
    roll_no: str
    branch: str


@app.get("/students")
def get_students(branch: Optional[str] = None):
    if branch is None:
        return students

    result = []

    for student in students.values():
        if student["branch"] == branch:
            result.append(student)

    return result


@app.get("/students/{student_id}")
def get_student_by_id(student_id: int):
    return students.get(student_id, {"error": "Student Not Found"})

@app.post("/students")
def create_student(student: Student):
    return {
        "message": "Student Created",
        "student": student
    }
teachers = {
    1: {
        "name": "Ram",
        "teacher_id": "T100",
        "department": "CSE"
    },
    2: {
        "name": "Sita",
        "teacher_id": "T101",
        "department": "ECE"
    },
    3: {
        "name": "Krishna",
        "teacher_id": "T102",
        "department": "ME"
    }
}


@app.get("/teachers")
def get_teachers(department: Optional[str] = None):
    if department is None:
        return teachers

    result = []

    for teacher in teachers.values():
        if teacher["department"] == department:
            result.append(teacher)

    return result


@app.get("/teachers/{teacher_id}")
def get_teacher_by_id(teacher_id: int):
    return teachers.get(teacher_id, {"error": "Teacher Not Found"})