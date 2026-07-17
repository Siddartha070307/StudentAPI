from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import status
from fastapi import HTTPException
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")

db = client["student_db"]

collection = db["students"]
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
        "age" :19,
        "roll_no": "23CS001",
        "branch": "CSE"
    },
    2: {
        "name": "Rahul",
        "age" :20,
        "roll_no": "23CS002",
        "branch": "ECE"
    },
    3: {
        "name": "Anitha",
        "age" :18,
        "roll_no": "23CS003",
        "branch": "CSE"
    }
}


class Student(BaseModel):
    name: str
    age: int
    roll_no: str
    branch: str

class Teacher(BaseModel):
    name : str
    teacher_id:str
    department:str



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
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail=" student Not found"
        )
    return students[student_id]


@app.post("/students",status_code=status.HTTP_201_CREATED)
def create_student(student: Student):
    new_id = max(students.keys()) + 1 if students else 1

    students[new_id] = {
        "name": student.name,
        "age": student.age,
        "roll_no": student.roll_no,
        "branch": student.branch
    }

    return {
        "message": "Student created successfully",
        "student_id":new_id,
        "student": students[new_id]
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
   if teacher_id not in teachers:
       raise HTTPException(
           status_code=404,
           detail="Teacher Not Found"
       )
   return teachers[teacher_id]


@app.post("/teachers",status_code=status.HTTP_201_CREATED)
def create_teachers(teacher:Teacher):
    teach_id = max(teachers.keys()) + 1 if teachers else 1
    teachers[teach_id] = {
        "name": teacher.name,
        "teacher_id": teacher.teacher_id,
        "department": teacher.department
    }

    return {
        "message": "Teacher created successfully",
        "Teacher_id":teach_id,
        "Teacher": teachers[teach_id]
    }



@app.put("/students/{student_id}")
def update_students(student_id:int,student:Student):
    if student_id not in students:
       raise HTTPException(
           status_code=404,
           detail="Student Not Found"
       )
    students[student_id] = {
        "name" : student.name,
        "age": student.age,
        "roll_no": student.roll_no,
        "branch": student.branch
    }

    return{
        "message":"Updated succefully",
        "Student-id":students[student_id]
    }
@app.put("/teachers/{teacher_id}")
def update_teachers(teacher_id:int,teacher:Teacher):
    if teacher_id not in teachers:
       raise HTTPException(
           status_code=404,
           detail="Teacher Not Found"
       )
    teachers[teacher_id] = {
        "name" : teacher.name,
        "teacher_id": teacher.teacher_id,
        "departent": teacher.department
    }

    return{
        "message":"Updated succefully",
        "teachers-id":teachers[teacher_id]
    }

@app.delete("/students/{student_id}")
def delete_students(student_id:int):
    if student_id not in students:
       raise HTTPException(
           status_code=404,
           detail="Student Not Found"
       )
    deleted_student = students.pop(student_id)
    return{
        "Message":"Student Deleted Succefully",
        "Deleted-student":deleted_student
    }
@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id:int):
    if teacher_id not in teachers:
       raise HTTPException(
           status_code=404,
           detail="Teacher Not Found"
       )
    deleted_teacher = teachers.pop(teacher_id)
    return{
        "Message":"teacher Deleted Succefully",
        "Deleted-teacher":deleted_teacher
    }